from django.urls import path
from . import views

app_name = 'knowledge'

urlpatterns = [
    path('', views.KnowledgeEntryListView.as_view(), name='entry_list'),
    path('entry/new/', views.KnowledgeEntryCreateView.as_view(), name='entry_create'),
    path('entry/<slug:slug>/', views.KnowledgeEntryDetailView.as_view(), name='entry_detail'),
    path('entry/<slug:slug>/edit/', views.KnowledgeEntryUpdateView.as_view(), name='entry_update'),
    path('entry/<slug:slug>/delete/', views.KnowledgeEntryDeleteView.as_view(), name='entry_delete'),
    path('topics/', views.TopicListView.as_view(), name='topic_list'),
    path('topic/new/', views.TopicCreateView.as_view(), name='topic_create'),
    path('topic/<int:pk>/edit/', views.TopicUpdateView.as_view(), name='topic_update'),
    path('topic/<int:pk>/delete/', views.TopicDeleteView.as_view(), name='topic_delete'),
    path('resources/', views.ResourceListView.as_view(), name='resource_list'),
    path('resource/new/', views.ResourceCreateView.as_view(), name='resource_create'),
    path('resource/<int:pk>/edit/', views.ResourceUpdateView.as_view(), name='resource_update'),
    path('resource/<int:pk>/delete/', views.ResourceDeleteView.as_view(), name='resource_delete'),
]
