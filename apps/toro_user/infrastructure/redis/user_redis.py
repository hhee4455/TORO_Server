from redis import Redis
from redis.exceptions import RedisError
from apps.toro_user.application.repositories.redis_repository import RedisRepository


class RedisRepositoryImpl(RedisRepository):
    """Redis를 사용하는 리프레시 토큰 저장소 구현체."""

    def __init__(self, redis_client: Redis):
        """Redis 클라이언트를 초기화하고 기본 TTL을 설정하는 함수."""
        self.redis_client = redis_client

    def find_user(self, token: str) -> str:
        """리프레시 토큰으로 유저 ID를 Redis에서 조회하는 함수."""
        key = f"refresh_token:{token}"
        try:
            user_id = self.redis_client.get(key)
            if user_id is not None:
                return user_id.decode('utf-8')  # Redis는 바이너리 데이터를 반환하므로 디코딩 필요
            return None
        except RedisError as e:
            raise RuntimeError(f"Failed to find user by token: {str(e)}") from e