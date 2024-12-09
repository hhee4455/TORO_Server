from django.apps import AppConfig

class ToroAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.toro_auth'

    def ready(self):
        """Django 앱이 초기화된 후에 DI 컨테이너 초기화."""
        from src.infrastructure.toro_auth.containers import Container  # infra 컨테이너 가져오기
        container = Container()
        container.wire(modules=[
            "apps.toro_auth.interface.controllers.signup",  # 필요한 모듈 추가
            "apps.toro_auth.interface.controllers.login",
        ])
