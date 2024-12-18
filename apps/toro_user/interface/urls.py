from django.urls import path
from apps.toro_user.interface.controllers.detail import DetailView
from apps.toro_user.interface.controllers.profile import ProfileImageView

urlpatterns = [
    path('detail', DetailView.as_view(), name='detail'),  
    path("profile", ProfileImageView.as_view(), name="profile"),
]
