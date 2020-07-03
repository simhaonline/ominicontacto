# Generated by Django 2.2.7 on 2020-02-14 15:45

import os

from django.conf import settings
from django.db import migrations

from constance import config


def copiar_valores_constance(apps, schema_editor):
    """Realiza la copia de los valores de las variables en constance
    desde el archivo de dump al nuevo backend en base de datos
    """
    ruta = os.path.join(settings.INSTALL_PREFIX, 'bin/constances_values.txt')
    if os.path.exists(ruta):
        with open(ruta, 'r') as archivo_dump:
            for line in archivo_dump.readlines():
                # eliminamos los caracteres de sufijos y prefijos de redis para obtener
                # el mero valor
                redis_key, redis_value = line.split('\t')
                redis_value = redis_value.strip()
                config.__setattr__(redis_key, redis_value)


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0057_inicializa_campo_modified'),
    ]

    operations = [
        migrations.RunPython(copiar_valores_constance, reverse_code=migrations.RunPython.noop),
    ]