from apps.toro_auth.application.repositories.account_repository import AccountRepository
from apps.toro_auth.application.repositories.refresh_token_repository import RefreshTokenRepository
from rest_framework.exceptions import ValidationError
import secrets 

class SignupService:

    def signup_user(self, email, password, name) -> dict:
        """
        사용자 회원가입 처리
        """
        # 이메일 중복 확인 및 사용자 생성

        account = AccountRepository().find_by_email(email)
        if account:
            raise ValidationError("이미 가입된 이메일 주소입니다.")
        account = AccountRepository().create(email, password, name)
         
        return {
            "message": "회원가입이 완료되었습니다.",
            "access_token": self._generate_access_token(account),
            "refresh_token": self._generate_refresh_token()
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



