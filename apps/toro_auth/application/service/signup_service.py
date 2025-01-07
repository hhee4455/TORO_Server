from rest_framework.exceptions import ValidationError
from apps.toro_auth.application.repositories.account_repository import AccountRepository

class SignupService:
    """회원가입 로직을 처리하는 서비스 클래스."""

    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository

    def signup_user(self, email: str, password: str, name: str, nickname: str, phone: str) -> dict:
        """회원가입 처리."""
        if self.account_repository.find_by_email(email):
            raise ValidationError({"detail": "이미 가입된 이메일 주소입니다."}, code="email_taken")

        # 계정 생성
        account = self.account_repository.create(email, password, name, nickname, phone)

        return {
            "message": "회원가입이 완료되었습니다.",
            "account": {
                "id": str(account.id),
                "email": account.email,
                "name": account.name,
                "date_joined": account.date_joined,
                "nickname": account.nickname,
                "phone": account.phone,
            }
        }