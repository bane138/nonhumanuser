# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-09-14 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0011_auto_20160906_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemcomment',
            name='created_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
