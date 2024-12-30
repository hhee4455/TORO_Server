from django.urls import path
from apps.toro_auth.interface.controllers.email_send import EmailRequestView
from apps.toro_auth.interface.controllers.email_check import CheckCodeView
from apps.toro_auth.interface.controllers.signup import SignupView
from apps.toro_auth.interface.controllers.login import LoginView
from apps.toro_auth.interface.controllers.logout import LogoutView
from apps.toro_auth.interface.controllers.validate import ValidateView
from apps.toro_auth.interface.controllers.update_refresh_token import UpdateRefreshTokenView



urlpatterns = [
    path('send-code', EmailRequestView.as_view(), name='send_code'),  # 이메일 인증 요청
    path('check-code', CheckCodeView.as_view(), name='check_code'),  # 인증 코드 검증
    path('signup', SignupView.as_view(), name='signup'), #회원가입 요청
    path('login', LoginView.as_view(), name='login'), #로그인 요청
    path('logout', LogoutView.as_view(), name='logout'), #로그아웃 요청
    path('validate', ValidateView.as_view(), name='validate'), #토큰 검증
    path('update-refresh-token', UpdateRefreshTokenView.as_view(), name='update_refresh_token'), #토큰 갱신
]
