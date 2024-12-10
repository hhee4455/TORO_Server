from django.apps import AppConfig

class ToroAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.interface.toro_auth'

    def ready(self):
        from src.di.settings import initialize_container
        """Django 앱 초기화 시 DI 컨테이너 초기화"""
        initialize_container()
