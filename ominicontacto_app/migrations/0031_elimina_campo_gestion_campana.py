# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2019-06-27 17:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0030_renombra_BD_repetidos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campana',
            name='gestion',
        ),
    ]
