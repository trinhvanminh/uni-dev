from django.db import models
from django.db.models.fields import BooleanField
from django.utils import tree

# Create your models here.


class Section(models.Model):
    no = models.SmallIntegerField()
    name = models.CharField(max_length=100)


class Chapter(models.Model):
    no = models.SmallIntegerField()
    name = models.CharField(max_length=100)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, blank=True, null=True)


class Heading(models.Model):
    no = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True),
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.no


class SubHeading(models.Model):
    no = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    heading = models.ForeignKey(Heading, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.no


class Note(models.Model):
    no = models.CharField(max_length=5)
    description = models.TextField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    heading = models.ForeignKey(
        Heading, on_delete=models.CASCADE, blank=True, null=True
    )
    subheading = models.ForeignKey(
        SubHeading, on_delete=models.CASCADE, blank=True, null=True
    )
