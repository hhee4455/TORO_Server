# infra/repository/refresh_token_repository_impl.py
from apps.toro_auth.domain.repository.refresh_token_repository import RefreshTokenRepository
from apps.toro_auth.domain.entity.refresh_token import RefreshToken
from apps.toro_auth.infra.models.refresh_token_model import RefreshTokenModel
from apps.toro_auth.infra.mapper.refresh_token_mapper import RefreshTokenMapper

class RefreshTokenRepositoryImpl(RefreshTokenRepository):
    """RefreshToken 저장소 구현체"""

    def save(self, refresh_token: RefreshToken) -> None:
        """새로운 리프레시 토큰 저장"""
        model_data = RefreshTokenMapper.to_model(refresh_token)
        RefreshTokenModel.objects.create(**model_data)

    def find_by_token(self, token: str) -> RefreshToken:
        """토큰 값으로 리프레시 토큰 조회"""
        token_model = RefreshTokenModel.objects.filter(token=token).first()
        if not token_model:
            return None
        return RefreshTokenMapper.to_entity(token_model)
