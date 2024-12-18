from apps.toro_user.domain.entity.user import User
from apps.toro_user.infrastructure.orm.mapper.user_mapper import UserMapper
from apps.toro_user.infrastructure.orm.models.user_model import UserModel
from apps.toro_user.application.repositories.detail_repository import DetailRepository

class DetailRepositoryImpl(DetailRepository):
    """UserRepository 구현체: 이메일을 기준으로 사용자 조회."""

    def find_by_email(self, email: str) -> User:
        """이메일로 사용자를 조회하고 도메인 엔티티로 변환."""
        try:
            user_record = UserModel.objects.select_related("account").get(account__email=email)
            return UserMapper.to_entity(user_record)
        except UserModel.DoesNotExist:
            return None
