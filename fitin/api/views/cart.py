from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.models import CartItem
from api.serializers.cart import (CartItemSerializer, UpdateCartItemSerializer,
                                  CreateCartItemSerializer)


class CartView(CreateModelMixin, DestroyModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(cart__user=user)

        return queryset

    def post(self, request, *args, **kwargs):
        self.serializer_class = CreateCartItemSerializer

        try:
            return super().create(request, *args, **kwargs)

        except IntegrityError:
            return Response(data={'error': 'This product is already in your shopping cart'},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        self.serializer_class = UpdateCartItemSerializer

        try:
            return super().update(request, *args, **kwargs)

        except IntegrityError:
            return Response(data={'error': 'This product is already in your shopping cart'},
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *, pk: int):
        self.get_queryset().filter(id=pk).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
