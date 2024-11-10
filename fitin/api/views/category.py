from django.core.cache import cache
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from api.models import Category
from api.serializers.category import CategorySerializer


class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        data = cache.get('categories')
        if data:
            return Response(data=data)

        return super().get(request, *args, **kwargs)

