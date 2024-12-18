from dependency_injector import containers, providers

from apps.toro_user.application.service.detail_service import DetailService 
from apps.toro_user.infrastructure.orm.repositories_impl.detail_repository_impl import DetailRepositoryImpl

from apps.toro_user.application.service.profile_service import ProfileService
from apps.toro_user.infrastructure.redis.user_redis import RedisRepositoryImpl
class Container(containers.DeclarativeContainer):

    detail_repository = providers.Factory(DetailRepositoryImpl)
    profile_repository = providers.Factory(RedisRepositoryImpl)

    detail_service = providers.Factory(
        DetailService,
        detail_repository=detail_repository,
    )

    profile_service = providers.Factory(
        ProfileService,
        profile_repository=profile_repository,
    )

