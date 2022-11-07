from django.urls import path
from . import views

app_name = 'friends'

urlpatterns = [
    path('', views.index, name='friendsHome'),
    path('search/', views.SearchResultsView.as_view(), name='search_results')
]