# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-06 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogengine', '0002_auto_20160106_2048'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='Default', max_length=40, unique=True),
            preserve_default=False,
        ),
    ]
