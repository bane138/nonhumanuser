# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-05 19:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_entrycomment_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entrycomment',
            old_name='body',
            new_name='comment',
        ),
        migrations.RemoveField(
            model_name='entrycomment',
            name='author',
        ),
    ]