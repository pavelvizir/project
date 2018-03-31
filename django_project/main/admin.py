from django.contrib import admin
from django.contrib import admin

from .models import Question, Document, Tag, Mail_Account, Mail

admin.site.register(Question)
admin.site.register(Document)
admin.site.register(Tag)
admin.site.register(Mail_Account)
admin.site.register(Mail)