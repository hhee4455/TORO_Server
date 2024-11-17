# apps/toro_auth/interface/urls.py
from django.urls import path
from apps.toro_auth.interface.views.email_check import views

urlpatterns = [
    path('api/send-code/', views.EmailRequestView.as_view(), name='send_code'),
    path('api/check-code/', views.CheckCodeView.as_view(), name='check_code'),
]
