from rest_framework import serializers, fields

from .models import Category, Product, CartItem


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'children']

    def get_children(self, obj):
        children_objs = Category.objects.filter(parent=obj)
        return CategorySerializer(children_objs, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    class CategoryForProduct(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()

    category = CategoryForProduct()

    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'price', 'characteristics', 'category']


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
