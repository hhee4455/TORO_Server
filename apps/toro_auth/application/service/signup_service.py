from injector import singleton, inject
import jwt
import secrets
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError
from apps.toro_auth.application.repositories.account_repository import AccountRepository
from apps.toro_auth.application.repositories.refresh_token_repository import RefreshTokenRepository

@singleton
class SignupService:
    """회원가입 로직을 처리하는 서비스 클래스."""

    @inject
    def __init__(self, account_repository: AccountRepository, refresh_token_repository: RefreshTokenRepository):
        self.account_repository = account_repository
        self.refresh_token_repository = refresh_token_repository

    def signup_user(self, email: str, password: str, name: str) -> dict:
        """회원가입 처리."""
        if self.account_repository.find_by_email(email):
            raise ValidationError({"detail": "이미 가입된 이메일 주소입니다."}, code="email_taken")

        account = self.account_repository.create(email, password, name)
        refresh_token = self._create_refresh_token()
        self.refresh_token_repository.save(refresh_token)

        return {
            "message": "회원가입이 완료되었습니다.",
            "access_token": self._create_access_token(account),
            "refresh_token": refresh_token
        }

    def _create_refresh_token(self) -> str:
        """64자리 리프레시 토큰 생성."""
        return secrets.token_urlsafe(64)

    def _create_access_token(self, account) -> str:
        """JWT 액세스 토큰 생성."""
        payload = {
            "id": account.id,
            "email": account.email,
            "exp": datetime.now() + timedelta(hours=1),
        }
        return jwt.encode(payload, "secret_key", algorithm="HS256")
