from typing import Any
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.request import Request

from users.serializers import UserSerializer

User = get_user_model()


class UserRegistration(generics.CreateAPIView):
    """
    Эндпоинт для регистрации нового пользователя.
    Принимает `login` и `password` в теле запроса и создаёт нового пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        login = request.data.get("login")
        password = request.data.get("password")

        if not login or not password:
            return Response(
                {"error": "login and password required"}, status=400
            )

        try:
            user = User(login=login)
            user.set_password(password)
            user.save()
            return Response({"message": "User created"}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)




