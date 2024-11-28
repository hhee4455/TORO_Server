from apps.toro_auth.domain.entity.social_account import SocialAccount
from apps.toro_auth.infra.orm.models.social_account_model import SocialAccountModel
from apps.toro_auth.infra.orm.models.account_model import AccountModel

class SocialAccountMapper:
    """ SocialAccount 모델과 도메인 엔티티 간 변환 """

    @staticmethod
    def to_entity(social_account_model: SocialAccountModel) -> SocialAccount:
        """ ORM 모델 -> 도메인 엔티티 변환 """
        return SocialAccount(
            id=social_account_model.id,
            provider=social_account_model.provider,
            provider_user_id=social_account_model.provider_user_id,
            access_token=social_account_model.access_token,
            refresh_token=social_account_model.refresh_token,
            account_id=social_account_model.account.id if social_account_model.account else None,
        )

    @staticmethod
    def from_entity(social_account: SocialAccount) -> SocialAccountModel:
        """ 도메인 엔티티 -> ORM 모델 변환 """
        account_instance = AccountModel.objects.get(id=social_account.account_id) if social_account.account_id else None
        return SocialAccountModel(
            id=social_account.id,
            provider=social_account.provider,
            provider_user_id=social_account.provider_user_id,
            access_token=social_account.access_token,
            refresh_token=social_account.refresh_token,
            account=account_instance,
        )
