from django import forms
from .models import Task, StudySession


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'task_type', 'priority', 'status', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tên công việc'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Mô tả chi tiết'}),
            'task_type': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }


class StudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ['subject', 'description', 'duration_minutes', 'date', 'notes']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Môn học / Chủ đề'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Mô tả'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Phút'}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5, 'placeholder': 'Ghi chú'}),
        }
