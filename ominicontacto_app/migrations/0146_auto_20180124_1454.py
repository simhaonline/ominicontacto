# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-01-24 17:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0145_auto_20180125_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queue',
            name='initial_boost_factor',
            field=models.DecimalField(
                blank=True, decimal_places=1, default=1.0, max_digits=3, null=True),
        ),
    ]
