from django.apps import AppConfig

class ToroAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.toro_auth.interface'
    label = 'toro_auth'

    def ready(self):
        """Django 앱이 초기화된 후에 DI 컨테이너 초기화."""
        from apps.toro_auth.di.containers import Container  
        container = Container()
        container.wire(modules=[
            "apps.toro_auth.interface.controllers.signup",  
            "apps.toro_auth.interface.controllers.login",
            "apps.toro_auth.interface.controllers.email_send",
            "apps.toro_auth.interface.controllers.email_check",
            "apps.toro_auth.interface.controllers.logout",
            "apps.toro_auth.interface.controllers.validate",
            "apps.toro_auth.interface.controllers.update_refresh_token",
        ])
