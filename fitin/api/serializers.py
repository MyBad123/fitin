from rest_framework import serializers

from .models import Category, Product


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
