import logging
from redis import Redis
from redis.exceptions import RedisError
from typing import Optional
from apps.toro_auth.application.repositories.token_repository import TokenRepository


def handle_redis_errors(func):
    """Redis 에러를 처리하는 데코레이터"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RedisError as e:
            logging.error(f"Redis error in {func.__name__}: {str(e)}")
            raise RuntimeError(f"Redis operation failed: {str(e)}") from e
    return wrapper


class TokenRepositoryImpl(TokenRepository):
    """Redis를 사용하는 리프레시 토큰 저장소 구현체."""

    def __init__(self, redis_client: Redis, ttl: int = 60 * 60 * 24 * 7):
        if not redis_client.ping():  # Redis 연결 확인
            raise RuntimeError("Redis server is not reachable")
        self.redis_client = redis_client
        self.ttl = ttl

    @handle_redis_errors
    def save(self, token: str, account_id: str, ttl: int = None) -> None:
        key = f"refresh_token:{token}"
        effective_ttl = ttl or self.ttl
        self.redis_client.set(key, account_id, ex=effective_ttl)

    @handle_redis_errors
    def delete(self, token: str) -> None:
        key = f"refresh_token:{token}"
        result = self.redis_client.delete(key)
        if result == 0:
            logging.warning(f"No key found to delete for token: {token}")

    @handle_redis_errors
    def get_account_id(self, token: str) -> Optional[str]:
        """
        Redis에서 주어진 토큰에 매핑된 account_id를 조회합니다.
        """
        key = f"refresh_token:{token}"
        account_id = self.redis_client.get(key)
        if account_id is not None and isinstance(account_id, bytes):
            account_id = account_id.decode("utf-8")
        return account_id

    @handle_redis_errors
    def validate_refresh_token(self, token: str) -> Optional[str]:
        account_id = self.get_account_id(token)
        if not account_id:
            logging.warning(f"Invalid or expired refresh token: {token}")
        return account_id