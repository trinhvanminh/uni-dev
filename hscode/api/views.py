from hscode.models import Product
from .serializers import ProductSerializer
from rest_framework import filters, viewsets, permissions


class ProductList(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['$name',
                     '$heading__no',
                     '$subheading__no']
