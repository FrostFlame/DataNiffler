from dal import autocomplete
from django import forms

from itis_manage.models import Subject

SEMESTER_CHOICES = ((i, str(i)) for i in range(1, 9))

ADD_THEME_FORM_FIELDS = {
    'semester': forms.ChoiceField(choices=SEMESTER_CHOICES, widget=autocomplete.Select2(), required=True),
    'subject': forms.ModelChoiceField(queryset=Subject.objects.all(),
                                      widget=autocomplete.ModelSelect2(),
                                      required=True),
}
