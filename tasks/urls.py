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
    
    # List100 admin URLs
    path('list100/admin/', views.list100_admin, name='list100_admin'),
    path('list100/new/', views.List100ItemCreateView.as_view(), name='list100_create'),
    path('list100/<int:pk>/edit/', views.List100ItemUpdateView.as_view(), name='list100_update'),
    path('list100/<int:pk>/delete/', views.List100ItemDeleteView.as_view(), name='list100_delete'),
]
