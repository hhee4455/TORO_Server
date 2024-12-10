from dependency_injector import containers, providers
from src.infrastructure.toro_auth.orm.repositories_impl.account_repository_impl import AccountRepositoryImpl
from src.application.toro_auth.service.login_service import LoginService

class Container(containers.DeclarativeContainer):
    """DI 컨테이너 정의"""
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.interface.toro_auth.controllers.login",  # DI가 필요한 모듈
            "src.interface.toro_auth.controllers.signup",
        ]
    )

    # 레포지토리 제공자
    account_repository = providers.Factory(AccountRepositoryImpl)

    # 서비스 제공자
    login_service = providers.Factory(
        LoginService,
        repository=account_repository,  # 주입할 레포지토리
    )
