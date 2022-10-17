from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from .serializers import CreateUserSerializer


class SignupView(CreateAPIView):
    serializer_class = CreateUserSerializer

