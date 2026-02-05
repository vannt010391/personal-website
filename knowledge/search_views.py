from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import KnowledgeEntry, Topic


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
            import time
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

        # Get all entries for sidebar (only root entries - no parent)
        all_entries = KnowledgeEntry.objects.filter(
            user=self.request.user,
            parent__isnull=True
        ).select_related('topic').prefetch_related('children').order_by('topic__name', 'order', 'title')

        context['query'] = query
        context['results'] = results
        context['result_count'] = len(results)
        context['query_time'] = query_time
        context['topics'] = Topic.objects.all()
        context['selected_topic'] = topic_id
        context['selected_type'] = entry_type
        context['all_entries'] = all_entries  # For sidebar navigation

        return context
