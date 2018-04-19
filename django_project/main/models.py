import datetime

from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.utils import timezone



class Data(models.Model):
    # ID = models.AutoField(primary_key=True, max_length=20)
    PID = models.IntegerField()  # номер письма
    CID = models.IntegerField()  # номер вложения (письмо считается первым вложением)
    psource = models.CharField(max_length=100)  # источник: sms, imap
    csource = models.CharField(max_length=500)  # @example.com, +7(999)453-..., и тд
    typedoc = models.CharField(max_length=100)  # тип документа предоставляет парсер
    metadata = models.TextField()  # в исходном коде письма содержатся заголовки, адреса
    data_main = models.TextField(null=True)  # plain text
    additional_data = models.TextField(null=True)  # html, если есть
    link = models.CharField(max_length=500, null=True)
    search_vector = SearchVectorField(null=True)

    def __int__(self):
        return self.PID

    # def was_published_recently(self):
    #     return self.Metadata >= timezone.now() - datetime.timedelta(days=1)

# def was_published_recently(self):
# 	return self.Metadata >= timezone.now() - datetime.timedelta(days=1)



class Mail_Account(models.Model):
    email = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    server = models.CharField(max_length=100)
    port = models.IntegerField(default=993)
    last_uid = models.IntegerField()

    def __str__(self):
        return self.email


class Mail(models.Model):
    _delivered_to = models.ForeignKey(Mail_Account, on_delete=models.CASCADE)
    _to = models.CharField(max_length=200)
    _from = models.CharField(max_length=200)
    _subject = models.CharField(max_length=200)
    _date = models.DateField()
    _message_id = models.CharField(max_length=200)
    text = models.TextField(default='')
    html = models.TextField(default='')

    def __str__(self):
        return self._subject

class Document(models.Model):
    name = models.CharField(max_length=50)
    date_of_creation = models.DateField()
    content = models.TextField()
    content_type = models.CharField(max_length=30)
    # tags = models.ManyToManyField(Tag, related_name="documents")
    path = models.CharField(max_length=1024)

    def __str__(self):
        return self.name

    def was_published_recently(self):
        return self.date_of_creation >= timezone.now() - datetime.timedelta(days=1)

# class DataProviders(models.Model):
# 	provider = models.CharField(max_length=100)
# 	name = models.CharField(max_length=100)
# 	type = models.CharField(max_length=100)
# 	last_number = models.IntegerField()
#
# 	def __str__(self):
# 		return self.Name
