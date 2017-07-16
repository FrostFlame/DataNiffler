import datetime

import django.forms as f
from dal import autocomplete
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, ModelMultipleChoiceField, ChoiceField, TypedChoiceField

from itis_manage.models import Subject
from practice2017 import settings

COURSE_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
)

SEMESTER_BOTH = 3

SEMESTER_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, 'Оба')
)

YEAR_CHOICES_S = ((i, i) for i in range(2000, datetime.datetime.today().year))
YEAR_CHOICES_E = ((i, i) for i in range(2000, datetime.datetime.today().year + 1))
CONTEXT = {
    ''
}
YEAR_TODAY = datetime.datetime.today().year

STUDENT_STATS_SCORE_FIELDS = {
    'date_begin': f.IntegerField(initial=YEAR_TODAY - 1,
                                 widget=autocomplete.Select(choices=YEAR_CHOICES_S), required=True),
    'date_end': f.IntegerField(initial=YEAR_TODAY,
                               widget=autocomplete.Select(choices=YEAR_CHOICES_E), required=True),
    'course': f.MultipleChoiceField(choices=COURSE_CHOICES, initial=COURSE_CHOICES[0],
                                    widget=autocomplete.Select2Multiple(), required=True),
    'semester': f.ChoiceField(choices=SEMESTER_CHOICES, initial=3, widget=autocomplete.Select2(), required=True),
    'subject': f.ModelMultipleChoiceField(queryset=Subject.objects.all(), widget=autocomplete.ModelSelect2Multiple(),
                                          required=True),
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


def get_sem(today_date, year_of_foundation):
    course = int(diff_month(today_date, year_of_foundation)) // 12 + 1
    semester = course * 2 - 1 if int(diff_month(today_date, year_of_foundation)) % 12 <= 4 else course * 2
    return semester


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


def today():
    return datetime.date.today()


def age(born):
    return today().year - born.year - ((today().month, today().day) < (born.month, born.day))
