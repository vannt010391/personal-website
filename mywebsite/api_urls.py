from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from blog.api_views import CategoryViewSet, PostViewSet
from tasks.api_views import TaskViewSet, StudySessionViewSet
from knowledge.api_views import TopicViewSet, KnowledgeEntryViewSet, ResourceViewSet

router = DefaultRouter()

# Blog API endpoints
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'posts', PostViewSet, basename='post')

# Tasks API endpoints
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'study-sessions', StudySessionViewSet, basename='studysession')

# Knowledge API endpoints
router.register(r'topics', TopicViewSet, basename='topic')
router.register(r'knowledge-entries', KnowledgeEntryViewSet, basename='knowledgeentry')
router.register(r'resources', ResourceViewSet, basename='resource')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', obtain_auth_token, name='api-token-auth'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]
