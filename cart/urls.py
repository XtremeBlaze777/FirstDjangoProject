from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
        path('cart-summary/', views.CartView.as_view(), name='cart-summary'),
        path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
        path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove-from-cart'),
        path("search/", views.SearchResultsView.as_view(), name="search_results"),
        path("course/<int:pk>/", views.CourseDescriptionView.as_view(), name="course_description"),
        ]
