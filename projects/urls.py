from django.urls import path
from .views import (
    AllBoardsView,
    BoardCreateView,
    BoardDetailView, 
    TaskCreateView,
    TaskDetailView, 
    TaskDisplayView,
    CommentCreateView, 
    TaskUpdateView,
    TaskDeleteView
)
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('boards/', AllBoardsView.as_view(), name='boards'),
    path('boards/#boardModal', BoardCreateView.as_view(), name='board-create'),
    path('boards/<int:board_id>/', BoardDetailView.as_view(), name='board-detail'),
    path('boards/<int:pk>/#taskModal', TaskCreateView.as_view(), name='task-create'),
    path('boards/<int:board_id>/task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('boards/comment/new', CommentCreateView.as_view(), name='comment-create'),
    path('boards/<int:board_id>/task/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('boards/<int:board_id>/task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    
]