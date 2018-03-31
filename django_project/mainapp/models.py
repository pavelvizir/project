from django.db import models


# Create your models here.
class Data(models.Model):
    #ID = models.AutoField(primary_key=True, max_length=20)
    PID = models.IntegerField()
    CID = models.IntegerField()
    Psource = models.CharField(max_length=100)
    Csource = models.CharField(max_length=500)
    Type = models.CharField(max_length=100)
    Metadata = models.TextField()
    Data_main = models.TextField()
    Additional_data = models.TextField()
    Link = models.CharField(max_length=500)


class Data_providers(models.Model):
    #ID = models.AutoField(primary_key=True, max_length=20)
    Provider = models.CharField(max_length=100)
    Name = models.CharField(max_length=100)
    Type = models.CharField(max_length=100)
    Last_number = models.IntegerField()
