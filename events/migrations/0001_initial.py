# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-06 06:13
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])),
                ('name', models.CharField(max_length=30)),
                ('event', models.CharField(choices=[(0, 'OSC'), (1, 'Esoteric'), (2, 'Debug your ass'), (3, 'Robotics')], max_length=1)),
                ('members', models.ManyToManyField(related_name='teams', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
