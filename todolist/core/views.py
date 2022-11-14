from django.contrib.auth import login, logout
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from .models import User
from .serializers import CreateUserSerializer, LoginSerializer, ProfileSerializer, UpdatePasswordSerializer


class SignupView(CreateAPIView):
    serializer_class = CreateUserSerializer
    """Регистрация пользователя """


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    """Авторизация пользователем """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return Response(ProfileSerializer(user).data)


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    """Просмотр данных юзера(возможен только авторизованным пользователям"""

    def get_object(self) -> User:
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=204)


class UpdatePasswordView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdatePasswordSerializer
    """Изменение пароля пользователя"""

    def get_object(self) -> User:
        return self.request.user
