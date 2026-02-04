from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtopics')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class KnowledgeEntry(models.Model):
    TYPE_CHOICES = [
        ('note', 'Note'),
        ('research', 'Research'),
        ('article', 'Article'),
        ('reference', 'Reference'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='knowledge_entries')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, related_name='entries')
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        help_text="Parent page for hierarchical structure",
    )
    order = models.IntegerField(default=0, help_text="Ordering within a topic or parent page")
    entry_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='note')
    content = models.TextField()
    summary = models.TextField(max_length=500, blank=True)
    source_url = models.URLField(blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name_plural = "Knowledge Entries"

    def __str__(self):
        return self.title

class Resource(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ('book', 'Book'),
        ('video', 'Video'),
        ('course', 'Course'),
        ('website', 'Website'),
        ('paper', 'Paper'),
    ]

    STATUS_CHOICES = [
        ('to_read', 'To Read'),
        ('reading', 'Reading'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPE_CHOICES)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, related_name='resources')
    url = models.URLField(blank=True)
    author = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='to_read')
    notes = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True, help_text="Rating from 1 to 5")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
