# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-17 19:43
from __future__ import unicode_literals

from django.db import migrations
from django.core.management.commands import loaddata

def apply_fixtures(apps, schema_editor):
    # XXX: This is more or less a hack! Please refrain from using this.
    cmd = loaddata.Command()
    cmd.run_from_argv(['./manage.py', 'loaddata', 'ossm/fixtures/social.json'])


class Migration(migrations.Migration):

    dependencies = [
        ('ossm', '0001_initial'),
        ('socialaccount', '0003_extra_data_default_dict')
    ]

    operations = [
        migrations.RunPython(apply_fixtures)
    ]
