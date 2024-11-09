from rest_framework.generics import ListAPIView

from api.models import Category
from api.serializers import CategorySerializer


class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

