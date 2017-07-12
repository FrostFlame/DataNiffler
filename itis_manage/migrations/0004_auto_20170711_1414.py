# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itis_manage', '0003_auto_20170710_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progress',
            name='student',
            field=models.ForeignKey(to='itis_manage.Student', related_name='student_progresses'),
        ),
        migrations.AlterField(
            model_name='progress',
            name='subject',
            field=models.ForeignKey(to='itis_manage.Subject', related_name='subject_progresses'),
        ),
        migrations.AlterUniqueTogether(
            name='progress',
            unique_together=set([('subject', 'student')]),
        ),
    ]
