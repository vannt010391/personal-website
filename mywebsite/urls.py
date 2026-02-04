"""
URL configuration for mywebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import public_views

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Public Portal
    path('', public_views.home, name='home'),
    path('blog/', include('blog.urls', namespace='blog')),
    path('note-taking/', public_views.note_taking, name='note_taking'),
    path('list-100/', public_views.list_100, name='list_100'),
    path('about/', public_views.about, name='about'),
    path('contact/', public_views.contact, name='contact'),
    
    # Admin Portal
    path('portal/', public_views.admin_portal, name='admin_portal'),
    path('portal/tasks/', include('tasks.urls', namespace='tasks')),
    path('portal/knowledge/', include('knowledge.urls', namespace='knowledge')),
    
    # API
    path('api/', include('mywebsite.api_urls')),
    path('markdownx/', include('markdownx.urls')),
    
    # Auth
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
