from django.contrib import admin
from .models import Task, StudySession

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'task_type', 'priority', 'status', 'due_date', 'created_at']
    list_filter = ['status', 'priority', 'task_type', 'due_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ['subject', 'user', 'date', 'duration_minutes', 'created_at']
    list_filter = ['date']
    search_fields = ['subject', 'description', 'notes']
    date_hierarchy = 'date'
