from apps.toro_user.domain.entity.user import User
from apps.toro_user.infrastructure.orm.mapper.user_mapper import UserMapper
from apps.toro_user.infrastructure.orm.models.user_model import UserModel
from apps.toro_user.application.repositories.user_repository import UserRepository

class UserRepositoryImpl(UserRepository):
    """UserRepository 구현체: 이메일을 기준으로 사용자 조회."""

    def find_by_email(self, email: str) -> User:
        """이메일로 사용자를 조회하고 도메인 엔티티로 변환."""
        try:
            user_record = UserModel.objects.select_related("account").get(account__email=email)
            return UserMapper.to_entity(user_record)
        except UserModel.DoesNotExist:
            return None

    def find_by_account_id(self, account_id: str):
        """
        account_id를 사용해 사용자 정보를 가져오는 함수.
        """
        try:
            return UserModel.objects.get(account_id=account_id)
        except UserModel.DoesNotExist:
            return None