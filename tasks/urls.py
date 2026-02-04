from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.task_dashboard, name='dashboard'),
    path('list/', views.TaskListView.as_view(), name='task_list'),
    path('kanban/', views.task_kanban, name='task_kanban'),
    path('new/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('study-sessions/', views.StudySessionListView.as_view(), name='study_session_list'),
    path('study-session/new/', views.StudySessionCreateView.as_view(), name='study_session_create'),
    path('study-session/<int:pk>/edit/', views.StudySessionUpdateView.as_view(), name='study_session_update'),
    path('study-session/<int:pk>/delete/', views.StudySessionDeleteView.as_view(), name='study_session_delete'),
]
