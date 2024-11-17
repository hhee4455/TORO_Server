from apps.toro_auth.infra.models import AccountModel
from apps.toro_auth.domain.entity import Account

class AccountRepository:
    """Account 데이터를 관리하는 레포지토리"""

    def get_by_id(self, account_id) -> Account:
        account_model = AccountModel.objects.get(id=account_id)
        return account_model.to_entity()

    def save(self, account: Account):
        account_model = AccountModel.from_entity(account)
        account_model.save()
