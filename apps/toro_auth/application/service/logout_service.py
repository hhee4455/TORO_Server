from apps.toro_auth.application.repositories.token_repository import TokenRepository

class LogoutService:
    """로그아웃 서비스."""

    def __init__(self, token_repository: TokenRepository):
        self.token_repository = token_repository

    def logout_user(self, user_id: str) -> None:
        self.token_repository.delete(user_id)
