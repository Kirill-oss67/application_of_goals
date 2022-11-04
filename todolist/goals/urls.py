from django.urls import path
from goals import views

urlpatterns = [
    path("board/create", views.BoardCreateView.as_view(), name='create-board'),
    path("board/list", views.BoardListView.as_view(), name='boards-list'),
    path("board/<pk>", views.BoardView.as_view(), name='board-view'),

    path("goal/create", views.GoalCreateView.as_view(), name='create-goal'),
    path("goal/list", views.GoalListView.as_view(), name='goals-list'),
    path("goal/<pk>", views.GoalView.as_view(), name='goal-view'),

    path("goal_comment/create", views.GoalCommentCreateView.as_view(), name='create-comment'),
    path("goal_comment/list", views.GoalCommentListView.as_view(), name='comments-list'),
    path("goal_comment/<pk>", views.GoalCommentView.as_view(), name='comment-view'),

    path("goal_category/create", views.GoalCategoryCreateView.as_view(), name='create-category'),
    path("goal_category/list", views.GoalCategoryListView.as_view(), name='categories-list'),
    path("goal_category/<pk>", views.GoalCategoryView.as_view(), name='category-view'),

]
