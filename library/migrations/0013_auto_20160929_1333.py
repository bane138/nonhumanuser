# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-09-29 20:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0012_auto_20160914_1254'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemcomment',
            old_name='comment',
            new_name='item',
        ),
    ]
