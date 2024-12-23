from redis import Redis
from dependency_injector import containers, providers
from django.conf import settings  # settings 가져오기
from apps.toro_auth.application.service.signup_service import SignupService
from apps.toro_auth.application.service.login_service import LoginService
from apps.toro_auth.infrastructure.orm.adapters.account_repository_impl import AccountRepositoryImpl
from apps.toro_auth.infrastructure.redis.token_repository_impl import TokenRepositoryImpl
from apps.toro_auth.application.service.email_service import EmailService
from apps.toro_auth.application.service.logout_service import LogoutService

class Container(containers.DeclarativeContainer):
    # Redis 클라이언트 생성
    redis_client = providers.Factory(
        Redis,
        host="localhost",
        port=6379,
        db=0
    )

    account_repository = providers.Factory(AccountRepositoryImpl)
    token_repository = providers.Factory(
        TokenRepositoryImpl,
        redis_client=redis_client
    )

    signup_service = providers.Factory(
        SignupService,
        account_repository=account_repository,
    )

    login_service = providers.Factory(
        LoginService,
        account_repository=account_repository,
        token_repository=token_repository,
        secret_key=settings.SECRET_KEY,
    )

    # 이메일 서비스를 위한 컨테이너
    email_service = providers.Factory(
        EmailService,
        account_repository=account_repository
    )

    logout_service = providers.Factory(
        LogoutService,
        token_repository=token_repository
    )