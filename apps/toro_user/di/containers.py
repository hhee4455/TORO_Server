from dependency_injector import containers, providers
from redis import Redis

from apps.toro_user.application.service.user_service import UserService
from apps.toro_user.infrastructure.orm.adapters.user_repository_impl import UserRepositoryImpl
from apps.toro_user.application.service.profile_service import ProfileService
from apps.toro_user.infrastructure.redis.find_user_repository import FindUserRepositoryImpl

class Container(containers.DeclarativeContainer):

    # Redis 클라이언트 설정
    redis_client = providers.Singleton(
        Redis,
        host='localhost',  # Redis 호스트
        port=6379,         # Redis 포트
        decode_responses=True  # 문자열로 응답 디코딩
    )

    # Repositories
    user_repository = providers.Factory(UserRepositoryImpl)
    find_user_repository = providers.Factory(
        FindUserRepositoryImpl,
        redis_client=redis_client
    )

    # Services
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
        find_user_repository=find_user_repository,
    )

    profile_service = providers.Factory(
        ProfileService,
        find_user_repository=find_user_repository,
        user_repository=user_repository
    )
