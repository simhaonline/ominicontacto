# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-03-27 15:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0165_mv_calificacioncliente_calificacionmanual'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calificacionmanual',
            name='agente',
        ),
        migrations.RemoveField(
            model_name='calificacionmanual',
            name='contacto',
        ),
        migrations.RemoveField(
            model_name='calificacionmanual',
            name='opcion_calificacion',
        ),
        migrations.DeleteModel(
            name='CalificacionManual',
        ),
    ]
