import logging
from datetime import datetime, timedelta
import jwt

from apps.toro_auth.application.repositories.account_repository import AccountRepository
from apps.toro_auth.application.repositories.token_repository import TokenRepository

class UpdateRefreshTokenService:

    ACCESS_TOKEN_EXPIRATION_HOURS = 1
    REFRESH_TOKEN_EXPIRATION_DAYS = 7

    """Refresh Token 갱신 서비스."""
    def __init__(self, account_repository: AccountRepository, token_repository: TokenRepository, secret_key: str):
        self.account_repository = account_repository
        self.token_repository = token_repository
        self.secret_key = secret_key


    def refresh_access_token(self, refresh_token: str) -> str:
        """
        Refresh Token을 사용해 Access Token 갱신
        """
        logging.debug(f"Refreshing access token using refresh_token: {refresh_token}")

        account_id = self.token_repository.validate_refresh_token(refresh_token)
        if not account_id:
            logging.warning(f"Invalid or expired refresh token: {refresh_token}")
            raise ValueError("Invalid or expired refresh token")
        logging.debug(f"Validated refresh token. Account ID: {account_id}")

        account = self.account_repository.find_by_id(account_id)
        if not account:
            logging.error(f"Account not found for ID: {account_id}")
            raise ValueError("Account does not exist")
        logging.debug(f"Found account for ID: {account_id}. Email: {account.email}")

        access_token = self._create_access_token(account)
        logging.debug(f"Generated new access token for account ID: {account_id}")

        return access_token  # 문자열 값만 반환

    
    def _create_access_token(self, account) -> str:
        """
        Access Token 생성
        """
        payload = {
            "id": str(account.id),
            "email": account.email,
            "exp": datetime.utcnow() + timedelta(hours=self.ACCESS_TOKEN_EXPIRATION_HOURS)
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")