from hscode.models import Product
from .serializers import ProductSerializer
from rest_framework import filters, viewsets


class ProductList(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    filter_fields = ('name',
                     'heading',
                     'subheading')
