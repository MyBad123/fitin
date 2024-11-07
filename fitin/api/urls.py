from django.urls import path
from rest_framework import routers

from .views import CategoryView, ProductsView, ProductView, CartView

router = routers.DefaultRouter()
router.register(r'card', CartView)


urlpatterns = [
    path('lol/', CategoryView.as_view()),
    path('products/', ProductsView.as_view()),
    path('products/<int:pk>/', ProductView.as_view()),

] + router.urls