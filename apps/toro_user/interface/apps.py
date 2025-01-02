from django.apps import AppConfig


class ToroUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.toro_user.interface'
    label = 'toro_user'


    def ready(self):
        """Django 앱이 초기화된 후에 DI 컨테이너 초기화."""
        from apps.toro_user.di.containers import Container  
        container = Container()
        container.wire(modules=[
            'apps.toro_user.interface.controllers.user',
            'apps.toro_user.interface.controllers.profile'
        ])

        """앱 초기화 시 Signals 등록"""
        import apps.toro_user.infrastructure.orm.signals