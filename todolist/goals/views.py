from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from .filters import GoalDateFilter
from .models import GoalCategory, Goal, GoalComment, Board
from .permission import BoardPermissions, GoalCategoryPermissions, GoalPermissions, CommentsPermissions
from .serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, GoalSerializer, \
    GoalCommentCreateSerializer, GoalCommentSerializer, BoardCreateSerializer, BoardSerializer, BoardListSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['board']
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.prefetch_related('board__participants').filter(
            board__participants__user_id=self.request.user.id, is_deleted=False
        )


class GoalCategoryCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.prefetch_related('board__participants').filter(
            board__participants__user_id=self.request.user.id, is_deleted=False
        )

    def perform_destroy(self, instance: GoalCategory):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            Goal.objects.filter(category=instance).update(status=Goal.Status.archived)
        return instance


class GoalCreateView(CreateAPIView):
    permission_classes = [GoalPermissions]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer
    filterset_class = GoalDateFilter
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter,
                       ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title", 'description']

    def get_queryset(self):
        return Goal.objects.select_related('user', 'category__board').filter(
            Q(category__board__participants__user_id=self.request.user.id) & ~Q(status=Goal.Status.archived)
        )


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [GoalPermissions]

    def get_queryset(self):
        return Goal.objects.select_related('user', 'category__board').filter(
            Q(category__board__participants__user_id=self.request.user.id) & ~Q(status=Goal.Status.archived)
        )

    def perform_destroy(self, instance: Goal):
        instance.Status = Goal.Status.archived
        instance.save(update_fields=('status',))
        return instance


class GoalCommentCreateView(CreateAPIView):
    permission_classes = [CommentsPermissions]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [CommentsPermissions]
    serializer_class = GoalCommentSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['goal']
    ordering = ["-created"]

    def get_queryset(self):
        return GoalComment.objects.select_related('goal__category__board', 'user').filter(
            goal__category__board__participants__user_id=self.request.user.id)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    permission_classes = [CommentsPermissions]
    serializer_class = GoalCommentSerializer

    def get_queryset(self):
        return GoalComment.objects.select_related('goal__category__board', 'user').filter(
            goal__category__board__participants__user_id=self.request.user.id)


class BoardCreateView(CreateAPIView):
    permission_classes = [BoardPermissions]
    serializer_class = BoardCreateSerializer


class BoardListView(ListAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardListSerializer
    ordering = ['title', ]

    def get_queryset(self):
        return Board.objects.prefetch_related('participants').filter(participants__user_id=self.request.user.id,
                                                                     is_deleted=False)


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.prefetch_related('participants').filter(participants__user_id=self.request.user.id,
                                                                     is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance
