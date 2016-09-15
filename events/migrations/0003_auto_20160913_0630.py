# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-13 06:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_team_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='event',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, to='events.Event'),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(default='default', max_length=30),
        ),
    ]