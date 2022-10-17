from django.contrib.auth import login, logout
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from .models import User
from .serializers import CreateUserSerializer, LoginSerializer, ProfileSerializer, UpdatePasswordSerializer


class SignupView(CreateAPIView):
    serializer_class = CreateUserSerializer


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exeptions=True)
        login(request=request, user=serializer.save())
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=204)


class UpdatePasswordView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    def get_object(self) -> User:
        return self.request.user
