# application/service/signup_service.py
from apps.toro_auth.domain.repository.refresh_token_repository import RefreshTokenRepository
from apps.toro_auth.domain.entity.refresh_token import RefreshToken
from uuid import uuid4
from django.utils import timezone

class SignupService:
    def __init__(self, account_repository, refresh_token_repository: RefreshTokenRepository):
        self.account_repository = account_repository
        self.refresh_token_repository = refresh_token_repository

    def signup_user(self, email: str, password: str, name: str) -> dict:
        # 이메일 중복 확인 및 사용자 생성
        account = self.account_repository.create(email=email, password=password, name=name)

        # 리프레시 토큰 생성 및 저장
        refresh_token = RefreshToken(
            id=uuid4(),
            token="generated_refresh_token_value",
            created_at=timezone.now(),
            updated_at=timezone.now(),
            account_id=account.id
        )
        self.refresh_token_repository.save(refresh_token)

        return {
            "message": f"{account.name}님의 회원가입이 완료되었습니다.",
            "access_token": "generated_access_token",
            "refresh_token": refresh_token.token
        }
