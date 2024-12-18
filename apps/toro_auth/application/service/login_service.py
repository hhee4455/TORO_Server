import jwt
import secrets
from datetime import datetime, timedelta
from django.contrib.auth.hashers import check_password
from apps.toro_auth.application.repositories.redis_repository import RedisRepository
from apps.toro_auth.application.repositories.account_repository import AccountRepository

class LoginService:
    """로그인 서비스: 사용자 인증 및 토큰 생성"""

    def __init__(self, account_repository: AccountRepository, redis_repository: RedisRepository, secret_key: str):
        """LoginService 초기화"""

        self.account_repository = account_repository
        self.redis_repository = redis_repository
        self.secret_key = secret_key

    def login_user(self, email: str, password: str) -> dict:
        """사용자 로그인 및 토큰 생성"""

        account = self.account_repository.find_by_email(email)
        if not account or not self._check_password(password, account.password):
            raise ValueError("Invalid email or password")

        refresh_token = secrets.token_urlsafe(64)
        try:
            self.redis_repository.save(refresh_token, str(account.id), ttl=60 * 60 * 24 * 7)
        except Exception as e:
            raise RuntimeError(f"Error saving refresh token: {str(e)}") from e

        return {
            "access_token": self._create_access_token(account),
            "refresh_token": refresh_token
        }

    def _check_password(self, raw_password: str, hashed_password: str) -> bool:
        """비밀번호 검증"""

        return check_password(raw_password, hashed_password)

    def _create_access_token(self, account) -> str:
        """Access Token 생성"""
        
        payload = {
            "id": str(account.id),
            "email": account.email,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
