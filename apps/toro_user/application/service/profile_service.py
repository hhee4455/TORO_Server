from apps.toro_user.application.repositories.redis_repository import RedisRepository
from apps.toro_user.application.repositories.detail_repository import DetailRepository


class ProfileService:
    """
    사용자 관련 비즈니스 로직을 처리하는 서비스 클래스.
    """

    def __init__(self, redis_repository: RedisRepository, user_repository: DetailRepository):
        self.user_repository = user_repository
        self.redis_repository = redis_repository

