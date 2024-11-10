from rest_framework import serializers

from api.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class CategoryForProduct(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()

    category = CategoryForProduct()

    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'price', 'characteristics', 'category']
