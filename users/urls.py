from rest_framework.urls import path
from users.views import UserRegistration
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserRegistration.as_view(), name="register")
]