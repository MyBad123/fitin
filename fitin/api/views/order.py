import uuid

from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from yookassa import Configuration, Payment

from api.models import CartItem, Order, OrderItem
from api.tasks import send_email_task

Configuration.configure()


class SetOrder(APIView):
    permission_classes = [IsAuthenticated, ]

    def __init__(self, **kwargs):
        self.__user_id: None | int = None

        super().__init__(**kwargs)

    def __get_payment(self) -> str | None:
        """get status of payment for user from request"""

        payment_id = cache.get(f'user__{self.__user_id}')

        if payment_id is None:
            return payment_id

        return Payment.find_one(payment_id)

    def __get_sum(self) -> str:
        """get sum of user's items from cart"""

        items_sum = 0

        for i in CartItem.objects.filter(cart__user__id=self.__user_id):
            items_sum += i.quantity * i.product.price

        return f"{items_sum:.2f}"

    def hzpost(self, request: Request):
        user = request.user
        queryset = CartItem.objects.filter(cart__user=user)

        if len(CartItem.objects.filter(cart__user=user)):
            order = Order.objects.create(user=user)
            order_products = [OrderItem(order=order, product=i.product, quantity=i.quantity) for i in queryset]

            OrderItem.objects.bulk_create(order_products)
            queryset.delete()

            send_email_task.delay('Заказ', 'Вы получили заказ', user.email)

            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request: Request) -> Response:
        self.__user_id = request.user.id
        status_payment = self.__get_payment()

        if status_payment:
            pass

        items_sum = self.__get_sum()
        if items_sum == '0.00':
            return Response(data={'message': 'You have an empty cart'})

        idempotence_key = str(uuid.uuid4())
        payment = Payment.create({
            "amount": {
                "value": items_sum,
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://www.example.com/return_url"
            },
            "description": f"Заказ № {idempotence_key}"
        }, idempotence_key)

        cache.set(f'user__{self.__user_id}', payment.id)

        return Response(data={'pay_url': payment.confirmation.confirmation_url},
                        status=status.HTTP_201_CREATED)
