# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-06-09 20:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actual_play', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamecomment',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]