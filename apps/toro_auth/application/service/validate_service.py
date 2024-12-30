import jwt
import logging


class ValidateService:
    """토큰 유효성 검증 서비스."""

    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def validate_access_token(self, access_token: str) -> dict:
        """
        Access Token의 유효성을 검증
        """
        try:
            decoded_token = jwt.decode(access_token, self.secret_key, algorithms=["HS256"])
            if not isinstance(decoded_token, dict):
                raise ValueError("Decoded token is not valid")
            return {"is_valid": True, "data": decoded_token}
        except jwt.ExpiredSignatureError:
            logging.warning("Access token has expired")
            raise ValueError("Access token has expired")
        except jwt.InvalidTokenError:
            logging.error("Invalid access token")
            raise ValueError("Invalid access token")
