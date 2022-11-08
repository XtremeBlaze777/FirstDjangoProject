from django.urls import path

from . import views
from .views import *

app_name = 'cart'

urlpatterns = [
        path('cart-summary/', CartView.as_view(), name='cart-summary'),
        path('add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),
        path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove-from-cart'),
        path("search/", SearchResultsView.as_view(), name="search_results"),
        path("course/<int:pk>/", CourseDescriptionView.as_view(), name="course_description"),
]
