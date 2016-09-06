# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-06 16:35
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('min_team_size', models.IntegerField(default=0)),
                ('max_team_size', models.IntegerField(default=2)),
                ('description', models.TextField()),
                ('prize_1', models.IntegerField(default=0)),
                ('prize_2', models.IntegerField(default=0)),
                ('prize_3', models.IntegerField(default=0)),
                ('max_teams', models.IntegerField(default=15)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])),
                ('name', models.CharField(max_length=30)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
            ],
        ),
    ]
