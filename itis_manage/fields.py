from dal import autocomplete
from django import forms

from itis_manage.models import Subject, NGroup

SEMESTER_CHOICES = [(i, str(i)) for i in range(1, 9)]
TYPE_OF_SUBJECT = (
    ('pra', 'Практическая часть'),
    ('ekz', 'Экзаменационная часть')
)
BLANK = [('', '')]

ADD_THEME_FORM_FIELDS = {
    'semester': forms.ChoiceField(choices=BLANK + SEMESTER_CHOICES, initial='',
                                  widget=autocomplete.Select2(), required=True),
    'subject': forms.ModelChoiceField(queryset=Subject.objects.all(),
                                      widget=autocomplete.ModelSelect2(),
                                      required=True),
}
ADD_PROGRESS_STUDENT_FIELDS = {
    'magister': forms.BooleanField(widget=forms.CheckboxInput, required=False),
    'group': forms.ModelChoiceField(queryset=NGroup.objects.all(),
                                    widget=autocomplete.ModelSelect2(url='manage:ajax-groups')),
    'semester': forms.ChoiceField(choices=BLANK + SEMESTER_CHOICES, initial='', widget=autocomplete.Select2(),
                                  required=True),
    'type': forms.ChoiceField(choices=TYPE_OF_SUBJECT, widget=autocomplete.Select2(), initial='ekz', ),
}
