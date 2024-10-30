# apps/toro_auth/infra/repositories/user_repository.py
from ..models.user_model import UserModel
from ...domain.entity.user import User

class UserRepository:
    """User 데이터를 관리하는 레포지토리"""

    def get_by_id(self, user_id) -> User:
        user_model = UserModel.objects.get(id=user_id)
        return user_model.to_entity()

    def save(self, user: User):
        user_model = UserModel.from_entity(user)
        user_model.save()
