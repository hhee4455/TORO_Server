# apps/toro_auth/infra/mapper/account_mapper.py
from apps.toro_auth.domain.entity.account import Account as DomainAccount
from apps.toro_auth.infra.models.account_model import AccountModel

class AccountMapper:
    @staticmethod
    def to_domain(account_model: AccountModel) -> DomainAccount:
        return DomainAccount(
            id=account_model.id,
            email=account_model.email,
            password=account_model.password,
            name=account_model.name,
            date_joined=account_model.date_joined,
            is_staff=account_model.is_staff,
            phone=account_model.phone,
            verification_code=account_model.verification_code
        )

    @staticmethod
    def to_model(domain_account: DomainAccount) -> AccountModel:
        return AccountModel(
            id=domain_account.id,
            email=domain_account.email,
            password=domain_account.password,
            name=domain_account.name,
            date_joined=domain_account.date_joined,
            is_staff=domain_account.is_staff,
            phone=domain_account.phone,
            verification_code=domain_account.verification_code
        )
