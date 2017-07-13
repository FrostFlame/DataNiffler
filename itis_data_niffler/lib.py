from datetime import datetime

from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, ModelMultipleChoiceField


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
        if isinstance(self.fields[field], (ModelChoiceField, ModelMultipleChoiceField)):
            try:
                self.fields[field].queryset = self.fields[field].queryset.filter(
                    **{'id': getattr(instance, field).id})
            except:
                try:
                    self.fields[field].queryset = self.fields[field].queryset.filter(
                        **{'id__in': getattr(instance, field).all().values('id')})
                except:
                    raise ValidationError('PLease Tell me about it!')