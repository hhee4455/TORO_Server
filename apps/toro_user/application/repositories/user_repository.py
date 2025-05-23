from abc import ABC, abstractmethod

from apps.toro_user.domain.entity.user import User

class UserRepository(ABC):
    """사용자 관련된 데이터 접근 인터페이스."""

    @abstractmethod
    def find_by_account_id(self, account_id: str) -> User:
        """account_id로 사용자를 찾습니다."""
        pass