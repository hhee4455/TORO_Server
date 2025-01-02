from dependency_injector import containers, providers
from redis import Redis

from apps.toro_user.application.service.user_service import UserService
from apps.toro_user.infrastructure.orm.adapters.user_repository_impl import UserRepositoryImpl
from apps.toro_user.application.service.profile_service import ProfileService

class Container(containers.DeclarativeContainer):

    # Repositories
    user_repository = providers.Factory(UserRepositoryImpl)
    
    # Services
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

    profile_service = providers.Factory(
        ProfileService,
        user_repository=user_repository
    )
