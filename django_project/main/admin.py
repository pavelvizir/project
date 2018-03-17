from django.contrib import admin
from django.contrib import admin

from .models import Question, Document, Tag

admin.site.register(Question)
admin.site.register(Document)
admin.site.register(Tag)