# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0003_complaint_village'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='docfile',
            field=models.FileField(null=True, upload_to=b'documents'),
        ),
    ]
