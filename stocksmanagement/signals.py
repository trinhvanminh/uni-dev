from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Balance, Ecus, BOM, Stock


@receiver(pre_save, sender=Ecus)
def on_ecus_change(sender, instance, **kwargs):
    if instance.id is None:
        try:
            if instance.npl_sp_code:
                balance_query = Balance.objects.get(
                    client=instance.client, ecus_code=instance.npl_sp_code)
                if instance.total:
                    if instance.type_code == 'E21':
                        if balance_query.e21:
                            balance_query.e21 += instance.total
                        else:
                            balance_query.e21 = instance.total
                    if instance.type_code == 'B13':
                        if balance_query.b13:
                            balance_query.b13 += instance.total
                        else:
                            balance_query.b13 = instance.total
                    if instance.type_code == 'A42':
                        if balance_query.a42:
                            balance_query.a42 += instance.total
                        else:
                            balance_query.a42 = instance.total
                    if instance.type_code == 'E52':
                        if balance_query.e52:
                            balance_query.e52 += instance.total
                        else:
                            balance_query.e52 = instance.total
                balance_query.save()
                return

        except Balance.DoesNotExist:
            if instance.npl_sp_code:
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
                return

    else:
        previous = Ecus.objects.get(id=instance.id)
        try:
            if instance.npl_sp_code:
                balance_query = Balance.objects.get(
                    client=instance.client, ecus_code=instance.ecus_code)
                if instance.total:
                    if previous.total:
                        if instance.type_code == 'E21':
                            if balance_query.e21:
                                balance_query.e21 = balance_query.e21 + instance.total - previous.total
                            else:
                                balance_query.e21 = instance.total - previous.total
                        if instance.type_code == 'B13':
                            if balance_query.b13:
                                balance_query.b13 = balance_query.b13 + instance.total - previous.total
                            else:
                                balance_query.b13 = instance.total - previous.total
                        if instance.type_code == 'A42':
                            if balance_query.a42:
                                balance_query.a42 = balance_query.a42 + instance.total - previous.total
                            else:
                                balance_query.a42 = instance.total - previous.total
                        if instance.type_code == 'E52':
                            if balance_query.e52:
                                balance_query.e52 = balance_query.e52 + instance.total - previous.total
                            else:
                                balance_query.e52 = instance.total - previous.total
                balance_query.save()
                return

        except Balance.DoesNotExist:
            if instance.npl_sp_code:
                new_balance = Balance(client=instance.client,
                                      ecus_code=instance.npl_sp_code)
                if instance.type_code == 'E21':
                    new_balance.e21 = instance.total - previous.total
                if instance.type_code == 'B13':
                    new_balance.b13 = instance.total - previous.total
                if instance.type_code == 'A42':
                    new_balance.a42 = instance.total - previous.total
                if instance.type_code == 'E52':
                    new_balance.e52 = instance.total - previous.total
                new_balance.save()
                return


'''
'ERP code': BOM.rm_code
'Ecus code': Ecus.npl_sp_code, BOM.ecus_code
'''


@receiver(pre_save, sender=BOM)
def on_bom_change(sender, instance, **kwargs):
    if instance.id is None:
        try:
            if instance.ecus_code:
                balance_query = Balance.objects.get(
                    client=instance.client, ecus_code=instance.ecus_code)
                if instance.finish_product_exchange:
                    if balance_query.fg_stock:
                        balance_query.fg_stock += instance.finish_product_exchange
                    else:
                        balance_query.fg_stock = instance.finish_product_exchange
                balance_query.save()
                return

        except Balance.DoesNotExist:
            if instance.ecus_code:
                new_balance = Balance(client=instance.client,
                                      ecus_code=instance.ecus_code)
                new_balance.fg_stock = instance.finish_product_exchange
                new_balance.save()
                return

    else:
        previous = BOM.objects.get(id=instance.id)
        try:
            if instance.ecus_code:
                balance_query = Balance.objects.get(
                    client=instance.client, ecus_code=instance.ecus_code)
                if instance.finish_product_exchange:
                    if balance_query.fg_stock:
                        if previous.finish_product_exchange:
                            balance_query.fg_stock = balance_query.fg_stock + \
                                instance.finish_product_exchange - previous.finish_product_exchange
                        else:
                            balance_query.fg_stock = balance_query.fg_stock + instance.finish_product_exchange
                    else:
                        balance_query.fg_stock = instance.finish_product_exchange - \
                            previous.finish_product_exchange
                balance_query.save()
                return

        except Balance.DoesNotExist:
            if instance.ecus_code:
                new_balance = Balance(client=instance.client,
                                      ecus_code=instance.ecus_code)
                if instance.type_code == 'E21':
                    new_balance.fg_stock = instance.finish_product_exchange
                new_balance.save()
                return


@receiver(pre_save, sender=Stock)
def on_stock_change(sender, instance, **kwargs):
    if instance.id is None:
        try:
            if instance.ecus_code:
                balance_query = Balance.objects.get(
                    client=instance.client, ecus_code=instance.ecus_code)
                if balance_query.rm_stock:
                    balance_query.rm_stock += instance.get_ending_quantity()
                else:
                    balance_query.rm_stock = instance.get_ending_quantity()
                balance_query.save()
                return
        except Balance.DoesNotExist:
            if instance.ecus_code:
                new_balance = Balance(client=instance.client,
                                      ecus_code=instance.ecus_code)
                new_balance.rm_stock = instance.get_ending_quantity()
                new_balance.save()
                return

    else:
        previous = Stock.objects.get(id=instance.id)
        try:
            if instance.ecus_code:
                balance_query = Balance.objects.get(
                    client=instance.client, ecus_code=instance.ecus_code)
                if balance_query.rm_stock:
                    balance_query.rm_stock = balance_query.fg_stock + \
                        instance.get_ending_quantity() - previous.get_ending_quantity()
                balance_query.save()
                return
        except Balance.DoesNotExist:
            if instance.ecus_code:
                new_balance = Balance(client=instance.client,
                                      ecus_code=instance.ecus_code)

                new_balance.rm_stock = instance.get_ending_quantity()
                new_balance.save()
                return
