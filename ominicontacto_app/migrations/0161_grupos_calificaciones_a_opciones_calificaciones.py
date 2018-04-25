# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-01-30 21:13
from __future__ import unicode_literals

import django.db.models.deletion

from django.db import migrations, models
from django.conf import settings
from django.utils.translation import ugettext as _

GESTION = 1
AGENDA = 2


def adicionar_opciones_calificacion_modelos_calificacion_contactos(apps, schema_editor):
    """
    Crea opciones de calificacion y las relaciona con las calificaciones de contactos existentes
    de acuerdo a los valores existentes
    """
    CalificacionCliente = apps.get_model('ominicontacto_app', 'calificacioncliente')
    CalificacionManual = apps.get_model('ominicontacto_app', 'calificacionmanual')
    OpcionCalificacion = apps.get_model('ominicontacto_app', 'opcioncalificacion')

    # TODO: unificar este código en un sólo ciclo cuando se hayan unificado los modelos
    # CalificacionCliente y CalificacionManual
    for calif_cliente in CalificacionCliente.objects.all():
        campana = calif_cliente.campana
        if calif_cliente.calificacion is None and calif_cliente.es_venta:
            # las calificaciones de gestion anteriormente no tenían
            # instancia de nombre de calificación asociada, se la asigna el nombre
            # la opción de gestión de la campaña
            tipo = GESTION
            nombre_calificacion = campana.gestion
        elif calif_cliente.calificacion.nombre == settings.CALIFICACION_REAGENDA:
            nombre_calificacion = calif_cliente.calificacion.nombre
            tipo = AGENDA
        else:
            nombre_calificacion = calif_cliente.calificacion.nombre
            tipo = int(campana.gestion == nombre_calificacion)
        opcion_calificacion, _ = OpcionCalificacion.objects.get_or_create(
            campana=campana, nombre=nombre_calificacion, tipo=tipo)
        calif_cliente.opcion_calificacion = opcion_calificacion
        calif_cliente.save()

    for calif_manual in CalificacionManual.objects.all():
        campana = calif_manual.campana
        if calif_manual.calificacion is None and calif_manual.es_gestion:
            # las calificaciones manuales de gestion anteriormente no tenían
            # instancia de nombre de calificación asociada, se la asigna el nombre
            # la opción de gestión de la campaña
            tipo = GESTION
            nombre_calificacion = campana.gestion
        elif calif_manual.calificacion.nombre == settings.CALIFICACION_REAGENDA:
            nombre_calificacion = calif_manual.calificacion.nombre
            tipo = AGENDA
        else:
            nombre_calificacion = calif_manual.calificacion.nombre
            tipo = int(campana.gestion == nombre_calificacion)
        opcion_calificacion, _ = OpcionCalificacion.objects.get_or_create(
            campana=campana, nombre=nombre_calificacion, tipo=tipo)
        calif_manual.opcion_calificacion = opcion_calificacion
        calif_manual.save()


def adicionar_calificaciones_y_campanas_a_modelos_calificacion_contactos(apps, schema_editor):
    """
    Asigna los nombres de calificaciones y campañas a las instancias de los modelos de calificación
    de contactos tomando como referencia los valores de las opciones de clasificacion existentes
    """
    CalificacionCliente = apps.get_model('ominicontacto_app', 'calificacioncliente')
    CalificacionManual = apps.get_model('ominicontacto_app', 'calificacionmanual')
    NombreCalificacion = apps.get_model('ominicontacto_app', 'nombrecalificacion')

    for calif_cliente in CalificacionCliente.objects.all():
        opcion_calificacion = calif_cliente.opcion_calificacion
        calif_cliente.campana = opcion_calificacion.campana
        nombre_calificacion, _ = NombreCalificacion.objects.get_or_create(
            nombre=opcion_calificacion.nombre)
        calif_cliente.calificacion = nombre_calificacion
        calif_cliente.save()

    for calif_manual in CalificacionManual.objects.all():
        opcion_calificacion = calif_manual.opcion_calificacion
        calif_manual.campana = opcion_calificacion.campana
        nombre_calificacion, _ = NombreCalificacion.objects.get_or_create(
            nombre=opcion_calificacion.nombre)
        calif_manual.calificacion = nombre_calificacion
        calif_manual.save()


