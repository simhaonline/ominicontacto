# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-15 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0079_auto_20170515_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='campanamember',
            name='campana_nombre',
            field=models.CharField(default='campana_default', max_length=128),
            preserve_default=False,
        ),
    ]