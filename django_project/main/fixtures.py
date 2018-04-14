# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

def load_models_from_fixture(apps, schema_editor):
    from django.core.management import call_command
    call_command("loaddata", "Data")

def delete_models(apps, schema_editor):
    Model = apps.get_model("models", "Model")
    Model.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('models', '0003_auto_20180414_0959'),
    ]
    operations = [
        migrations.RunPython(load_models_from_fixture,delete_models),
    ]
