# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-13 20:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0047_auto_20170202_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metadatacliente',
            name='contacto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ominicontacto_app.Contacto'),
        ),
    ]