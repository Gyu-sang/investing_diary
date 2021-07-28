from django.db import models

# Create your models here.
class Corporation(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(null=True, upload_to='logos')

class Diary(models.Model):
    user = models.CharField(max_length=50)
    content = models.TextField()
    buy = models.ManyToManyField(Corporation, related_name='item_bought')
    sell = models.ManyToManyField(Corporation, related_name='item_sold')


