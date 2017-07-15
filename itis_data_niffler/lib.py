from datetime import datetime
import django.forms as f
from dal import autocomplete
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, ModelMultipleChoiceField, ChoiceField, TypedChoiceField

from itis_manage.models import Subject

COURSE_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
)

SEMESTER_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, 'Оба')
)

STUDENT_STATS_SCORE_FIELDS = {
    'date_begin': f.DateField(),
    'date_end': f.DateField(),
    'course': f.MultipleChoiceField(choices=COURSE_CHOICES, widget=autocomplete.Select2Multiple()),
    'semester': f.ChoiceField(choices=SEMESTER_CHOICES, widget=autocomplete.Select2()),
    'subject': f.ModelMultipleChoiceField(queryset=Subject.objects.all(), widget=autocomplete.ModelSelect2Multiple()),
}


def semesters(x):
    return {
        '1': [1, 2],
        '2': [3, 4],
        '3': [5, 6],
        '4': [7, 8]
    }.get(x)


MONTH_OF_GROUPS_FOUNDATION = 9


def diff_month(d1, d2):
    return (int(d1.year) - d2) * 12 + int(d1.month) - MONTH_OF_GROUPS_FOUNDATION


def set_readable_related_fields(instance, self, ):
    for field in self.fields:
        try:
            if self.fields[field].__class__ == ModelChoiceField:
                self.fields[field].queryset = self.fields[field].queryset.filter(
                    **{'id': getattr(instance, field).id})
            elif self.fields[field].__class__ == ModelMultipleChoiceField:
                self.fields[field].queryset = self.fields[field].queryset.filter(
                    **{'id__in': getattr(instance, field).all().values('id')})
            elif self.fields[field].__class__ == TypedChoiceField:
                for i in self.fields[field].choices:
                    if i[0] == getattr(instance, field):
                        ls = (i[0], i[1])
                        self.fields[field].choices = [ls, ]
        except:
            raise ValidationError(str(self.fields[field].__class__) + ' is not a readable')


def make_form(form_name, form_init, form_class=(f.BaseForm,), ctx=None):
    return type(form_name, form_class, form_init)
