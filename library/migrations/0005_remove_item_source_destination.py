# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-29 00:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_auto_20160229_0021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='source_destination',
        ),
    ]
