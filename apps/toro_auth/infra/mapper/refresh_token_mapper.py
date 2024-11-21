from apps.toro_auth.domain.entity.refresh_token import RefreshToken
from apps.toro_auth.infra.models.refresh_token_model import RefreshTokenModel
from apps.toro_auth.infra.models.account_model import AccountModel

class RefreshTokenMapper:
    """ RefreshToken 모델과 도메인 엔티티 간 변환 """

    @staticmethod
    def to_entity(refresh_token_model: RefreshTokenModel) -> RefreshToken:
        """ ORM 모델 -> 도메인 엔티티 변환 """
        return RefreshToken(
            id=refresh_token_model.id,
            token=refresh_token_model.token,
            created_at=refresh_token_model.created_at,
            updated_at=refresh_token_model.updated_at,
            account_id=refresh_token_model.account.id if refresh_token_model.account else None,
        )

    @staticmethod
    def from_entity(refresh_token: RefreshToken) -> RefreshTokenModel:
        """ 도메인 엔티티 -> ORM 모델 변환 """
        account_instance = AccountModel.objects.get(id=refresh_token.account_id) if refresh_token.account_id else None
        return RefreshTokenModel(
            id=refresh_token.id,
            token=refresh_token.token,
            created_at=refresh_token.created_at,
            updated_at=refresh_token.updated_at,
            account=account_instance,
        )
