import jwt
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


from apps.toro_user.application.repositories.user_repository import UserRepository


class ProfileService:
    """
    사용자 관련 비즈니스 로직을 처리하는 서비스 클래스.
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_account_id_from_access_token(self, access_token: str) -> str:
        """
        Access Token에서 account_id를 가져오는 함수.
        """
        try:
            decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
            account_id = decoded_token.get("id")  # Access Token의 "id" 필드가 account_id로 사용됨
            if not account_id:
                raise ValueError("Account ID not found in access token")
            return account_id
        except ExpiredSignatureError:
            raise ValueError("Access token has expired")
        except InvalidTokenError:
            raise ValueError("Invalid access token")
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve account_id from access token: {str(e)}") from e
        
    def get_profile(self, token: str) -> dict:
        """
        사용자 프로필 정보를 조회하는 함수.
        """
        account_id = self.get_account_id_from_access_token(token)

        userprofile = self.user_repository.find_by_account_id(account_id)
        if not userprofile:
            raise ValueError("User not found")
        
        # 필요한 정보를 포함한 사용자 프로필 반환
        return {
            "profile_picture": userprofile.profile_picture,
        }
