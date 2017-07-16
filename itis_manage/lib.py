from django.contrib import messages
from django.contrib.auth.models import User

from itis_manage.forms import PersonForm, StudentForm, MagistrForm, LabRequestForm
from itis_manage.models import Student, LaboratoryRequest

# FIELDS

LAB_REQUEST_FIELDS = LaboratoryRequest._meta.fields


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
            student = ctx['student_form'].save(**{'person': person})
            if ctx['magistr_form'].is_valid():
                ctx['magistr_form'].save(**{'student': student})
    return person


def lab_post(request, ctx, form=LabRequestForm, **kwargs):
    lab_request_object = None
    if request.method == "POST":
        ctx['lab_form'] = form(**kwargs)
        if ctx['lab_form'].is_valid():
            lab_request_object = ctx['lab_form'].save()
        else:
            messages.add_message(request, messages.ERROR, ctx['lab_form'].errors['__all__'])
    return lab_request_object, ctx


def get_list_aj(val):
    return [int(i) for i in val.split(',')]


def get_set_sem(val):
    c = []
    for i in val:
        c.append((i - 1) * 2 + 1)
        c.append((i - 1) * 2 + 2)
    return c


def get_set_sem_on(val, sem):
    c = []
    for i in val:
        c.append((i - 1) * 2 + sem)
    return c
