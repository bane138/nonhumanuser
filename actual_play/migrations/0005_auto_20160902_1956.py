# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-09-02 19:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('actual_play', '0004_remove_game_source_destination'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('author', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(default=datetime.datetime(2016, 9, 2, 19, 56, 26, 24233, tzinfo=utc))),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.RenameField(
            model_name='game',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='game',
            name='number_comments',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='number_views',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gamecomment',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='actual_play.Game'),
        ),
    ]
