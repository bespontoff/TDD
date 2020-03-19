from django.db import models


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey('List', models.CASCADE, default=None)


class List(models.Model):
    pass
