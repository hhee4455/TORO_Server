from abc import ABC, abstractmethod
from apps.toro_auth.domain.entity.account import Account

class AccountRepository(ABC):
    """
    계정과 관련된 데이터 접근 인터페이스.
    """

    @abstractmethod
    def create(self, email: str, password: str, name: str) -> Account:
        """
        사용자 계정을 생성합니다.
        """
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Account:
        """
        이메일로 사용자를 찾습니다.
        """
        pass
