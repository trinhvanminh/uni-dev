from django.db.models import Sum, F, Avg
from rest_framework import permissions, status, viewsets
from rest_framework import views
from rest_framework.response import Response
from iob_demo.models import IOB, ItemsTakeIn, ItemsTakeOut

from .serializers import (
    IOBSerializer, ItemsTakeInSerializer, IOBDisplay, ItemsTakeOutSerializer)


class TakeInViewSet(viewsets.ModelViewSet):
    serializer_class = ItemsTakeInSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_queryset(self):
        queryset = ItemsTakeIn.objects.filter(client=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        # unit = serializer.get("email", None)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        kwargs = {
            'client': self.request.user
        }
        serializer.save(**kwargs)


class TakeOutViewSet(viewsets.ModelViewSet):
    serializer_class = ItemsTakeOutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = ItemsTakeOut.objects.filter(client=self.request.user)
        return queryset

    def perform_create(self, serializer):
        kwargs = {
            'client': self.request.user
        }
        serializer.save(**kwargs)


class IOBViewSet(viewsets.ModelViewSet):
    serializer_class = IOBSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = IOB.objects.filter(client=self.request.user)
        return queryset


class TestTing(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        queryset = IOB.objects.filter(
            client=self.request.user).order_by('-date')
        queryset = IOB.objects.filter(client=self.request.user).values(
            'code', 'unit').annotate(take_in=Sum(F('take_ins__take_in')), take_out=Sum(F('take_outs__take_out')), price=Avg('price'))
        serializer = IOBDisplay(queryset, many=True)
        return Response(serializer.data)
