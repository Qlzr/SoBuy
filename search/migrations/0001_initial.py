# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-09 13:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('price', models.CharField(max_length=12)),
                ('detail_url', models.CharField(max_length=150)),
                ('img_url', models.CharField(max_length=150)),
                ('store', models.CharField(max_length=50)),
                ('store_url', models.CharField(max_length=150)),
                ('website', models.CharField(max_length=16)),
                ('keyword', models.CharField(max_length=150)),
                ('search_time', models.DateTimeField()),
                ('sort_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=150)),
                ('user', models.CharField(default='visitor', max_length=50)),
                ('created_time', models.DateTimeField()),
            ],
        ),
    ]
