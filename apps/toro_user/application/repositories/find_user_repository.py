from abc import ABC, abstractmethod
from typing import Optional

class FindUserRepository(ABC):
    """리프레시 토큰 저장소 추상화."""

    @abstractmethod
    def get_account_id(self, token: str) -> Optional[str]:
        """리프레시 토큰으로 사용자 ID를 조회."""
        pass
