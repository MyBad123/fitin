from django.core.cache import cache
from rest_framework import serializers

from api.models import Category


class CustomListSerializer(serializers.ListSerializer):
    """
    class for work with list response

    in this place we must to set .data method
    for getting cache work
    """

    @property
    def data(self):
        data = super().data
        cache.set('categories', data)

        return data


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'children']
        list_serializer_class = CustomListSerializer

    def get_children(self, obj):
        children_objs = Category.objects.filter(parent=obj)
        return CategorySerializer(children_objs, many=True).data
