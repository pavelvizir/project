from django.db import models

# Create your models here.
class Tag(models.Model):
	name = models.CharField(max_length = 50)

class Document(models.Model):
	name = models.CharField(max_length = 50)
	date_of_creation = models.DateField()
	content = models.TextField()
	content_type = models.CharField(max_length = 30) 
	tags = models.ManyToManyField(Tag, related_name = "documents")
	path = models.CharField(max_length = 1024)
