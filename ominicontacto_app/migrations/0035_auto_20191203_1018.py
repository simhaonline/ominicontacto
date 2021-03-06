# Generated by Django 2.2.7 on 2019-12-03 13:18

import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0034_auto_20200120_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actuacionvigente',
            name='campana',
            field=models.OneToOneField(on_delete=django.db.models.fields.related.OneToOneField, to='ominicontacto_app.Campana'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
