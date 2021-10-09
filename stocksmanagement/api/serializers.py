from rest_framework import serializers
from stocksmanagement.models import Stock, Ecus, BOM, Balance


class StockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stock
        fields = ['id',
                  'description',
                  'date',
                  'item_name',
                  'ecus_code',
                  'item_desciption',
                  'date',
                  'begin_quantity',
                  'begin_price',
                  'pr_purchase_quantity',
                  'pr_purchase_price',
                  'mr_production_quantity',
                  'mr_production_price',
                  'or_unplanned_quantity',
                  'or_unplanned_price',
                  'stock_transfer_quantity',
                  'stock_transfer_price',
                  'pi_issue_production_quantity',
                  'pi_issue_production_price',
                  'di_sale_issue_quantity',
                  'di_sale_issue_price',
                  'oi_unplanned_issue_quantity',
                  'oi_unplanned_issue_price',
                  'stock_transfer_issue_quantity',
                  'stock_transfer_issue_price']


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
