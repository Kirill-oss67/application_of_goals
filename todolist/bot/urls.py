from django.urls import path
from bot import views

urlpatterns = [
    path("verify", views.VerificationView.as_view(), name='verify'),

]
