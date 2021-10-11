from rest_framework import viewsets
from rest_framework import permissions
from stocksmanagement.models import Stock
from .serializers import StockSerializer


class StockViewSet(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        client = self.request.user
        return Stock.objects.filter(client=client)
