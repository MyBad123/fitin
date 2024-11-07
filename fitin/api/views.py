from rest_framework import generics
from rest_framework import viewsets
from rest_framework import views, request, response, status
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .serializers import CategorySerializer, ProductSerializer
from .tasks import send_email_task


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductsView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)

    filterset_fields = {
        'price': ['lte', 'gte']
    }

    ordering_fields = ['price', 'name']
    ordering = ['name']


class ProductView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        #user = self.request.user
        #Cart.objects.get_or_create(user=user)

        hz = super().get_queryset()
        return hz

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)


class SetOrder(views.APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request: request.Request):
        user = request.user
        queryset = CartItem.objects.filter(cart__user=user)

        if len(CartItem.objects.filter(cart__user=user)):
            order = Order.objects.create(user=user)
            order_products = [OrderItem(order=order, product=i.product, quantity=i.quantity) for i in queryset]

            OrderItem.objects.bulk_create(order_products)
            queryset.delete()

            # send_email_task.delay('Заказ', 'Вы получили заказ', user.email)

            return response.Response(status=status.HTTP_201_CREATED)

        return response.Response(status=status.HTTP_400_BAD_REQUEST)
