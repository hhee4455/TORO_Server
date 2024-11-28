from django.urls import path
from apps.toro_auth.interface.controllers.email_send import EmailRequestView
from apps.toro_auth.interface.controllers.email_check import CheckCodeView
from apps.toro_auth.interface.controllers.signup import SignupView

urlpatterns = [
    path('send-code', EmailRequestView.as_view(), name='send_code'),  # 이메일 인증 요청
    path('check-code', CheckCodeView.as_view(), name='check_code'),  # 인증 코드 검증
    path('signup', SignupView.as_view(), name='signup'), #회원가입 요청
]
