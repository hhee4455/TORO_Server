from apps.toro_auth.domain.entity.refresh_token import RefreshToken as DomainRefreshToken
from apps.toro_auth.infrastructure.orm.models.refresh_token_model import RefreshTokenModel

class RefreshTokenMapper:
    """RefreshToken의 ORM 모델과 도메인 객체 간의 매퍼."""
    
    @staticmethod
    def to_domain(refresh_token_model: RefreshTokenModel) -> DomainRefreshToken:
        """ORM 모델을 도메인 객체로 변환."""
        return DomainRefreshToken(
            id=refresh_token_model.id,
            token=refresh_token_model.token,
            created_at=refresh_token_model.created_at,
            account_id=refresh_token_model.account_id
        )

    @staticmethod
    def to_model(domain_refresh_token: DomainRefreshToken) -> RefreshTokenModel:
        """도메인 객체를 ORM 모델로 변환."""
        return RefreshTokenModel(
            id=domain_refresh_token.id,
            token=domain_refresh_token.token,
            created_at=domain_refresh_token.created_at,
            account_id=domain_refresh_token.account_id
        )
