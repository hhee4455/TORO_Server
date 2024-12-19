from django.urls import path
from apps.toro_user.interface.controllers.user import UserView
from apps.toro_user.interface.controllers.profile import ProfileView

urlpatterns = [
    path('user', UserView.as_view(), name='user'),
    path('profile', ProfileView.as_view(), name='profile'),
]
