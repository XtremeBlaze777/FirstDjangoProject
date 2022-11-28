from django.urls import path, re_path

from . import views

app_name = 'schedule'

urlpatterns = [
        path('schedule-summary/', views.schedule_view, name='schedule_view'),
        path('friend-schedule-summary/<user_id>', views.friend_schedule_view, name='friend_schedule_view'),
        ]
