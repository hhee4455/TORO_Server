from injector import Module, Binder, singleton
from apps.toro_auth.application.repositories.account_repository import AccountRepository
from apps.toro_auth.application.repositories.refresh_token_repository import RefreshTokenRepository
from apps.toro_auth.infra.orm.repositories_impl.account_repository_impl import AccountRepositoryImpl
from apps.toro_auth.infra.orm.repositories_impl.refresh_token_repository_impl import RefreshTokenRepositoryImpl
from apps.toro_auth.application.service.signup_service import SignupService
from apps.toro_auth.interface.controllers.signup import SignupView

class AppModule(Module):
    """의존성 주입을 위한 모듈 클래스."""

    def configure(self, binder: Binder):
        binder.bind(AccountRepository, to=AccountRepositoryImpl, scope=singleton)
        binder.bind(RefreshTokenRepository, to=RefreshTokenRepositoryImpl, scope=singleton)
        binder.bind(SignupService, to=SignupService, scope=singleton)
        binder.bind(SignupView, to=SignupView)
