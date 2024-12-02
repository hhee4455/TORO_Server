from typing import Optional
from apps.toro_auth.domain.entity.refresh_token import RefreshToken
from apps.toro_auth.application.repositories.refresh_token_repository import RefreshTokenRepository
from apps.toro_auth.infra.orm.models.refresh_token_model import RefreshTokenModel
from apps.toro_auth.infra.orm.mapper.refresh_token_mapper import RefreshTokenMapper

class RefreshTokenRepositoryImpl(RefreshTokenRepository):
    """RefreshTokenRepository의 구현체."""

    def save(self, refresh_token: RefreshToken) -> None:
        """리프레시 토큰을 저장."""
        refresh_token_model = RefreshTokenMapper.to_model(refresh_token)
        refresh_token_model.save()

    def create(self, token: str, account_id: str) -> RefreshToken:
        """새로운 리프레시 토큰 생성 및 저장."""
        refresh_token_model = RefreshTokenModel.objects.create(
            token=token,
            account_id=account_id
        )
        return RefreshTokenMapper.to_domain(refresh_token_model)

    def find_by_token(self, token: str) -> Optional[RefreshToken]:
        """리프레시 토큰 값으로 조회."""
        try:
            refresh_token_model = RefreshTokenModel.objects.get(token=token)
            return RefreshTokenMapper.to_domain(refresh_token_model)
        except RefreshTokenModel.DoesNotExist:
            return None
