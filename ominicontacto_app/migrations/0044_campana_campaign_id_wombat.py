# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-25 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0043_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='campana',
            name='campaign_id_wombat',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
