from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Post
from .serializers import CategorySerializer, PostSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'author']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'updated_at', 'published_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        return queryset
