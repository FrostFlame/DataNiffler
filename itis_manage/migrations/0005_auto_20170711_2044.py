# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itis_manage', '0004_auto_20170711_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='progress',
            name='semester_subject',
            field=models.ForeignKey(related_name='semester_subject_progresses', to='itis_manage.SemesterSubject', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(unique=True, max_length=30),
        ),
        migrations.AlterUniqueTogether(
            name='progress',
            unique_together=set([('semester_subject', 'student')]),
        ),
        migrations.RemoveField(
            model_name='progress',
            name='subject',
        ),
    ]
