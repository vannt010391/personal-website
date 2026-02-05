from django import forms
from django.utils.text import slugify
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
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['parent'].queryset = KnowledgeEntry.objects.filter(user=self.user).order_by('title')
        if 'content' in self.fields:
            self.fields['content'].required = False
        # Make topic required
        self.fields['topic'].required = True

    def clean_topic(self):
        topic = self.cleaned_data.get('topic')
        if not topic:
            raise forms.ValidationError('Please select a topic for this entry')
        return topic

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        title = self.cleaned_data.get('title')

        if not slug and title:
            base_slug = slugify(title)
            slug = base_slug
            counter = 1
            while KnowledgeEntry.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

        return slug
    class Meta:
        model = KnowledgeEntry
        fields = ['title', 'slug', 'topic', 'parent', 'order', 'entry_type', 'status', 'content', 'summary', 'source_url', 'tags', 'is_favorite']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tiêu đề', 'id': 'id_title'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tự động tạo từ tiêu đề', 'id': 'id_slug'}),
            'topic': forms.Select(attrs={'class': 'form-select'}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'step': 1, 'placeholder': '0'}),
            'entry_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
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
