# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-12 07:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0013_auto_20170409_1350'),
        ('users', '0002_user_institute'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='program_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='academy.ProgramLevel'),
        ),
        migrations.AlterField(
            model_name='user',
            name='institute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='academy.Institute'),
        ),
    ]