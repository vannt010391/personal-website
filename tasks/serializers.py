from rest_framework import serializers
from .models import Task, StudySession


class TaskSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'user', 'user_name', 'title', 'description',
            'task_type', 'priority', 'status', 'due_date',
            'completed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class StudySessionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = StudySession
        fields = [
            'id', 'user', 'user_name', 'subject', 'description',
            'duration_minutes', 'date', 'notes', 'created_at'
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
