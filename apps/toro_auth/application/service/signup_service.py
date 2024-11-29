import jwt
import secrets
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError
from injector import inject, singleton
from apps.toro_auth.application.repositories.account_repository import AccountRepository
from apps.toro_auth.application.repositories.refresh_token_repository import RefreshTokenRepository

@singleton
class SignupService:
    """
    회원가입과 관련된 비즈니스 로직을 처리하는 서비스 클래스.
    """

    @inject
    def __init__(self, account_repository: AccountRepository, refresh_token_repository: RefreshTokenRepository):
        """
        SignupService 생성자.

        Args:
            account_repository (AccountRepository): 의존성 주입된 계정 레포지토리 구현체
            refresh_token_repository (RefreshTokenRepository): 의존성 주입된 리프레시 토큰 레포지토리 구현체
        """
        self.account_repository = account_repository
        self.refresh_token_repository = refresh_token_repository

    def signup_user(self, email: str, password: str, name: str) -> dict:
        """
        회원가입을 처리하는 메서드.

        Args:
            email (str): 사용자의 이메일 주소
            password (str): 사용자의 비밀번호
            name (str): 사용자의 이름

        Returns:
            dict: 회원가입 결과와 토큰 정보

        Raises:
            ValidationError: 이메일 중복 시 발생
        """
        # 이메일 중복 확인
        account = self.account_repository.find_by_email(email)
        if account:
            raise ValidationError({"detail": "이미 가입된 이메일 주소입니다."}, code="email_taken")

        # 사용자 생성
        account = self.account_repository.create(email, password, name)

        # 리프레시 토큰 생성 및 저장
        refresh_token = self._generate_refresh_token(account)
        self.refresh_token_repository.save(refresh_token)

        return {
            "message": "회원가입이 완료되었습니다.",
            "access_token": self._generate_access_token(account),
            "refresh_token": refresh_token.token  # 토큰 값을 반환
        }

    def _generate_refresh_token(self, account) -> str:
        """
        리프레시 토큰 생성 메서드.

        Args:
            account: 회원 정보 객체

        Returns:
            str: 생성된 리프레시 토큰
        """
        refresh_token = secrets.token_urlsafe(64)
        return refresh_token

    def _generate_access_token(self, account) -> str:
        """
        JWT 액세스 토큰 생성 메서드.

        Args:
            account: 회원 정보 객체

        Returns:
            str: 생성된 액세스 토큰
        """
        payload = {
            "id": account.id,
            "email": account.email,
            "exp": datetime.now() + timedelta(hours=1),  # 토큰 만료 시간
            "iat": datetime.now()  # 토큰 발행 시간
        }
        secret_key = "your_secret_key"  # 실제 환경변수에서 관리 권장
        return jwt.encode(payload, secret_key, algorithm="HS256")
