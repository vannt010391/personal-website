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

        # Get all entries for sidebar (only root entries - no parent)
        all_entries = KnowledgeEntry.objects.filter(
            user=self.request.user,
            parent__isnull=True
        ).select_related('topic').prefetch_related('children').order_by('topic__name', 'order', 'title')
        context['all_entries'] = all_entries
        context['current_slug'] = entry.slug

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

    def get_initial(self):
        initial = super().get_initial()
        topic_id = self.request.GET.get('topic')
        parent_id = self.request.GET.get('parent')

        if topic_id:
            initial['topic'] = topic_id
        if parent_id:
            initial['parent'] = parent_id
            try:
                parent_entry = KnowledgeEntry.objects.get(id=parent_id, user=self.request.user)
                if parent_entry.topic_id:
                    initial['topic'] = parent_entry.topic_id
            except KnowledgeEntry.DoesNotExist:
                pass

        return initial

    def get_success_url(self):
        # If creating a child page, redirect to parent page to see the new child
        if self.object.parent:
            return reverse_lazy('knowledge:entry_detail', kwargs={'slug': self.object.parent.slug})
        # Otherwise redirect to the newly created page
        return reverse_lazy('knowledge:entry_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()

        # Check if creating a child page
        parent_id = self.request.GET.get('parent')

        if parent_id:
            try:
                parent_entry = KnowledgeEntry.objects.get(id=parent_id, user=self.request.user)
                context['parent_entry'] = parent_entry

                # Get siblings (other children of the same parent, or same topic if no parent)
                if parent_entry.parent:
                    context['sidebar_entries'] = parent_entry.parent.children.exclude(id=parent_entry.id).order_by('order', 'title')
                else:
                    context['sidebar_entries'] = KnowledgeEntry.objects.filter(
                        user=self.request.user,
                        topic=parent_entry.topic,
                        parent__isnull=True
                    ).exclude(id=parent_entry.id).order_by('order', 'title')
            except KnowledgeEntry.DoesNotExist:
                context['parent_entry'] = None
                context['sidebar_entries'] = []
        else:
            selected_topic_id = self.request.GET.get('topic') or self.request.POST.get('topic')
            if selected_topic_id:
                context['selected_topic_id'] = str(selected_topic_id)
                context['sidebar_entries'] = KnowledgeEntry.objects.filter(
                    user=self.request.user,
                    topic_id=selected_topic_id,
                ).order_by('order', 'title')
            else:
                context['sidebar_entries'] = []

        # Get all entries for sidebar (only root entries - no parent)
        all_entries = KnowledgeEntry.objects.filter(
            user=self.request.user,
            parent__isnull=True
        ).select_related('topic').prefetch_related('children').order_by('topic__name', 'order', 'title')
        context['all_entries'] = all_entries

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        parent_id = self.request.GET.get('parent')
        if parent_id and form.instance.parent is None:
            try:
                parent_entry = KnowledgeEntry.objects.get(id=parent_id, user=self.request.user)
                form.instance.parent = parent_entry
                if form.instance.topic_id is None and parent_entry.topic_id:
                    form.instance.topic = parent_entry.topic
            except KnowledgeEntry.DoesNotExist:
                pass
        print(f"=== FORM VALID ===")
        print(f"Title: {form.cleaned_data.get('title')}")
        print(f"Parent: {form.cleaned_data.get('parent')}")
        print(f"Topic: {form.cleaned_data.get('topic')}")
        messages.success(self.request, 'Page created successfully!', extra_tags='success')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(f"=== FORM INVALID ===")
        print(f"Errors: {form.errors}")
        print(f"Data: {form.data}")
        # Add error message for topic field
        if 'topic' in form.errors:
            for error in form.errors['topic']:
                messages.error(self.request, f'Topic: {error}', extra_tags='error')
        # Add any other form errors
        for field, errors in form.errors.items():
            if field != 'topic':
                for error in errors:
                    messages.error(self.request, f'{field}: {error}', extra_tags='error')
        return super().form_invalid(form)


class KnowledgeEntryUpdateView(LoginRequiredMixin, UpdateView):
    model = KnowledgeEntry
    form_class = KnowledgeEntryForm
    template_name = 'knowledge/entry_form.html'

    def get_queryset(self):
        return KnowledgeEntry.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('knowledge:entry_detail', kwargs={'slug': self.object.slug})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Page updated successfully!', extra_tags='success')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        context['entry'] = self.object
        selected_topic_id = self.object.topic_id
        if selected_topic_id:
            context['selected_topic_id'] = str(selected_topic_id)
            context['sidebar_entries'] = KnowledgeEntry.objects.filter(
                user=self.request.user,
                topic_id=selected_topic_id,
            ).order_by('order', 'title')
        else:
            context['sidebar_entries'] = []

        if self.object.parent:
            context['sibling_pages'] = self.object.parent.children.exclude(id=self.object.id).order_by('order', 'title')
        else:
            context['sibling_pages'] = KnowledgeEntry.objects.filter(
                topic=self.object.topic,
                parent__isnull=True
            ).exclude(id=self.object.id).order_by('order', 'title')

        # Get all entries for sidebar (only root entries - no parent)
        all_entries = KnowledgeEntry.objects.filter(
            user=self.request.user,
            parent__isnull=True
        ).select_related('topic').prefetch_related('children').order_by('topic__name', 'order', 'title')
        context['all_entries'] = all_entries
        context['current_slug'] = self.object.slug

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
