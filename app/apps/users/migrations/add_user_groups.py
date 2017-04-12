# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import Group
from django.db import migrations


def add_groups(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    # Group = apps.get_model("django.contrib.auth", "Group")
    Group.objects.bulk_create([
        Group(name='Institute Admin'),
        Group(name='Student'),
        Group(name='Instructor')]
    )


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_auto_20170412_1319'),
    ]

    operations = [
        migrations.RunPython(add_groups),
    ]
