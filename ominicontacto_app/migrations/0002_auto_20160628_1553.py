# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 15:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='queuemember',
            old_name='queue',
            new_name='queue_name',
        ),
        migrations.AlterUniqueTogether(
            name='queuemember',
            unique_together=set([('queue_name', 'membername')]),
        ),
    ]