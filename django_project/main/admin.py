from django.contrib import admin
from django.contrib import admin

from .models import Question, Document, Tag, Data

admin.site.register(Question)
admin.site.register(Document)
admin.site.register(Tag)
admin.site.register(Data)
# admin.site.register(DataProviders)