from apps.toro_auth.infra.models.social_account_model import SocialAccountModel
from apps.toro_auth.domain.entity.social_account import SocialAccount

class SocialAccountRepository:
    """SocialAccount 데이터를 관리하는 레포지토리"""

    def get_by_id(self, social_account_id) -> SocialAccount:
        social_account_model = SocialAccountModel.objects.get(id=social_account_id)
        return social_account_model.to_entity()

    def save(self, social_account: SocialAccount):
        social_account_model = SocialAccountModel.from_entity(social_account)
        social_account_model.save()
