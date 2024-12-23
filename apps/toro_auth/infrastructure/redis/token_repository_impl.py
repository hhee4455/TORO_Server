from redis import Redis
from typing import Optional
from redis.exceptions import RedisError
import logging
from apps.toro_auth.application.repositories.token_repository import TokenRepository

class TokenRepositoryImpl(TokenRepository):
    """Redis를 사용하는 리프레시 토큰 저장소 구현체."""

    def __init__(self, redis_client: Redis, ttl: int = 60 * 60 * 24 * 7):
        self.redis_client = redis_client
        self.ttl = ttl

    def save(self, token: str, account_id: str, ttl: int = None) -> None:
        key = f"refresh_token:{token}"
        try:
            self.redis_client.set(key, account_id, ex=ttl or self.ttl)
        except RedisError as e:
            raise RuntimeError(f"Failed to save refresh token: {str(e)}") from e
        
    def delete(self, token: str) -> None:
        key = f"refresh_token:{token}"
        logging.debug(f"Attempting to delete key: {key}")  # 디버깅 로그
        try:
            result = self.redis_client.delete(key)
            logging.debug(f"Redis delete result: {result}")  # 삭제된 키의 개수 로그
            if result == 0:
                logging.warning(f"No key found to delete for token: {token}")  # 키가 없는 경우
        except RedisError as e:
            logging.error(f"Failed to delete refresh token: {str(e)}")
            raise RuntimeError(f"Failed to delete refresh token: {str(e)}") from e


    def get_account_id(self, token: str) -> Optional[str]:
        key = f"refresh_token:{token}"
        logging.debug(f"Retrieving account ID with key: {key}")  # 디버깅 로그
        try:
            account_id = self.redis_client.get(key)
            if isinstance(account_id, bytes):
                account_id = account_id.decode("utf-8")
            logging.debug(f"Retrieved account ID: {account_id}")  # 디버깅 로그
            return account_id
        except RedisError as e:
            logging.error(f"Failed to retrieve account ID: {str(e)}")
            raise RuntimeError(f"Failed to retrieve account ID: {str(e)}") from e
