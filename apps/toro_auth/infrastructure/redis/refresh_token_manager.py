from redis import Redis
from typing import Optional
from redis.exceptions import RedisError
from apps.toro_auth.application.repositories.refresh_token_repository import RefreshTokenRepository

class RefreshTokenRepositoryImpl(RefreshTokenRepository):
    """Redis를 사용하는 리프레시 토큰 저장소 구현체."""

    def __init__(self, redis_client: Redis, ttl: int = 60 * 60 * 24 * 7):
        """Redis 클라이언트를 초기화하고 기본 TTL을 설정하는 함수."""
        
        self.redis_client = redis_client
        self.ttl = ttl  # 기본 TTL: 7일

    def save(self, token: str, user_id: str, ttl: int = None) -> None:
        """리프레시 토큰과 유저 ID를 Redis에 저장하는 함수."""

        key = f"refresh_token:{token}"
        try:
            self.redis_client.set(key, user_id, ex=ttl or self.ttl)
        except RedisError as e:
            raise RuntimeError(f"Failed to save refresh token: {str(e)}") from e

    def find_user_id_by_token(self, token: str) -> Optional[str]:
        """리프레시 토큰으로 유저 ID를 조회하는 함수."""

        key = f"refresh_token:{token}"
        try:
            user_id = self.redis_client.get(key)
            return user_id.decode() if user_id else None
        except RedisError as e:
            raise RuntimeError(f"Failed to find refresh token: {str(e)}") from e

    def delete(self, token: str) -> None:
        """리프레시 토큰을 Redis에서 삭제하는 함수."""

        key = f"refresh_token:{token}"
        try:
            self.redis_client.delete(key)
        except RedisError as e:
            raise RuntimeError(f"Failed to delete refresh token: {str(e)}") from e
