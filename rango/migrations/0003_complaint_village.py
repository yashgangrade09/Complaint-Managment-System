# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0002_village'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='village',
            field=models.ForeignKey(to='rango.village', null=True),
        ),
    ]
