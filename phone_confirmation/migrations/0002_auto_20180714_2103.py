# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-07-14 21:03
from __future__ import unicode_literals

from django.db import migrations
import phone_confirmation.fields


class Migration(migrations.Migration):

    dependencies = [
        ('phone_confirmation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phoneconfirmation',
            name='code',
            field=phone_confirmation.fields.RandomPinField(blank=True, length=6, max_length=6),
        ),
    ]
