from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Task, StudySession
from .forms import TaskForm, StudySessionForm
from datetime import date
from django.utils import timezone


@login_required
def task_dashboard(request):
    today = date.today()
    tasks = Task.objects.filter(user=request.user)

    context = {
        'today_tasks': tasks.filter(due_date=today).exclude(status='completed'),
        'overdue_tasks': tasks.filter(due_date__lt=today).exclude(status='completed'),
        'pending_tasks': tasks.filter(status='pending').order_by('due_date')[:5],
        'in_progress_tasks': tasks.filter(status='in_progress'),
        'recent_sessions': StudySession.objects.filter(user=request.user).order_by('-date')[:5],
    }
    return render(request, 'tasks/dashboard.html', context)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by('due_date', '-priority')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()
        return context


@login_required
def task_kanban(request):
    """Kanban board view for tasks"""
    tasks = Task.objects.filter(user=request.user)
    today = date.today()

    context = {
        'pending_tasks': tasks.filter(status='pending').order_by('-priority', 'due_date'),
        'in_progress_tasks': tasks.filter(status='in_progress').order_by('-priority', 'due_date'),
        'completed_tasks': tasks.filter(status='completed').order_by('-completed_at')[:20],  # Limit completed to 20
        'today': today,
    }
    return render(request, 'tasks/task_kanban.html', context)


class StudySessionListView(LoginRequiredMixin, ListView):
    model = StudySession
    template_name = 'tasks/study_session_list.html'
    context_object_name = 'sessions'
    paginate_by = 20

    def get_queryset(self):
        return StudySession.objects.filter(user=self.request.user).order_by('-date')


# Task CRUD Views
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Công việc đã được tạo thành công!')
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def form_valid(self, form):
        if form.instance.status == 'completed' and not form.instance.completed_at:
            form.instance.completed_at = timezone.now()
        messages.success(self.request, 'Công việc đã được cập nhật!')
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Công việc đã được xóa!')
        return super().delete(request, *args, **kwargs)


# StudySession CRUD Views
class StudySessionCreateView(LoginRequiredMixin, CreateView):
    model = StudySession
    form_class = StudySessionForm
    template_name = 'tasks/study_session_form.html'
    success_url = reverse_lazy('tasks:study_session_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Phiên học đã được tạo thành công!')
        return super().form_valid(form)


class StudySessionUpdateView(LoginRequiredMixin, UpdateView):
    model = StudySession
    form_class = StudySessionForm
    template_name = 'tasks/study_session_form.html'
    success_url = reverse_lazy('tasks:study_session_list')

    def get_queryset(self):
        return StudySession.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Phiên học đã được cập nhật!')
        return super().form_valid(form)


class StudySessionDeleteView(LoginRequiredMixin, DeleteView):
    model = StudySession
    template_name = 'tasks/study_session_confirm_delete.html'
    success_url = reverse_lazy('tasks:study_session_list')

    def get_queryset(self):
        return StudySession.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Phiên học đã được xóa!')
        return super().delete(request, *args, **kwargs)
