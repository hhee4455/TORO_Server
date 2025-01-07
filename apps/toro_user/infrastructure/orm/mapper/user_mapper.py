from apps.toro_user.domain.entity.user import User
from apps.toro_user.infrastructure.orm.models.user_model import UserModel
from apps.toro_auth.infrastructure.orm.models.account_model import AccountModel

class UserMapper:
    """ User 모델과 도메인 엔티티 간 변환 """

    @staticmethod
    def to_entity(user_model: UserModel) -> User:
        """ ORM 모델 -> 도메인 엔티티 변환 """
        return User(
            id=user_model.id,
            nickname=user_model.nickname,
            profile_picture=user_model.profile_picture,
            bio=user_model.bio,
            is_public=user_model.is_public,
            last_seen=user_model.last_seen,
            follower_count=user_model.follower_count,
            is_active=user_model.is_active,
        )

    @staticmethod
    def from_entity(user: User) -> UserModel:
        """ 도메인 엔티티 -> ORM 모델 변환 """
        account_instance = AccountModel.objects.get(id=user.account_id) if user.account_id else None
        return UserModel(
            id=user.id,
            nickname=user.nickname,
            profile_picture=user.profile_picture,
            bio=user.bio,
            is_public=user.is_public,
            last_seen=user.last_seen,
            follower_count=user.follower_count,
            is_active=user.is_active,
            account=account_instance,
        )