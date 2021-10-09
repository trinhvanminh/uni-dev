from rest_framework import viewsets
from rest_framework import permissions
from stocksmanagement.models import Stock
from .serializers import StockSerializer


class StockViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Stock.objects.all().order_by('-date')
    serializer_class = StockSerializer
