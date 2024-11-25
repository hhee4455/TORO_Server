from uuid import uuid4
from django.utils import timezone
from apps.toro_auth.domain.repository.account_repository import AccountRepository
from apps.toro_auth.domain.repository.refresh_token_repository import RefreshTokenRepository
from apps.toro_auth.domain.entity.refresh_token import RefreshToken
import secrets  # 안전한 랜덤 토큰 생성

class SignupService:
    def __init__(self, refresh_token_repository: RefreshTokenRepository, account_repository: AccountRepository):
        self.account_repository = account_repository
        self.refresh_token_repository = refresh_token_repository

    def signup_user(self, email: str, password: str, name: str) -> dict:
        """
        새로운 사용자 회원가입을 처리합니다.
        이메일 중복 확인 후 계정을 생성하고, 리프레시 토큰을 생성합니다.

        Args:
            email (str): 사용자의 이메일
            password (str): 사용자의 비밀번호
            name (str): 사용자의 이름

        Returns:
            dict: 회원가입 처리 결과 및 토큰 정보
        """
        # 이메일 중복 확인 및 사용자 생성
        account = self.account_repository.create(email=email, password=password, name=name)

        # 리프레시 토큰 값 생성 (안전한 랜덤 값 사용)
        refresh_token_value = secrets.token_urlsafe(32)  # 32 바이트 길이의 안전한 랜덤 토큰 생성

        # 리프레시 토큰 생성
        refresh_token = self.refresh_token_repository.create(
            token=refresh_token_value,  # 생성된 리프레시 토큰 값 사용
            account_id=account.id  # 생성된 계정의 ID 사용
        )

        return {
            "message": f"{account.name}님의 회원가입이 완료되었습니다.",
            "access_token": "generated_access_token",  # 실제 JWT 토큰 생성 로직 필요
            "refresh_token": refresh_token.token
        }


    def _generate_refresh_token(self) -> str:
        """
        리프레시 토큰을 생성하는 헬퍼 메서드

        Returns:
            str: 생성된 리프레시 토큰
        """
        return secrets.token_urlsafe()

    def _generate_access_token(self, account) -> str:
        """
        액세스 토큰을 생성하는 헬퍼 메서드
        실제 JWT 토큰 생성 로직이 여기에 들어갑니다.

        Args:
            account: 회원 정보

        Returns:
            str: 생성된 액세스 토큰
        """
        return secrets.token_urlsafe()  # 실제 토큰 생성 로직은 JWT 라이브러리로 대체



