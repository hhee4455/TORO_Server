import jwt
import secrets
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError
from src.application.toro_auth.repository.account_repository import AccountRepository
from src.application.toro_auth.repository.refresh_token_repository import RefreshTokenRepository
from django.contrib.auth import hashers

SECRET_KEY = secrets.token_hex(32)

class LoginService:
    """로그인 로직을 처리하는 서비스 클래스."""

    def __init__(self, account_repository: AccountRepository, refresh_token_repository: RefreshTokenRepository):
        self.account_repository = account_repository
        self.refresh_token_repository = refresh_token_repository

    def login_user(self, email: str, password: str) -> dict:
        """로그인 처리."""
        account = self.account_repository.find_by_email(email)
        
        if not account:
            raise ValidationError({"detail": "이메일 또는 비밀번호가 일치하지 않습니다."})

        # 비밀번호 비교: 저장된 비밀번호 해시와 입력한 비밀번호 해시 비교
        if not hashers.check_password(password, account.password):
            raise ValidationError({"detail": "이메일 또는 비밀번호가 일치하지 않습니다."})

        # 리프레시 토큰 생성
        refresh_token_str = self._create_refresh_token()

        # 리프레시 토큰을 저장 (account.id를 사용하여 저장)
        refresh_token = self.refresh_token_repository.create(refresh_token_str, str(account.id))

        return {
            "message": "로그인이 완료되었습니다.",
            "account": {
                "id": str(account.id),
                "email": account.email,
                "name": account.name,
                "date_joined": account.date_joined
            },
            "access_token": self._create_access_token(account),
            "refresh_token": refresh_token.token
        }

    def _create_refresh_token(self) -> str:
        """64자리 리프레시 토큰 생성."""
        return secrets.token_urlsafe(64)

    def _create_access_token(self, account) -> str:
        """JWT 액세스 토큰 생성."""
        payload = {
            "id": str(account.id),  # UUID를 문자열로 변환
            "email": account.email,
            "exp": datetime.now() + timedelta(hours=1),  # 1시간 후 만료
        }
        return jwt.encode(payload, "secret_key", algorithm="HS256")
