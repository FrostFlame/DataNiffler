from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect as Redirect
from django.shortcuts import render, render_to_response as render_resp, get_object_or_404
from django.views.generic import View

from itis_manage.forms import UserForm, StudentForm, PersonForm
from itis_manage.lib import get_unique_object_or_none
from itis_manage.models import Person, Student


def auth_login(request):
    form = UserForm()
    if request.method == 'GET':
        return render(request, 'login.html', context={'form': form})
    else:
        form = UserForm(data=request.POST)
        if form.authorize(request):
            return Redirect(reverse('manage:index'))
        else:
            return render(request, 'login.html', {'form': form})


@login_required(login_url=reverse_lazy('manage:login'))
def index(request):
    return HttpResponse("index")


def add_person(request):
    ctx = {}
    ctx['person_form'] = PersonForm()
    ctx['student_form'] = StudentForm()
    return render(request, 'itis_manage/templates/add_student.html', ctx)


def view_person(request, person_id):
    ctx = {}
    ctx['person_form'] = PersonForm()
    ctx['student_form'] = StudentForm()
    person = get_object_or_404(Person, pk=person_id)
    if request.method == 'GET':
        student = get_unique_object_or_none(Student, **{'person': person.id})
        ctx['person_form'] = PersonForm(instance=person)
        if student:
            ctx['student_form'] = StudentForm(instance=student)
    else:
        f = get_unique_object_or_none(Student, **{'person': person})

        ctx['person_form'] = PersonForm(data=request.POST, instance=person)
        ctx['student_form'] = StudentForm(data=request.POST, instance=f)
        if ctx['person_form'].is_valid():
            ctx['person_form'].save()
            if ctx['student_form'].is_valid():
                ctx['student_form'].save(**{'person': person})
    return render(request, 'itis_manage/templates/add_student.html', ctx)
