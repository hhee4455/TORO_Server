from abc import ABC, abstractmethod
from src.domain.toro_auth.entity.refresh_token import RefreshToken

class RefreshTokenRepository(ABC):
    """
    리프레시 토큰과 관련된 데이터 접근 인터페이스.
    """
    
    @abstractmethod
    def save(self, refresh_token: RefreshToken):
        """
        리프레시 토큰을 저장합니다.
        
        Args:
            refresh_token (RefreshToken): 리프레시 토큰 객체
        """
        pass

    @abstractmethod
    def create(self, token: str, account_id: str) -> RefreshToken:
        """
        새로운 리프레시 토큰을 생성합니다.
        
        Args:
            token (str): 리프레시 토큰 값
            account_id (str): 연결된 사용자 ID
        
        Returns:
            RefreshToken: 생성된 리프레시 토큰 객체
        """
        pass

    @abstractmethod
    def find_by_token(self, token: str) -> RefreshToken:
        """
        리프레시 토큰을 통해 해당 토큰을 찾습니다.
        
        Args:
            token (str): 리프레시 토큰
        
        Returns:
            RefreshToken: 리프레시 토큰 객체
        """
        pass
