# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-10 08:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0003_auto_20170109_1939'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='TempUserProfile',
        ),
        migrations.AlterModelOptions(
            name='tempuserprofile',
            options={},
        ),
    ]
