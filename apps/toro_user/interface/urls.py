from django.urls import path
from apps.toro_user.interface.controllers.user import UserView

urlpatterns = [
    path('user', UserView.as_view(), name='user'),  
]
