# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-11 14:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_auto_20180311_2205'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Collention',
        ),
    ]