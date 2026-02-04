from django import forms
from .models import Topic, KnowledgeEntry, Resource


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'slug', 'description', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tên chủ đề', 'id': 'id_name'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tự động tạo từ tên', 'id': 'id_slug'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Mô tả'}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
        }
        help_texts = {
            'slug': 'Để trống để tự động tạo từ tên. VD: web-development',
        }


class KnowledgeEntryForm(forms.ModelForm):
    class Meta:
        model = KnowledgeEntry
        fields = ['title', 'slug', 'topic', 'entry_type', 'content', 'summary', 'source_url', 'tags', 'is_favorite']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tiêu đề', 'id': 'id_title'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tự động tạo từ tiêu đề', 'id': 'id_slug'}),
            'topic': forms.Select(attrs={'class': 'form-select'}),
            'entry_type': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 15, 'placeholder': 'Nội dung (hỗ trợ Markdown)'}),
            'summary': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Tóm tắt'}),
            'source_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
            'tags': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'python, django, web (phân cách bằng dấu phẩy)'}),
            'is_favorite': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        help_texts = {
            'slug': 'Để trống để tự động tạo từ tiêu đề. VD: web-development',
        }


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'resource_type', 'topic', 'url', 'author', 'status', 'notes', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tên tài nguyên'}),
            'resource_type': forms.Select(attrs={'class': 'form-select'}),
            'topic': forms.Select(attrs={'class': 'form-select'}),
            'url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
            'author': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tác giả'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5, 'placeholder': 'Ghi chú'}),
            'rating': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 5, 'placeholder': '1-5'}),
        }
