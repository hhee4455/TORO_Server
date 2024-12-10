from dependency_injector import containers, providers
from apps.toro_auth.application.service.signup_service import SignupService
from apps.toro_auth.application.service.login_service import LoginService
from apps.toro_auth.infrastructure.orm.repositories_impl.account_repository_impl import AccountRepositoryImpl
from apps.toro_auth.infrastructure.orm.repositories_impl.refresh_token_repository_impl import RefreshTokenRepositoryImpl

class Container(containers.DeclarativeContainer):
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