# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itis_manage', '0009_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ngroup',
            name='semester',
        ),
        migrations.AddField(
            model_name='ngroup',
            name='curator',
            field=models.ForeignKey(default=1, to='itis_manage.Person', related_name='curator_groups'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ngroup',
            name='year_of_foundation',
            field=models.IntegerField(max_length=4, default=2015),
            preserve_default=False,
        ),
    ]
