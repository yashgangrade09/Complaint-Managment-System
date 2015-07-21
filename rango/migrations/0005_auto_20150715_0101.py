# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0004_complaint_docfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='docfile',
            field=models.FileField(null=True, upload_to=b'documents', blank=True),
        ),
    ]
