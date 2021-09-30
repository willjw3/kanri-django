from django.urls import path
from .views import (
    AllBoardsView,
    BoardCreateView,
    BoardDetailView, 
    TaskCreateView,
    TaskDetailView, 
    TaskDisplayView
)
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('boards/', AllBoardsView.as_view(), name='boards'),
    path('boards/#boardModal', BoardCreateView.as_view(), name='board-create'),
    path('boards/<int:board_id>/', BoardDetailView.as_view(), name='board-detail'),
    path('boards/<int:board_id>/task/<int:task_id>/', TaskDisplayView.as_view(), name='task-detail'),
    # path('boards/<int:pk>/#taskModal', TaskCreateView.as_view(), name='task-create'),
    
]