from django.urls import path
from .views import (
    AllBoardsView,
    BoardCreateView
)
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('boards/', AllBoardsView.as_view(), name='boards'),
    path('boards/#boardModal', BoardCreateView.as_view(), name='board-create'),
    path('boards/<int:pk>/', BoardCreateView.as_view(), name='board-create'),
    
]