def adicionar_calificaciones_campana(apps, schema_editor):
    """
    Adiciona las opciones de calificación a una campaña de acuerdo
    a partir de las calificaciones en el grupo de calificacion asociado
    a la campaña
    """
    Campana = apps.get_model("ominicontacto_app", "campana")
    OpcionCalificacion = apps.get_model('ominicontacto_app', 'opcioncalificacion')
    NombreCalificacion = apps.get_model('ominicontacto_app', 'nombrecalificacion')

    for campana in Campana.objects_default.all():
        # creamos las opciones de calificacion que relacionan las campañas con las calificaciones
        # todas tendrán inicialmente el valor de opción por defecto NO_ACCION, excepto la
        # calificación que corresponde con el tipo de gestión de la campaña
        opciones_clasificacion = [
            OpcionCalificacion(campana=campana, nombre=calificacion.nombre)
            for calificacion in campana.calificacion_campana.calificacion.all()
            if calificacion.nombre not in [campana.gestion, settings.CALIFICACION_REAGENDA]]
        calificacion_gestion, _ = NombreCalificacion.objects.get_or_create(nombre=campana.gestion)
        opciones_clasificacion.extend(
            [OpcionCalificacion(campana=campana, nombre=calificacion_gestion.nombre, tipo=GESTION),
             OpcionCalificacion(
                 campana=campana, nombre=settings.CALIFICACION_REAGENDA, tipo=AGENDA)])
        OpcionCalificacion.objects.bulk_create(opciones_clasificacion)


