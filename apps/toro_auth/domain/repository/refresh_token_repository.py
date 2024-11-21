from abc import ABC, abstractmethod
from apps.toro_auth.domain.entity.refresh_token import RefreshToken

class RefreshTokenRepository(ABC):
    """RefreshToken 저장소 인터페이스"""

    @abstractmethod
    def save(self, refresh_token: RefreshToken) -> None:
        """새로운 리프레시 토큰 저장"""
        pass

    @abstractmethod
    def find_by_token(self, token: str) -> RefreshToken:
        """토큰 값으로 리프레시 토큰 조회"""
        pass
