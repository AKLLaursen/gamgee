# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-06 19:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogengine', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='pubDate',
            new_name='pub_date',
        ),
    ]