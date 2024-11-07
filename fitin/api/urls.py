from django.urls import path

from .views import CategoryView, ProductsView, ProductView

urlpatterns = [
    path('lol/', CategoryView.as_view()),
    path('products/', ProductsView.as_view()),
    path('products/<int:pk>/', ProductView.as_view())
]