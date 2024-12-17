from dependency_injector import containers, providers

from apps.toro_user.application.service.user_service import UserService 
from apps.toro_user.infrastructure.orm.repositories_impl.user_repository_impl import UserRepositoryImpl

class Container(containers.DeclarativeContainer):

    user_repository = providers.Factory(UserRepositoryImpl)

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )