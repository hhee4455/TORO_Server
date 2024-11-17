from apps.toro_auth.infra.models.refresh_token_model import RefreshTokenModel
from apps.toro_auth.domain.entity.refresh_token import RefreshToken

class RefreshTokenRepository:
    """RefreshToken 데이터를 관리하는 레포지토리"""

    def get_by_id(self, token_id) -> RefreshToken:
        token_model = RefreshTokenModel.objects.get(id=token_id)
        return token_model.to_entity()

    def save(self, refresh_token: RefreshToken):
        token_model = RefreshTokenModel.from_entity(refresh_token)
        token_model.save()
