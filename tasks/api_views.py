from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, StudySession
from .serializers import TaskSerializer, StudySessionSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'task_type', 'due_date']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority', 'created_at']
    ordering = ['due_date', '-priority']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class StudySessionViewSet(viewsets.ModelViewSet):
    serializer_class = StudySessionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['date']
    search_fields = ['subject', 'description', 'notes']
    ordering_fields = ['date', 'duration_minutes', 'created_at']
    ordering = ['-date']

    def get_queryset(self):
        return StudySession.objects.filter(user=self.request.user)
