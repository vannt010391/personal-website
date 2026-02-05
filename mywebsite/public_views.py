from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Post
from knowledge.models import KnowledgeEntry, Topic
from tasks.models import List100Item

def home(request):
    """Public homepage"""
    recent_posts = Post.objects.filter(status='published').order_by('-published_at')[:3]
    return render(request, 'public/home.html', {'recent_posts': recent_posts})

def about(request):
    """About me page"""
    return render(request, 'public/about.html')

def contact(request):
    """Contact page"""
    return render(request, 'public/contact.html')

def list_100(request):
    """List 100 page - public view"""
    items = List100Item.objects.all()
    stats = {
        'total': items.count(),
        'not_started': items.filter(status='not_started').count(),
        'in_progress': items.filter(status='in_progress').count(),
        'completed': items.filter(status='completed').count(),
    }
    return render(request, 'public/list_100.html', {
        'items': items,
        'stats': stats,
    })

def note_taking(request):
    """Note-taking public page - shows public knowledge entries"""
    # Get all topics with entry counts (only public entries)
    topics = Topic.objects.all()
    for topic in topics:
        topic.entries_count = KnowledgeEntry.objects.filter(topic=topic, status='public').count()
    
    # Filter by topic if selected
    selected_topic = None
    entries = KnowledgeEntry.objects.filter(status='public').select_related('topic').order_by('-updated_at')
    
    topic_slug = request.GET.get('topic')
    if topic_slug:
        try:
            selected_topic = Topic.objects.get(slug=topic_slug)
            entries = entries.filter(topic=selected_topic)
        except Topic.DoesNotExist:
            pass
    
    # Pagination
    paginator = Paginator(entries, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'public/note_taking.html', {
        'entries': page_obj,
        'topics': topics,
        'selected_topic': selected_topic,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    })

def admin_portal(request):
    """Admin portal dashboard"""
    if not request.user.is_authenticated:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.get_full_path())
    
    from blog.models import Category
    from tasks.models import Task, List100Item
    
    # Get counts for dashboard
    context = {
        'posts_count': Post.objects.count(),
        'categories_count': Category.objects.count(),
        'entries_count': KnowledgeEntry.objects.count(),
        'topics_count': Topic.objects.count(),
        'tasks_count': Task.objects.count(),
        'active_tasks': Task.objects.filter(status__in=['todo', 'in_progress']).count(),
        'list100_count': List100Item.objects.count(),
        'list100_completed': List100Item.objects.filter(status='completed').count(),
    }
    
    return render(request, 'admin_portal/dashboard.html', context)
