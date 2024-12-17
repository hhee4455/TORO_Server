from redis import Redis
from dependency_injector import containers, providers
from django.conf import settings  # settings 가져오기
from apps.toro_auth.application.service.signup_service import SignupService
from apps.toro_auth.application.service.login_service import LoginService
from apps.toro_auth.infrastructure.orm.repositories_impl.account_repository_impl import AccountRepositoryImpl
from apps.toro_auth.infrastructure.redis.refresh_token_manager import RefreshTokenRepositoryImpl
from apps.toro_auth.application.service.email_service import EmailService

class Container(containers.DeclarativeContainer):
    # Redis 클라이언트 생성
    redis_client = providers.Factory(
        Redis,
        host="localhost",
        port=6379,
        db=0
    )

    account_repository = providers.Factory(AccountRepositoryImpl)
    refresh_token_repository = providers.Factory(
        RefreshTokenRepositoryImpl,
        redis_client=redis_client
    )

    signup_service = providers.Factory(
        SignupService,
        account_repository=account_repository,
    )

    login_service = providers.Factory(
        LoginService,
        account_repository=account_repository,
        refresh_token_repository=refresh_token_repository,
        secret_key=settings.SECRET_KEY,
    )

    # 이메일 서비스를 위한 컨테이너
    email_service = providers.Factory(
        EmailService,
        account_repository=account_repository
    )
