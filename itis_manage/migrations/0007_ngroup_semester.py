# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itis_manage', '0006_remove_progress_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='ngroup',
            name='semester',
            field=models.ForeignKey(default=1, related_name='semester_groups', to='itis_manage.Semester'),
            preserve_default=False,
        ),
    ]
