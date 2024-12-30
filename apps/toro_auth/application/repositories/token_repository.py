from abc import ABC, abstractmethod

class TokenRepository(ABC):
    """리프레시 토큰 저장소 추상화."""

    @abstractmethod
    def save(self, token: str, user_id: str, ttl: int) -> None:
        """리프레시 토큰 저장."""
        pass

    @abstractmethod
    def delete(self, user_id: str) -> None:
        """사용자 ID로 리프레시 토큰 삭제."""
        pass

    @abstractmethod
    def get_account_id(self, token: str) -> str:
        """리프레시 토큰에서 사용자 ID를 추출."""
        pass 

    @abstractmethod
    def validate_refresh_token(self, token: str) -> str:
        """리프레시 토큰 유효성 검사."""
        pass