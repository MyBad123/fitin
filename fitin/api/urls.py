from django.urls import path

from .views import CategoryView, ProductsView, ProductView, CartView, SetOrder


urlpatterns = [
    path('lol/', CategoryView.as_view()),
    path('products/', ProductsView.as_view()),
    path('products/<int:pk>/', ProductView.as_view()),
    path('order/', SetOrder.as_view()),

    path('card/', CartView.as_view()),
    path('card/<int:pk>', CartView.as_view()),
]