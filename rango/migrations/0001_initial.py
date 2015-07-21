# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='comp_type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('complaint_date', models.DateTimeField(auto_now_add=True)),
                ('complaint_taker', models.CharField(max_length=30)),
                ('fname', models.CharField(max_length=60)),
                ('birth_date', models.DateField(null=True)),
                ('gender', models.CharField(default=b'M', max_length=2, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('mob', models.IntegerField(null=True)),
                ('descrip', models.CharField(max_length=500)),
                ('status_remarks', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ComplaintView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('search', models.CharField(max_length=50, null=True, blank=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='office_staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='offices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('office_name', models.CharField(unique=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('complaint_status', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='taluka',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('t', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='office_staff',
            name='office',
            field=models.ForeignKey(to='rango.offices'),
        ),
        migrations.AddField(
            model_name='complaintview',
            name='acc_person',
            field=models.ForeignKey(to='rango.office_staff', to_field=b'name', null=True),
        ),
        migrations.AddField(
            model_name='complaintview',
            name='complaint_type',
            field=models.ForeignKey(to='rango.comp_type', null=True),
        ),
        migrations.AddField(
            model_name='complaintview',
            name='office',
            field=models.ForeignKey(blank=True, to='rango.offices', null=True),
        ),
        migrations.AddField(
            model_name='complaintview',
            name='status',
            field=models.ForeignKey(to='rango.status', null=True),
        ),
        migrations.AddField(
            model_name='complaintview',
            name='taluka',
            field=models.ForeignKey(to='rango.taluka', null=True),
        ),
        migrations.AddField(
            model_name='complaint',
            name='acc_person',
            field=models.ForeignKey(to='rango.office_staff', to_field=b'name'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='complaint_type',
            field=models.ForeignKey(to='rango.comp_type'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='office',
            field=models.ForeignKey(to='rango.offices'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='status',
            field=models.ForeignKey(to='rango.status'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='taluka',
            field=models.ForeignKey(to='rango.taluka'),
        ),
    ]
