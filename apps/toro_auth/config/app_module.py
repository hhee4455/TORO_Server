from injector import inject, Module, singleton
from apps.toro_auth.application.repositories.account_repository import AccountRepository
from apps.toro_auth.application.repositories.refresh_token_repository import RefreshTokenRepository
from apps.toro_auth.infra.orm.repositories_impl.account_repository_impl import AccountRepositoryImpl
from apps.toro_auth.infra.orm.repositories_impl.refresh_token_repository_impl import RefreshTokenRepositoryImpl

class AppModule(Module):
    """
    의존성 주입을 위한 모듈 클래스.
    """
    def configure(self, binder):
        """
        의존성 주입 설정 메서드.

        Args:
            binder (Binder): 의존성 주입 설정 객체
        """
        binder.bind(AccountRepository, to=AccountRepositoryImpl, scope=singleton)
        binder.bind(RefreshTokenRepository, to=RefreshTokenRepositoryImpl, scope=singleton)