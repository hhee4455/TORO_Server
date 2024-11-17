from apps.toro_auth.domain.entity.account import Account
from apps.toro_auth.infra.models.account_model import AccountModel

class AccountMapper:
    """ Account ORM 모델과 도메인 엔티티 간 변환 """

    @staticmethod
    def to_entity(account_model: AccountModel) -> Account:
        return Account(
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
    def from_entity(account: Account) -> AccountModel:
        return AccountModel(
            id=account.id,
            email=account.email,
            password=account.password,
            name=account.name,
            date_joined=account.date_joined,
            is_staff=account.is_staff,
            phone=account.phone,
            verification_code=account.verification_code
        )