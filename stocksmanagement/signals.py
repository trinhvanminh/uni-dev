from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Balance, Ecus, BOM


@receiver(pre_save, sender=Ecus)
def on_ecus_change(sender, instance, **kwargs):
    if instance.id is None:
        try:
            balance_query = Balance.objects.get(pk=instance.npl_sp_code)
            if instance.type_code == 'E21':
                balance_query.e21 += instance.total
            if instance.type_code == 'B13':
                balance_query.b13 += instance.total
            if instance.type_code == 'A42':
                balance_query.a42 += instance.total
            if instance.type_code == 'E52':
                balance_query.e52 += instance.total
            balance_query.save()
        except Balance.DoesNotExist:
            if not instance.npl_sp_code:
                return
            new_balance = Balance(client=instance.client,
                                  ecus_code=instance.npl_sp_code)
            if instance.type_code == 'E21':
                new_balance.e21 = instance.total
            if instance.type_code == 'B13':
                new_balance.b13 = instance.total
            if instance.type_code == 'A42':
                new_balance.a42 = instance.total
            if instance.type_code == 'E52':
                new_balance.e52 = instance.total
            new_balance.save()

    else:
        previous = Ecus.objects.get(id=instance.id)
        try:
            balance_query = Balance.objects.get(pk=instance.npl_sp_code)
            if instance.type_code == 'E21':
                balance_query.e21 = balance_query.e21 + instance.total - previous.total
            if instance.type_code == 'B13':
                balance_query.b13 += balance_query.b13 + instance.total - previous.total
            if instance.type_code == 'A42':
                balance_query.a42 += balance_query.a42 + instance.total - previous.total
            if instance.type_code == 'E52':
                balance_query.e52 += balance_query.e52 + instance.total - previous.total
            balance_query.save()
        except Balance.DoesNotExist:
            if not instance.npl_sp_code:
                return
            new_balance = Balance(client=instance.client,
                                  ecus_code=instance.npl_sp_code)
            if instance.type_code == 'E21':
                new_balance.e21 = instance.total
            if instance.type_code == 'B13':
                new_balance.b13 = instance.total
            if instance.type_code == 'A42':
                new_balance.a42 = instance.total
            if instance.type_code == 'E52':
                new_balance.e52 = instance.total
            new_balance.save()
        # if previous.field_a != instance.field_a:  # field will be updated
        #     pass  # write your code here


'''
'ERP code': BOM.rm_code
'Ecus code': Ecus.npl_sp_code, BOM.ecus_code
'''


@receiver(pre_save, sender=BOM)
def on_bom_change(sender, instance, **kwargs):
    if instance.id is None:
        try:
            balance_query = Balance.objects.get(pk=instance.ecus_code)
            balance_query.fg_stock += instance.finish_product_exchange
            balance_query.save()
        except Balance.DoesNotExist:
            if not instance.ecus_code:
                return
            new_balance = Balance(client=instance.client,
                                  ecus_code=instance.ecus_code)
            new_balance.fg_stock = instance.finish_product_exchange
            new_balance.save()

    else:
        previous = BOM.objects.get(id=instance.id)
        try:
            balance_query = Balance.objects.get(pk=instance.ecus_code)
            balance_query.fg_stock = balance_query.fg_stock + \
                instance.finish_product_exchange - previous.finish_product_exchange
            balance_query.save()
        except Balance.DoesNotExist:
            if not instance.ecus_code:
                return
            new_balance = Balance(client=instance.client,
                                  ecus_code=instance.ecus_code)
            if instance.type_code == 'E21':
                new_balance.e21 = instance.finish_product_exchange
            new_balance.save()
