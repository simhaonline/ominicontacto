# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-29 19:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0019_formulariodemo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formulariodemo',
            name='apellido',
        ),
        migrations.RemoveField(
            model_name='formulariodemo',
            name='datos',
        ),
        migrations.RemoveField(
            model_name='formulariodemo',
            name='email',
        ),
        migrations.RemoveField(
            model_name='formulariodemo',
            name='id_cliente',
        ),
        migrations.RemoveField(
            model_name='formulariodemo',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='formulariodemo',
            name='telefono',
        ),
    ]
