from rest_framework import serializers
from rest_framework import fields

from api.models import Cart, CartItem
from .product import ProductSerializer


class CartItemSerializer(serializers.Serializer):
    class NewCartItem(serializers.Serializer):
        id = serializers.IntegerField()
        quantity = serializers.IntegerField()

    product = ProductSerializer(read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    new_item = serializers.ListSerializer(child=NewCartItem(), write_only=True)

    def __init__(self, instance=None, data=fields.empty, **kwargs):
        self.__create_data: dict | None = None
        self.__update_data: dict | None = None
        self.__delete_data: dict | None = None

        super().__init__(instance, data, **kwargs)

    def validate(self, attrs):
        return super().validate(attrs)

    @property
    def data(self):
        # return data if you create/update/delete
        for return_data in [self.__create_data, self.__update_data, self.__delete_data]:
            if return_data:
                return return_data

        return_data = super().data

        return {
            'total_price': [],
            'total_': [],
            'objects': return_data
        }


class ChangeCartItemSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    def __init__(self, instance=None, data=fields.empty, **kwargs):
        self.user = kwargs.get('context').get('request').user
        self.cart = Cart.objects.get_or_create(user=self.user)[0]

        super().__init__(instance, data, **kwargs)


class CreateCartItemSerializer(ChangeCartItemSerializer):
    """serializer for create cart item"""

    def create(self, validated_data):
        return CartItem.objects.create(cart=self.cart, **validated_data)


class UpdateCartItemSerializer(ChangeCartItemSerializer):
    """serializer for update cart item"""

    def update(self, instance: CartItem, validated_data: dict):
        instance.product_id = validated_data['product']
        instance.quantity = validated_data['quantity']
        instance.save()

        return instance
