from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Admin Blog Management (specific paths first)
    path('admin/', views.AdminBlogListView.as_view(), name='admin_blog_list'),
    path('admin/category/<slug:category_slug>/', views.AdminBlogListView.as_view(), name='admin_blog_by_category'),
    
    # Post CRUD
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Category Management
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/new/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('category/<slug:category_slug>/', views.PublicBlogListView.as_view(), name='post_list_by_category'),
    
    # Public Blog (generic paths last)
    path('', views.PublicBlogListView.as_view(), name='post_list'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]
