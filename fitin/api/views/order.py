from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from api.models import CartItem, Order, OrderItem


class SetOrder(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request: Request):
        user = request.user
        queryset = CartItem.objects.filter(cart__user=user)

        if len(CartItem.objects.filter(cart__user=user)):
            order = Order.objects.create(user=user)
            order_products = [OrderItem(order=order, product=i.product, quantity=i.quantity) for i in queryset]

            OrderItem.objects.bulk_create(order_products)
            queryset.delete()

            # send_email_task.delay('Заказ', 'Вы получили заказ', user.email)

            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)