from apps.toro_auth.application.repositories.redis_repository import RedisRepository

class LogoutService:
    """로그아웃 서비스."""

    def __init__(self, refresh_token_repository: RedisRepository):
        self.refresh_token_repository = refresh_token_repository

    def logout_user(self, user_id: str) -> None:
        self.refresh_token_repository.delete(user_id)
