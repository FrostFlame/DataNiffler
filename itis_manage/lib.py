from django.contrib.auth.models import User

from itis_manage.forms import PersonForm, StudentForm
from itis_manage.models import Student


def get_unique_object_or_none(model=User, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except:
        return None


def person_student_save(ctx, request, person=None, f=None):
    ctx['person_form'] = PersonForm(data=request.POST, instance=person)
    ctx['student_form'] = StudentForm(data=request.POST, instance=f)
    if ctx['person_form'].is_valid():
        person = ctx['person_form'].save()
        if ctx['student_form'].is_valid():
            ctx['student_form'].save(**{'person': person})
    return person
