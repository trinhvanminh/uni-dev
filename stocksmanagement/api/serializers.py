from rest_framework import serializers
from stocksmanagement.models import Stock, Ecus, BOM, Balance


class IOBSerializer(serializers.ModelSerializer):
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(IOBSerializer, self).get_field_names(
            declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class StockSerializer(IOBSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
        extra_fields = ['get_beginning_amount', 'get_pr_purchase_amount',
                        'get_mr_production_amount',
                        'get_or_unplanned_amount',
                        'get_stock_transfer_amount',
                        'get_pi_issue_production_amount',
                        'get_di_sale_issue_amount',
                        'get_oi_unplanned_issue_amount',
                        'get_stock_transfer_amount',
                        'get_ending_quantity', ]


# class EcusSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Ecus
#         fields = ['url', 'username', 'email', 'groups']


# class BOMSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = BOM
#         fields = ['url', 'username', 'email', 'groups']


# class BalanceSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Balance
#         fields = ['url', 'username', 'email', 'groups']