def restaurar_grupos_calificaciones_campanas(apps, schema_editor):
    """
    Crea un grupo de calificaciones con las existentes asociadas a una campaña y lo asocia a
    dicha campaña mediante el modelo CalificacionCampana
    """

    Campana = apps.get_model("ominicontacto_app", "campana")
    CalificacionCampana = apps.get_model('ominicontacto_app', 'calificacioncampana')
    NombreCalificacion = apps.get_model('ominicontacto_app', 'nombrecalificacion')

    for campana in Campana.objects_default.all():
        grupo_calificacion_campana = CalificacionCampana.objects.create(
            nombre=_("Grupo {0}".format(campana.pk)))
        nombres_opciones_calificaciones = campana.opciones_calificacion.values_list(
            'nombre', flat=True)
        calificaciones_campana = NombreCalificacion.objects.filter(
            nombre__in=nombres_opciones_calificaciones)
        grupo_calificacion_campana.calificacion.add(*calificaciones_campana)
        nombre_calificacion_gestion = campana.opciones_calificacion.filter(
            tipo=GESTION).first().nombre
        campana.calificacion_campana = grupo_calificacion_campana
        campana.gestion = nombre_calificacion_gestion
        campana.save()


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0160_cambia_nombre_modelo_calificacion')
    ]

    operations = [
        # permite que el campo 'calificacion_campana' sea nulo, esto para poder volver
        # hacia atrás y reasignar los grupos calificaciones en reversa
        migrations.AlterField(
            model_name='campana',
            name='calificacion_campana',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE,
                related_name='calificacioncampana', to='ominicontacto_app.CalificacionCampana'),
        ),

        # operaciones para crear el modelo OpcionCalificacion y su relacion con las campañas
        migrations.CreateModel(
            name='OpcionCalificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('tipo', models.IntegerField(choices=[(1, 'Gesti\xf3n'), (0, 'Sin acci\xf3n'),
                                                      (2, 'Agenda')], default=0)),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),

        migrations.AddField(
            model_name='opcioncalificacion',
            name='campana',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='opciones_calificacion',
                                    to='ominicontacto_app.Campana'),
        ),


        # operaciones para migrar los datos de grupos a opciones de calificacion y en reversa
        migrations.RunPython(code=adicionar_calificaciones_campana,
                             reverse_code=migrations.RunPython.noop),

        migrations.RunPython(code=migrations.RunPython.noop,
                             reverse_code=restaurar_grupos_calificaciones_campanas),

        # operaciones para realizar la migración de datos de los campos 'calificacion'
        # y 'campana' de los modelos CalificacionCliente y CalificacionManual hacia el
        # el modelo OpcionCalificacion y viceversa

        # permiten nulidad en los campos 'campana' y 'calificacion' de los modelos de calificaciones
        # de contactos
        migrations.AlterField(
            model_name='calificacioncliente',
            name='campana',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE,
                related_name='calificaconcliente', to='ominicontacto_app.Campana'),
        ),

        migrations.AlterField(
            model_name='calificacioncliente',
            name='calificacion',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE,
                 to='ominicontacto_app.NombreCalificacion'),
        ),

        migrations.AlterField(
            model_name='calificacionmanual',
            name='campana',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE,
                related_name='calificaconcliente', to='ominicontacto_app.Campana'),
        ),

        migrations.AlterField(
            model_name='calificacionmanual',
            name='calificacion',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE,
                 to='ominicontacto_app.NombreCalificacion'),
        ),

        # adiciona campo 'opcion_calificacion' a modelos de calificaciones de contactos
        # inicialmente permitiendo nulidad para poder luego adicionar los valores
        migrations.AddField(
            model_name='calificacioncliente',
            name='opcion_calificacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='calificaciones_cliente', null=True,
                                    to='ominicontacto_app.OpcionCalificacion'),
        ),

        migrations.AddField(
            model_name='calificacionmanual',
            name='opcion_calificacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='calificaciones_manuales', null=True,
                                    to='ominicontacto_app.OpcionCalificacion'),
        ),

        # realiza migraciones de datos para modelos de calificaciones de contactos
        # hacia modelo OpcionCalificacion (y migraciones de datos reversas)

        migrations.RunPython(
            code=adicionar_opciones_calificacion_modelos_calificacion_contactos,
            reverse_code=adicionar_calificaciones_y_campanas_a_modelos_calificacion_contactos),


        # no se permite nulidad al campo 'opcion_calificacion' en los modelos de calificación
        # de contactos después de adicionar los datos de las opciones de calificación
        migrations.AlterField(
            model_name='calificacioncliente',
            name='opcion_calificacion',
            field=models.ForeignKey(
                null=False, related_name='calificaciones_cliente',
                on_delete=django.db.models.deletion.CASCADE,
                to='ominicontacto_app.OpcionCalificacion'),
        ),

        migrations.AlterField(
            model_name='calificacionmanual',
            name='opcion_calificacion',
            field=models.ForeignKey(
                null=False, related_name='calificaciones_manuales',
                on_delete=django.db.models.deletion.CASCADE,
                to='ominicontacto_app.OpcionCalificacion'),
        ),

        # operaciones para eliminar los campos 'campanas' y 'calificacion' de los modelos de
        # calificacion de contactos
        migrations.RemoveField(
            model_name='calificacioncliente',
            name='campana',
        ),

        migrations.RemoveField(
            model_name='calificacioncliente',
            name='calificacion',
        ),

        migrations.RemoveField(
            model_name='calificacionmanual',
            name='campana',
        ),

        migrations.RemoveField(
            model_name='calificacionmanual',
            name='calificacion',
        ),

        # operaciones para eliminar los grupos de calificaciones
        migrations.RemoveField(
            model_name='calificacioncampana',
            name='calificacion',
        ),
        migrations.RemoveField(
            model_name='campana',
            name='calificacion_campana',
        ),
        migrations.DeleteModel(
            name='CalificacionCampana',
        ),

    ]