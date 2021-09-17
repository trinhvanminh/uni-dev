from django.db import models

# Create your models here.


class Section(models.Model):
    no = models.SmallIntegerField()
    name = models.CharField(max_length=100)


class Chapter(models.Model):
    no = models.SmallIntegerField()
    name = models.CharField(max_length=100)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)


class Heading(models.Model):
    no = models.TextField(max_length=4)
    name = models.CharField(max_length=100)
    description = models.TextField()
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)


class SubHeading(models.Model):
    no = models.TextField(max_length=8)
    name = models.CharField(max_length=100)
    description = models.TextField()
    heading = models.ForeignKey(Heading, on_delete=models.CASCADE)


class Note(models.Model):
    no = models.CharField(max_length=5)
    description = models.TextField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
