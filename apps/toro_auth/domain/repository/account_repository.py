from abc import ABC, abstractmethod
from typing import Optional
from apps.toro_auth.domain.entity.account import Account

class AccountRepository(ABC):
    @abstractmethod
    def create(self, email: str, password: str, name: str) -> Account:
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Account]:
        pass
