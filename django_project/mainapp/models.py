from django.db import models


# Create your models here.
class Data(models.Model):
    #ID = models.AutoField(primary_key=True, max_length=20)
    PID = models.IntegerField() #номер письма
    CID = models.IntegerField() #номер вложения (письмо считается первым вложением)
    Psource = models.CharField(max_length=100) # источник: sms, imap
    Csource = models.CharField(max_length=500) #@example.com, +7(999)453-..., и тд
    Type = models.CharField(max_length=100) #тип документа предоставляет парсер
    Metadata = models.TextField() #в исходном коде письма содержатся заголовки, адреса
    Data_main = models.TextField() #plain text
    Additional_data = models.TextField() #html, если есть
    Link = models.CharField(max_length=500, null=True)



class Data_providers(models.Model):
    #ID = models.AutoField(primary_key=True, max_length=20)
    Provider = models.CharField(max_length=100)
    Name = models.CharField(max_length=100)
    Type = models.CharField(max_length=100)
    Last_number = models.IntegerField()
