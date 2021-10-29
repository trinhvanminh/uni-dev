from django.db import models
from django.utils import timezone
from client.models import Client
from django.db.models import Sum


# class TakeIn(models.Model):
#     take_in = models.IntegerField()
#     item = models.ForeignKey(
#         "ItemsTakeIn", related_name='take_ins', on_delete=models.CASCADE, null=True, blank=True)


# class TakeOut(models.Model):
#     take_out = models.IntegerField()
#     item = models.ForeignKey(
#         "ItemsTakeOut", related_name='take_outs', on_delete=models.CASCADE, null=True, blank=True)


class ItemsTakeIn(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, null=True, blank=True)
    iob = models.ForeignKey(
        'IOB', related_name='take_ins', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    invoice_no = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True, blank=True)
    unit = models.CharField(max_length=5)
    price = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    cd_no = models.CharField(max_length=50, null=True, blank=True)
    take_in = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.code

    def get_take_in(self):
        return self.take_in.objects.all().aggregate(Sum('take_in'))


class ItemsTakeOut(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, null=True, blank=True)
    iob = models.ForeignKey(
        'IOB', related_name='take_outs', on_delete=models.CASCADE, null=True, blank=True)
    invoice_no = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True, blank=True)
    unit = models.CharField(max_length=5)
    price = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    take_out = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.code

    def get_take_out(self):
        return self.take_in.objects.all().aggregate(Sum('take_out'))


class IOB(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    date = models.DateField()
    unit = models.CharField(max_length=5, null=True, blank=True)

    class Meta:
        unique_together = ("client", "code", "date")

    def __str__(self) -> str:
        return self.code

    def begin(self):
        take_ins = ItemsTakeIn.objects.filter(client=self.client,
                                              code=self.code).filter(date__lt=self.date)
        take_outs = ItemsTakeOut.objects.filter(client=self.client,
                                                code=self.code).filter(date__lt=self.date)
        begin = 0
        for take_in in take_ins:
            if take_in.take_in:
                begin += take_in.take_in
        for take_out in take_outs:
            if take_out.take_out:
                begin += take_out.take_out
        return begin

    def get_take_in(self):
        take_ins = self.take_ins.all()
        take_in_amount = 0
        for take_in in take_ins:
            if take_in.take_in:
                take_in_amount += take_in.take_in
        return take_in_amount

    def get_take_out(self):
        take_outs = self.take_outs.all()
        take_out_amount = 0
        for take_out in take_outs:
            if take_out.take_out:
                take_out_amount += take_out.take_out
        return take_out_amount

    def end(self):
        return self.begin() + self.get_take_in() - self.get_take_out()
