from django.contrib.auth.models import User

from itis_manage.forms import PersonForm, StudentForm, MagistrForm
from itis_manage.models import Student


def get_unique_object_or_none(model=User, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except:
        return None


def person_student_save(ctx, request, person=None, student=None, magistr=None):
    ctx['person_form'] = PersonForm(data=request.POST, instance=person)
    ctx['student_form'] = StudentForm(data=request.POST, instance=student)
    ctx['magistr_form'] = MagistrForm(data=request.POST, instance=magistr)
    if ctx['person_form'].is_valid():
        person = ctx['person_form'].save()
        if ctx['student_form'].is_valid():
            ctx['student_form'].save(**{'person': person})
            if ctx['magistr_form'].is_valid():
                ctx['magistr_form'].save(**{'student': student})
    return person
