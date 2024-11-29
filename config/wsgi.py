import os
from django.core.wsgi import get_wsgi_application

# 프로젝트의 settings.py 파일 경로 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
