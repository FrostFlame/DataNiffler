from datetime import datetime

from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, ModelMultipleChoiceField, ChoiceField, TypedChoiceField


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
