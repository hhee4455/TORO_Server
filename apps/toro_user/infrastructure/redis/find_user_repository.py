from redis import Redis
from redis.exceptions import RedisError
from apps.toro_user.application.repositories.find_user_repository import FindUserRepository


class FindUserRepositoryImpl(FindUserRepository):
    """Redis를 사용하는 리프레시 토큰 저장소 구현체."""

    def __init__(self, redis_client: Redis):
        """Redis 클라이언트를 초기화."""
        self.redis_client = redis_client

    def get_account_id(self, refresh_token: str) -> str:
        """리프레시 토큰으로부터 account_id를 가져오는 함수."""
        key = f"refresh_token:{refresh_token}"
        try:
            account_id = self.redis_client.get(key)
            if account_id is None:
                raise ValueError("Refresh token not found")
            # Redis 클라이언트 설정에 따라 반환값 처리
            if isinstance(account_id, bytes):  # decode_responses=False인 경우
                account_id = account_id.decode("utf-8")
            return account_id  # decode_responses=True인 경우 이미 문자열 반환
        except RedisError as e:
            raise RuntimeError(f"Failed to retrieve account_id: {str(e)}") from e
