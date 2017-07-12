from django.contrib import messages
from django.shortcuts import render, get_object_or_404

from itis_manage.forms import PersonForm, StudentForm, MagistrForm
from itis_manage.lib import get_unique_object_or_none
from itis_manage.models import Person, Student, Magistrate


def view_person(request, person_id=None):
    ctx = {'read': True}
    if request.method == 'GET':
        person = get_object_or_404(Person, pk=person_id)
        student = get_unique_object_or_none(Student, **{'person': person.id})
        ctx['person_form'] = PersonForm(instance=person, readonly=True)
        if student:
            ctx['student_form'] = StudentForm(instance=student, readonly=True)
            magistr = get_unique_object_or_none(Magistrate, **{'student': student.id})
            if magistr:
                ctx['magistr_form'] = MagistrForm(instance=magistr, readonly=True)
    else:
        messages.add_message(request, messages.INFO, 'POST method not allowed here!')
    return render(request, 'templates/add_student.html', ctx)


def view_persons(request):
    return None
