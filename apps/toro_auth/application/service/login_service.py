import jwt
import secrets
from datetime import datetime, timedelta
from apps.toro_auth.application.repositories.refresh_token_repository import RefreshTokenRepository
from apps.toro_auth.application.repositories.account_repository import AccountRepository

class LoginService:
    """로그인 서비스."""

    def __init__(self, account_repository: AccountRepository, refresh_token_repository: RefreshTokenRepository, secret_key: str):
        self.account_repository = account_repository
        self.refresh_token_repository = refresh_token_repository
        self.secret_key = secret_key

    def login_user(self, email: str, password: str) -> dict:
        account = self.account_repository.find_by_email(email)
        if not account or not self._check_password(password, account.password):
            raise ValueError("Invalid email or password")

        # 리프레시 토큰 생성 및 저장
        refresh_token = secrets.token_urlsafe(64)
        self.refresh_token_repository.save(refresh_token, str(account.id), ttl=60 * 60 * 24 * 7)  # 7일 TTL

        return {
            "access_token": self._create_access_token(account),
            "refresh_token": refresh_token
        }

    def _check_password(self, raw_password: str, hashed_password: str) -> bool:
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, hashed_password)

    def _create_access_token(self, account) -> str:
        payload = {
            "id": str(account.id),
            "email": account.email,
            "exp": datetime.now() + timedelta(hours=1)
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
