from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin

from api.models import CartItem
from api.serializers import CartItemSerializer


class CartView(CreateModelMixin, GenericAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        return queryset

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
