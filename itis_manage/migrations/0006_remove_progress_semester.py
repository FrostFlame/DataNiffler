# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itis_manage', '0005_auto_20170711_2044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='progress',
            name='semester',
        ),
    ]
