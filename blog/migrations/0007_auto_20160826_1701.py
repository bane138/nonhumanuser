# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-26 17:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20160814_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrycomment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 26, 17, 1, 50, 611144, tzinfo=utc)),
        ),
    ]
