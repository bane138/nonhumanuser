# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-20 22:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actual_play', '0005_auto_20161010_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='actual_play/image/%Y/%m/%d'),
        ),
    ]