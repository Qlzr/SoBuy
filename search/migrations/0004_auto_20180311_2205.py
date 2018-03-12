# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-11 14:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_auto_20180309_2138'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collention',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=200)),
                ('price', models.CharField(max_length=12)),
                ('detail_url', models.CharField(max_length=150)),
                ('img_url', models.CharField(max_length=255)),
                ('website', models.CharField(max_length=16)),
                ('collect_time', models.DateTimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='Commodity',
        ),
    ]
