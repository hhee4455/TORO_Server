from django.urls import path
from src.interface.toro_auth.controllers.email_check import CheckCodeView
from src.interface.toro_auth.controllers.email_send import EmailRequestView
from src.interface.toro_auth.controllers.signup import SignupView
from src.interface.toro_auth.controllers.login import LoginView



urlpatterns = [
    path('send-code', EmailRequestView.as_view(), name='send_code'),  # 이메일 인증 요청
    path('check-code', CheckCodeView.as_view(), name='check_code'),  # 인증 코드 검증
    path('signup', SignupView.as_view(), name='signup'), #회원가입 요청
    path('login', LoginView.as_view(), name='login'), #로그인 요청
]
