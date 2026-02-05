from django.contrib import admin
from .models import Topic, KnowledgeEntry, Resource

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'created_at']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(KnowledgeEntry)
class KnowledgeEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'topic', 'entry_type', 'status', 'is_favorite', 'created_at', 'updated_at']
    list_filter = ['entry_type', 'status', 'topic', 'is_favorite', 'created_at']
    search_fields = ['title', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'resource_type', 'status', 'rating', 'created_at']
    list_filter = ['resource_type', 'status', 'rating', 'topic']
    search_fields = ['title', 'author', 'notes']
    date_hierarchy = 'created_at'
