# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-09-02 19:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_auto_20160901_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemcomment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 2, 19, 56, 26, 20894, tzinfo=utc)),
        ),
    ]
