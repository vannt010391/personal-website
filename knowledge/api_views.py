from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Topic, KnowledgeEntry, Resource
from .serializers import TopicSerializer, KnowledgeEntrySerializer, ResourceSerializer


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class KnowledgeEntryViewSet(viewsets.ModelViewSet):
    serializer_class = KnowledgeEntrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['entry_type', 'topic', 'is_favorite']
    search_fields = ['title', 'content', 'tags', 'summary']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']

    def get_queryset(self):
        return KnowledgeEntry.objects.filter(user=self.request.user)


class ResourceViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['resource_type', 'status', 'rating', 'topic']
    search_fields = ['title', 'author', 'notes']
    ordering_fields = ['created_at', 'updated_at', 'rating']
    ordering = ['-created_at']

    def get_queryset(self):
        return Resource.objects.filter(user=self.request.user)
