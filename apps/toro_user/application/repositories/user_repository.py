from abc import ABC, abstractmethod

from apps.toro_user.domain.entity.user import User

class UserRepository(ABC):
    """사용자 관련된 데이터 접근 인터페이스."""

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        """이메일로 사용자를 찾습니다."""
        pass