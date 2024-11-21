from apps.toro_auth.domain.repository.account_repository import AccountRepository
from apps.toro_auth.domain.entity.account import Account
from apps.toro_auth.models import AccountModel  # 실제 Django ORM 모델
from typing import Optional

class AccountRepositoryImpl(AccountRepository):
    def create(self, email: str, password: str, name: str) -> Account:
        account_model = AccountModel.objects.create(email=email, password=password, name=name)
        return Account(
            id=account_model.id,
            email=account_model.email,
            password=account_model.password,
            name=account_model.name,
            date_joined=account_model.date_joined
        )

    def find_by_email(self, email: str) -> Optional[Account]:
        account_model = AccountModel.objects.filter(email=email).first()
        if account_model:
            return Account(
                id=account_model.id,
                email=account_model.email,
                password=account_model.password,
                name=account_model.name,
                date_joined=account_model.date_joined
            )
        return None
