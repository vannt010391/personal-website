from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Post, Category
from .forms import PostForm, CategoryForm
import markdown
from django.utils import timezone


# Admin Blog Management - All posts with CRUD
class AdminBlogListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/admin_blog_list.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        queryset = Post.objects.all().select_related('author', 'category').order_by('-created_at')
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['total_posts'] = Post.objects.count()
        context['published_posts'] = Post.objects.filter(status='published').count()
        context['draft_posts'] = Post.objects.filter(status='draft').count()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['current_category'] = get_object_or_404(Category, slug=category_slug)
        return context


# Public Blog - Only published posts
class PublicBlogListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(status='published').select_related('author', 'category')
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['current_category'] = get_object_or_404(Category, slug=category_slug)
        return context


# Backward compatibility alias
PostListView = PublicBlogListView


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = Post.objects.select_related('author', 'category')
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['content_html'] = markdown.markdown(
            post.content,
            extensions=['extra', 'codehilite', 'toc']
        )
        return context


# Post CRUD Views
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.status == 'published' and not form.instance.published_at:
            form.instance.published_at = timezone.now()
        messages.success(self.request, 'Bài viết đã được tạo thành công!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        if form.instance.status == 'published' and not form.instance.published_at:
            form.instance.published_at = timezone.now()
        messages.success(self.request, 'Bài viết đã được cập nhật thành công!')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Bài viết đã được xóa!')
        return super().delete(request, *args, **kwargs)


# Category CRUD Views
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category_form.html'
    success_url = reverse_lazy('blog:category_list')

    def form_valid(self, form):
        messages.success(self.request, 'Danh mục đã được tạo thành công!')
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category_form.html'
    success_url = reverse_lazy('blog:category_list')

    def form_valid(self, form):
        messages.success(self.request, 'Danh mục đã được cập nhật!')
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'blog/category_confirm_delete.html'
    success_url = reverse_lazy('blog:category_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Danh mục đã được xóa!')
        return super().delete(request, *args, **kwargs)
