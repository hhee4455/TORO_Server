from apps.toro_auth.domain.entity.account import Account
from apps.toro_auth.application.repositories.account_repository import AccountRepository
from apps.toro_auth.infra.orm.models.account_model import AccountModel
from apps.toro_auth.infra.orm.mapper.account_mapper import AccountMapper  # AccountMapper 임포트
from django.contrib.auth.hashers import make_password
from typing import Optional

class AccountRepositoryImpl(AccountRepository):
    """AccountRepository의 Django ORM을 이용한 구현체."""

    def create(self, email: str, password: str, name: str) -> Account:
        """새로운 사용자를 생성."""
        hashed_password = make_password(password)
        account_model = AccountModel.objects.create(email=email, password=hashed_password, name=name)
        return AccountMapper.to_domain(account_model)

    def find_by_email(self, email: str) -> Optional[Account]:
        """이메일로 사용자 조회."""
        try:
            account_model = AccountModel.objects.get(email=email)
            return AccountMapper.to_domain(account_model)
        except AccountModel.DoesNotExist:
            return None
