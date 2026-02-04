from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from .models import KnowledgeEntry, Topic, Resource
from .forms import KnowledgeEntryForm, TopicForm, ResourceForm
import markdown
import re
import time


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
        if topic_id:
            return queryset.order_by('order', 'title')
        return queryset.order_by('topic__name', 'order', 'title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        return context


def extract_headings_from_html(html_content):
    """Extract headings from HTML content to generate TOC"""
    headings = []
    # Match h1, h2, h3, h4, h5, h6 tags
    pattern = r'<h([1-6]).*?id="([^"]*)".*?>([^<]+)</h[1-6]>'
    matches = re.finditer(pattern, html_content)
    
    for match in matches:
        level = int(match.group(1))
        heading_id = match.group(2) if match.group(2) else ''
        text = match.group(3)
        # Remove any HTML tags from text
        text = re.sub(r'<[^>]+>', '', text)
        headings.append({
            'level': level,
            'text': text.strip(),
            'id': heading_id or text.lower().replace(' ', '-')
        })
    
    return headings


class KnowledgeEntryDetailView(LoginRequiredMixin, DetailView):
    model = KnowledgeEntry
    template_name = 'knowledge/entry_detail.html'
    context_object_name = 'entry'

    def get_queryset(self):
        return KnowledgeEntry.objects.filter(user=self.request.user).select_related('topic')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry = self.get_object()
        
        # Use toc extension to generate IDs for headings
        content_html = markdown.markdown(
            entry.content,
            extensions=['extra', 'codehilite', 'toc']
        )
        context['content_html'] = content_html
        
        # Extract headings for TOC
        headings = extract_headings_from_html(content_html)
        context['toc_items'] = headings
        
        # Get related pages (siblings and children)
        if entry.parent:
            context['sibling_pages'] = entry.parent.children.exclude(id=entry.id).order_by('order', 'title')
        else:
            context['sibling_pages'] = KnowledgeEntry.objects.filter(
                topic=entry.topic,
                parent__isnull=True
            ).exclude(id=entry.id).order_by('order', 'title')
        
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

    def get_initial(self):
        initial = super().get_initial()
        topic_id = self.request.GET.get('topic')
        if topic_id:
            initial['topic'] = topic_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        selected_topic_id = self.request.GET.get('topic') or self.request.POST.get('topic')
        if selected_topic_id:
            context['selected_topic_id'] = str(selected_topic_id)
            context['sidebar_entries'] = KnowledgeEntry.objects.filter(
                user=self.request.user,
                topic_id=selected_topic_id,
            ).order_by('order', 'title')
        else:
            context['sidebar_entries'] = []
        return context

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        selected_topic_id = self.object.topic_id
        if selected_topic_id:
            context['selected_topic_id'] = str(selected_topic_id)
            context['sidebar_entries'] = KnowledgeEntry.objects.filter(
                user=self.request.user,
                topic_id=selected_topic_id,
            ).order_by('order', 'title')
        else:
            context['sidebar_entries'] = []
        return context


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


# Search View
class KnowledgeSearchView(LoginRequiredMixin, TemplateView):
    template_name = 'knowledge/search_results.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        topic_id = self.request.GET.get('topic')
        entry_type = self.request.GET.get('type')
        
        results = []
        query_time = 0
        
        if query:
            start_time = time.time()
            
            # Search in title, content, summary, tags
            search_filter = Q(
                user=self.request.user,
            ) & (
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(summary__icontains=query) |
                Q(tags__icontains=query)
            )
            
            results = KnowledgeEntry.objects.filter(search_filter).select_related('topic')
            
            # Apply additional filters
            if topic_id:
                results = results.filter(topic_id=topic_id)
            if entry_type:
                results = results.filter(entry_type=entry_type)
            
            results = results.order_by('-updated_at')
            query_time = time.time() - start_time
        
        context['query'] = query
        context['results'] = results
        context['result_count'] = len(results)
        context['query_time'] = query_time
        context['topics'] = Topic.objects.all()
        context['selected_topic'] = topic_id
        context['selected_type'] = entry_type
        
        return context

        return super().delete(request, *args, **kwargs)
