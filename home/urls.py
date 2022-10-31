from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('subject/<str:subject>', views.subject, name='subject'),
    path('subject/<str:subject>/course/<int:courseNum>', views.course, name='course')
]
