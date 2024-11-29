from apps.toro_auth.domain.entity.refresh_token import RefreshToken
from apps.toro_auth.application.repositories.refresh_token_repository import RefreshTokenRepository
from apps.toro_auth.infra.orm.models.refresh_token_model import RefreshTokenModel
from typing import Optional

class RefreshTokenRepositoryImpl(RefreshTokenRepository):
    def save(self, refresh_token: RefreshToken) -> None:
        """
        리프레시 토큰을 저장합니다.
        
        Args:
            refresh_token (RefreshToken): 리프레시 토큰 객체
        """
        refresh_token_model = RefreshTokenModel(
            id=refresh_token.id,
            token=refresh_token.token,
            created_at=refresh_token.created_at,
            account_id=refresh_token.account_id
        )
        refresh_token_model.save()

    def create(self, token: str, account_id: str) -> RefreshToken:
        """
        새로운 리프레시 토큰을 생성하여 저장합니다.
        
        Args:
            token (str): 리프레시 토큰 값
            account_id (str): 연결된 사용자 ID
        
        Returns:
            RefreshToken: 생성된 리프레시 토큰 객체
        """
        refresh_token_model = RefreshTokenModel.objects.create(
            token=token,
            account_id=account_id
        )
        return RefreshToken(
            id=refresh_token_model.id,
            token=refresh_token_model.token,
            created_at=refresh_token_model.created_at,
            account_id=refresh_token_model.account_id
        )

    def find_by_token(self, token: str) -> Optional[RefreshToken]:
        """
        리프레시 토큰을 통해 해당 토큰을 찾습니다.
        
        Args:
            token (str): 리프레시 토큰
        
        Returns:
            Optional[RefreshToken]: 리프레시 토큰 객체 또는 None
        """
        try:
            refresh_token_model = RefreshTokenModel.objects.get(token=token)
            return RefreshToken(
                id=refresh_token_model.id,
                token=refresh_token_model.token,
                created_at=refresh_token_model.created_at,
                account_id=refresh_token_model.account_id
            )
        except RefreshTokenModel.DoesNotExist:
            return None
