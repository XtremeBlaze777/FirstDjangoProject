from django.urls import path
from . import views

app_name = 'friends'

urlpatterns = [
    path('', views.index, name='friendsHome'),
    path('search/', views.SearchResults, name='search_results')
]