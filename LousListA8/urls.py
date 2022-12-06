"""LousListA8 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('', include('home.urls')),
    path('', include('cart.urls')),
    path('', include('schedule.urls')),
    path('friends/', include('friends.urls')),
    path('about/', TemplateView.as_view(template_name="about.html")),
    path('admin/', admin.site.urls),
    path('login/', TemplateView.as_view(template_name="login.html")),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
    path('profile/', TemplateView.as_view(template_name="profile.html")),
]
urlpatterns += staticfiles_urlpatterns()
