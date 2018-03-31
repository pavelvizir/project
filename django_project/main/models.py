import datetime
from django.db import models
from django.utils import timezone


# Create your models here.
class Tag(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class Document(models.Model):
	name = models.CharField(max_length=50)
	date_of_creation = models.DateField()
	content = models.TextField()
	content_type = models.CharField(max_length=30)
	tags = models.ManyToManyField(Tag, related_name="documents")
	path = models.CharField(max_length=1024)

	def __str__(self):
		return self.name


	def was_published_recently(self):
		return self.date_of_creation >= timezone.now() - datetime.timedelta(days=1)


class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.question_text


class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text


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
