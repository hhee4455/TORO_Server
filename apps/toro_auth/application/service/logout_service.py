from apps.toro_auth.application.repositories.token_repository import TokenRepository
import logging

class LogoutService:
    """로그아웃 서비스."""

    def __init__(self, token_repository: TokenRepository):
        self.token_repository = token_repository

    def logout_user(self, token: str) -> str:
        logging.info(f"Logging out with token: {token}")  # 디버깅 로그
        account_id = self.token_repository.get_account_id(token)

        if account_id:
            logging.debug(f"Account ID found: {account_id}")  # 디버깅 로그
            self.token_repository.delete(token)
            return "Logout successful"
        else:
            logging.warning("Invalid token provided for logout")  # 경고 로그
            raise ValueError("Invalid token")
