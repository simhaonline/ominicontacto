# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2019-03-20 19:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion




class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0015_rename_metadatacliente_respuestaformulariogestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuestaformulariogestion',
            name='calificacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='respuesta_formulario_gestion',
                                    to='ominicontacto_app.CalificacionCliente'),
        ),
        migrations.AlterField(
            model_name='respuestaformulariogestion',
            name='campana',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='metadatacliente',
                                    to='ominicontacto_app.Campana'),
        ),
        migrations.AlterField(
            model_name='respuestaformulariogestion',
            name='contacto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='ominicontacto_app.Contacto'),
        ),
        migrations.AlterField(
            model_name='respuestaformulariogestion',
            name='agente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='metadataagente',
                                    to='ominicontacto_app.AgenteProfile'),
        ),
    ]