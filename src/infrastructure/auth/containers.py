from dependency_injector import containers, providers
from src.infrastructure.auth.orm.repositories_impl.account_repository_impl import AccountRepositoryImpl
from src.infrastructure.auth.orm.repositories_impl.refresh_token_repository_impl import RefreshTokenRepositoryImpl
from src.application.auth.service.signup_service import SignupService
from src.application.auth.service.login_service import LoginService

class Container(containers.DeclarativeContainer):
    """DI 컨테이너는 infra에 위치."""
    account_repository = providers.Factory(AccountRepositoryImpl)
    refresh_token_repository = providers.Factory(RefreshTokenRepositoryImpl)

    signup_service = providers.Factory(
        SignupService,
        account_repository=account_repository,
    )

    login_service = providers.Factory(
        LoginService,
        account_repository=account_repository,
        refresh_token_repository=refresh_token_repository
    )