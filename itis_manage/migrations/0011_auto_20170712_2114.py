# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itis_manage', '0010_auto_20170712_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ngroup',
            name='year_of_foundation',
            field=models.IntegerField(),
        ),
    ]
