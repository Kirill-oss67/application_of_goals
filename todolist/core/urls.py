from django.urls import path
from .views import SignupView

urlpatterns = [
    path('gignup', SignupView.as_view(), name='signup')
]
