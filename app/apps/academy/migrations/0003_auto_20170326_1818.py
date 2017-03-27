# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-26 12:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0002_auto_20170326_0739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='education_program_courses', to='academy.Program'),
        ),
        migrations.AlterField(
            model_name='program',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='program_level_programs', to='academy.ProgramLevel'),
        ),
        migrations.AlterField(
            model_name='programlevel',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculty_program_levels', to='academy.Faculty'),
        ),
    ]
