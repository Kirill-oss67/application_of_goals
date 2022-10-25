from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from .models import GoalCategory
from .serializers import GoalCreateSerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer
