from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/new/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('category/<slug:category_slug>/', views.PostListView.as_view(), name='post_list_by_category'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]
