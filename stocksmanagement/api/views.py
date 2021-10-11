from rest_framework import viewsets
from rest_framework import permissions
from stocksmanagement.models import BOM, Balance, Ecus, Stock
from .serializers import StockSerializer, EcusSerializer, BOMSerializer, BalanceSerializer


class StockViewSet(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        client = self.request.user
        queryset = Stock.objects.filter(client=client)

        description = self.request.query_params.get('description')
        if description is not None:
            queryset = queryset.filter(description__icontains=description)

        item_name = self.request.query_params.get('item_name')
        if item_name is not None:
            queryset = queryset.filter(item_name__icontains=item_name)

        return queryset


class EcusViewSet(viewsets.ModelViewSet):
    serializer_class = EcusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        client = self.request.user
        queryset = Ecus.objects.filter(client=client)

        type_code = self.request.query_params.get('type_code')
        if type_code is not None:
            queryset = queryset.filter(type_code__icontains=type_code)

        from_country = self.request.query_params.get('from_country')
        if from_country is not None:
            queryset = queryset.filter(from_country__icontains=from_country)

        return queryset


class BOMViewSet(viewsets.ModelViewSet):
    serializer_class = BOMSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        client = self.request.user
        queryset = BOM.objects.filter(client=client)

        ecus_code = self.request.query_params.get('ecus_code')
        if ecus_code is not None:
            queryset = queryset.filter(ecus_code__icontains=ecus_code)

        tp_code = self.request.query_params.get('tp_code')
        if tp_code is not None:
            queryset = queryset.filter(tp_code__icontains=tp_code)

        ecus = self.request.query_params.get('ecus')
        if ecus is not None:
            queryset = queryset.filter(ecus__icontains=ecus)

        return queryset


class BalanceViewSet(viewsets.ModelViewSet):
    serializer_class = BalanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        client = self.request.user
        queryset = Balance.objects.filter(client=client)

        ecus_code = self.request.query_params.get('ecus_code')
        if ecus_code is not None:
            queryset = queryset.filter(ecus_code__icontains=ecus_code)

        description = self.request.query_params.get('description')
        if description is not None:
            queryset = queryset.filter(description__icontains=description)

        return queryset
