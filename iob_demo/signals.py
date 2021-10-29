from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import ItemsTakeIn, ItemsTakeOut, IOB


@receiver(pre_save, sender=ItemsTakeIn)
def on_take_in_change(sender, instance, **kwargs):
    iob, _ = IOB.objects.get_or_create(
        client=instance.client, code=instance.code, date=instance.date, unit=str.upper(instance.unit))
    instance.iob = iob


@receiver(pre_save, sender=ItemsTakeOut)
def on_take_out_change(sender, instance, **kwargs):
    iob, _ = IOB.objects.get_or_create(
        client=instance.client, code=instance.code, date=instance.date, unit=str.upper(instance.unit))
    instance.iob = iob
