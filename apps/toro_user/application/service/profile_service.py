from apps.toro_user.application.repositories.find_user_repository import FindUserRepository
from apps.toro_user.application.repositories.user_repository import UserRepository


class ProfileService:
    """
    사용자 관련 비즈니스 로직을 처리하는 서비스 클래스.
    """

    def __init__(self, find_user_repository: FindUserRepository, user_repository: UserRepository):
        self.find_user_repository = find_user_repository
        self.user_repository = user_repository

    def get_profile_picture(self, refresh_token: str) -> str:
        """
        리프레시 토큰으로부터 account_id를 가져와 해당 사용자의 프로필 사진을 반환.
        """
        try:
            # Redis에서 account_id 가져오기
            account_id = self.find_user_repository.get_account_id(refresh_token)
            
            # DB에서 해당 account_id로 사용자 정보 가져오기
            user = self.user_repository.find_by_account_id(account_id)
            if not user:
                raise ValueError(f"No user found for account_id: {account_id}")
            
            # 사용자 프로필 사진 반환
            return user.profile_picture
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve profile picture: {str(e)}") from e
