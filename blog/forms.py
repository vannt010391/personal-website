from django import forms
from .models import Post, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tên danh mục', 'id': 'id_name'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tự động tạo từ tên', 'id': 'id_slug'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Mô tả danh mục'}),
        }
        help_texts = {
            'slug': 'Để trống để tự động tạo từ tên. VD: web-development',
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'category', 'content', 'excerpt', 'status', 'published_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tiêu đề bài viết', 'id': 'id_title'}),
            'slug': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tự động tạo từ tiêu đề', 'id': 'id_slug'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 15, 'placeholder': 'Nội dung bài viết (hỗ trợ Markdown)'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Tóm tắt ngắn'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'published_at': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
        }
        help_texts = {
            'slug': 'Để trống để tự động tạo từ tiêu đề. VD: web-development',
        }
