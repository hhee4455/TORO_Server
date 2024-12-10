from redis import Redis
from typing import Optional
from redis.exceptions import RedisError
from apps.toro_auth.application.repositories.refresh_token_repository import RefreshTokenRepository

class RefreshTokenRepositoryImpl(RefreshTokenRepository):
    """Redis를 사용하는 리프레시 토큰 저장소 구현체."""

    def __init__(self, redis_client: Redis, ttl: int = 60 * 60 * 24 * 7):
        self.redis_client = redis_client
        self.ttl = ttl  # 기본 TTL: 7일

    def save(self, token: str, user_id: str, ttl: int = None) -> None:
        key = f"refresh_token:{user_id}"
        try:
            self.redis_client.set(key, token, ex=ttl or self.ttl)
        except RedisError as e:
            raise Exception(f"Failed to save refresh token: {str(e)}")

    def find_by_token(self, token: str) -> Optional[str]:
        try:
            for key in self.redis_client.scan_iter(match="refresh_token:*"):
                if self.redis_client.get(key).decode() == token:
                    return key.split(":")[1]
        except RedisError as e:
            raise Exception(f"Failed to find refresh token: {str(e)}")
        return None
    
    def delete(self, user_id: str) -> None:
        """Redis에서 리프레시 토큰 삭제."""
        key = f"refresh_token:{user_id}"
        self.redis_client.delete(key)
