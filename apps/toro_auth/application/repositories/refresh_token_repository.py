from abc import ABC, abstractmethod
from typing import Optional

class RefreshTokenRepository(ABC):
    """리프레시 토큰 저장소 추상화."""

    @abstractmethod
    def save(self, token: str, user_id: str, ttl: int) -> None:
        """리프레시 토큰 저장."""
        pass

    @abstractmethod
    def find_by_token(self, token: str) -> Optional[str]:
        """리프레시 토큰으로 사용자 ID를 조회."""
        pass

    @abstractmethod
    def delete(self, user_id: str) -> None:
        """사용자 ID로 리프레시 토큰 삭제."""
        pass
