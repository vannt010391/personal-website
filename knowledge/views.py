from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import KnowledgeEntry, Topic, Resource
from .forms import KnowledgeEntryForm, TopicForm, ResourceForm
import markdown


class KnowledgeEntryListView(LoginRequiredMixin, ListView):
    model = KnowledgeEntry
    template_name = 'knowledge/entry_list.html'
    context_object_name = 'entries'
    paginate_by = 20

    def get_queryset(self):
        queryset = KnowledgeEntry.objects.filter(user=self.request.user).select_related('topic')
        topic_id = self.request.GET.get('topic')
        entry_type = self.request.GET.get('type')
        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)
        if entry_type:
            queryset = queryset.filter(entry_type=entry_type)
        return queryset.order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        return context


class KnowledgeEntryDetailView(LoginRequiredMixin, DetailView):
    model = KnowledgeEntry
    template_name = 'knowledge/entry_detail.html'
    context_object_name = 'entry'

    def get_queryset(self):
        return KnowledgeEntry.objects.filter(user=self.request.user).select_related('topic')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry = self.get_object()
        context['content_html'] = markdown.markdown(
            entry.content,
            extensions=['extra', 'codehilite', 'toc']
        )
        return context


class ResourceListView(LoginRequiredMixin, ListView):
    model = Resource
    template_name = 'knowledge/resource_list.html'
    context_object_name = 'resources'
    paginate_by = 20

    def get_queryset(self):
        queryset = Resource.objects.filter(user=self.request.user).select_related('topic')
        status = self.request.GET.get('status')
        resource_type = self.request.GET.get('type')
        if status:
            queryset = queryset.filter(status=status)
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        return context


# KnowledgeEntry CRUD Views
class KnowledgeEntryCreateView(LoginRequiredMixin, CreateView):
    model = KnowledgeEntry
    form_class = KnowledgeEntryForm
    template_name = 'knowledge/entry_form.html'
    success_url = reverse_lazy('knowledge:entry_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Entry đã được tạo thành công!')
        return super().form_valid(form)


class KnowledgeEntryUpdateView(LoginRequiredMixin, UpdateView):
    model = KnowledgeEntry
    form_class = KnowledgeEntryForm
    template_name = 'knowledge/entry_form.html'

    def get_queryset(self):
        return KnowledgeEntry.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('knowledge:entry_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        messages.success(self.request, 'Entry đã được cập nhật!')
        return super().form_valid(form)


class KnowledgeEntryDeleteView(LoginRequiredMixin, DeleteView):
    model = KnowledgeEntry
    template_name = 'knowledge/entry_confirm_delete.html'
    success_url = reverse_lazy('knowledge:entry_list')

    def get_queryset(self):
        return KnowledgeEntry.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Entry đã được xóa!')
        return super().delete(request, *args, **kwargs)


# Topic CRUD Views
class TopicListView(LoginRequiredMixin, ListView):
    model = Topic
    template_name = 'knowledge/topic_list.html'
    context_object_name = 'topics'


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'knowledge/topic_form.html'
    success_url = reverse_lazy('knowledge:topic_list')

    def form_valid(self, form):
        messages.success(self.request, 'Chủ đề đã được tạo!')
        return super().form_valid(form)


class TopicUpdateView(LoginRequiredMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = 'knowledge/topic_form.html'
    success_url = reverse_lazy('knowledge:topic_list')

    def form_valid(self, form):
        messages.success(self.request, 'Chủ đề đã được cập nhật!')
        return super().form_valid(form)


class TopicDeleteView(LoginRequiredMixin, DeleteView):
    model = Topic
    template_name = 'knowledge/topic_confirm_delete.html'
    success_url = reverse_lazy('knowledge:topic_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Chủ đề đã được xóa!')
        return super().delete(request, *args, **kwargs)


# Resource CRUD Views
class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'knowledge/resource_form.html'
    success_url = reverse_lazy('knowledge:resource_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Tài nguyên đã được tạo!')
        return super().form_valid(form)


class ResourceUpdateView(LoginRequiredMixin, UpdateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'knowledge/resource_form.html'
    success_url = reverse_lazy('knowledge:resource_list')

    def get_queryset(self):
        return Resource.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Tài nguyên đã được cập nhật!')
        return super().form_valid(form)


class ResourceDeleteView(LoginRequiredMixin, DeleteView):
    model = Resource
    template_name = 'knowledge/resource_confirm_delete.html'
    success_url = reverse_lazy('knowledge:resource_list')

    def get_queryset(self):
        return Resource.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Tài nguyên đã được xóa!')
        return super().delete(request, *args, **kwargs)
