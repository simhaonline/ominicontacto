# Generated by Django 2.2.7 on 2020-05-26 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0050_queue_wait_announce_frequency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campana',
            name='campos_bd_no_editables',
            field=models.CharField(default='', max_length=2052),
        ),
        migrations.AlterField(
            model_name='campana',
            name='campos_bd_ocultos',
            field=models.CharField(default='', max_length=2052),
        ),
    ]