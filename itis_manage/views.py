from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect as Redirect
from itis_manage.models import Semester, Laboratory
from itis_manage.forms import GroupForm, LaboratoryForm, LabRequestForm
from itis_manage.models import NGroup, LaboratoryRequests
from itis_manage.forms import MagistrForm
from django.shortcuts import render, get_object_or_404
from itis_manage.forms import UserForm, StudentForm, PersonForm, SimpleForm
from itis_manage.lib import get_unique_object_or_none, person_student_save, lab_post
from itis_manage.models import Person, Student, Magistrate

LOGIN_URL = reverse_lazy('data:login')


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


@login_required(login_url=reverse_lazy('data:login'))
def index(request):
    return HttpResponse("index")


def view_person(request, person_id="add"):
    ctx = {}
    ctx['person_form'] = PersonForm()
    ctx['student_form'] = StudentForm()
    ctx['magistr_form'] = MagistrForm()
    if person_id == 'add' and request.method == 'GET':
        return render(request, 'templates/add_student.html', ctx)
    elif person_id == 'add':
        person = person_student_save(ctx, request)
        if person is not None:
            return Redirect(reverse('manage:edit-add-delete-person', args=(person.id,)))
        else:
            return render(request, 'templates/add_student.html', ctx)
    person = get_object_or_404(Person, pk=person_id)
    student = get_unique_object_or_none(Student, **{'person': person.id})
    magistr = get_unique_object_or_none(Magistrate, **{'student': student.id})
    if request.method == 'GET':
        ctx['person_form'] = PersonForm(instance=person)
        if student:
            ctx['student_form'] = StudentForm(instance=student)
        if magistr:
            ctx['magistr_form'] = MagistrForm(instance=magistr)
    else:
        person_student_save(ctx, request, person, student, magistr)
    return render(request, 'templates/add_student.html', ctx)


def try_crispy_form(request):
    return render(request, 'crispy_form_example.html', {'form': SimpleForm()})


@login_required(login_url=reverse_lazy('data:login'))
def add_group(request):
    args = {'group_form': GroupForm()}
    if request.method == 'GET':
        return render(request, 'itis_manage/add_group.html', args)
    if request.method == 'POST':
        group = GroupForm(data=request.POST)
        group.save()
        return render(request, 'itis_manage/add_group.html', args)


@login_required(login_url=reverse_lazy('data:login'))
def edit_group(request, group_id=''):
    group = get_object_or_404(NGroup, pk=group_id)
    args = {}
    args['group_form'] = GroupForm(instance=group)
    if request.method == 'GET':
        return render(request, 'itis_manage/edit_group.html', args)
    if request.method == 'POST':
        group = GroupForm(request.POST, instance=group)
        group.save()
        return Redirect(reverse('manage:edit-group', args=(group_id,)))


@login_required(login_url=reverse_lazy('manage:login'))
def add_subject(request):
    args = {}
    args['semesters'] = Semester.objects.all()
    if request.method == 'GET':
        return render(request, 'itis_manage/add_subject.html', args)


@login_required(login_url=LOGIN_URL)
def lab_request(request, lab_id=None):
    ctx = {}
    params = {'data': request.POST}
    ctx['lab_form'] = LabRequestForm()
    if lab_id == 'add':
        lab_request_object, ctx = lab_post(request, ctx, **params)
        if lab_request_object is not None:
            return Redirect(reverse('manage:lab-request-add-edit-delete', args=(lab_request_object.id,)))
    else:
        lab_req = get_object_or_404(LaboratoryRequests, pk=lab_id)
        params['instance'] = lab_req
        ctx['lab_form'] = LabRequestForm(instance=lab_req)
        lab_request_object, ctx = lab_post(request, ctx, **params)
    return render(request, 'templates/add_lab_request.html', ctx)


@login_required(login_url=LOGIN_URL)
def lab_view(request, lab_id):
    ctx = {}
    params = {'data': request.POST}
    ctx['lab_form'] = LaboratoryForm()
    if lab_id == 'add':
        lab_request_object, ctx = lab_post(request, ctx, form=LaboratoryForm, **params)
        if lab_request_object is not None:
            return Redirect(reverse('manage:add-edit-delete-lab', args=(lab_request_object.id,)))
    else:
        lab_req = get_object_or_404(Laboratory, pk=lab_id)
        params['instance'] = lab_req
        ctx['lab_form'] = LaboratoryForm(instance=lab_req)
        lab_request_object, ctx = lab_post(request, ctx, form=LaboratoryForm, **params)
    return render(request, 'templates/add_lab.html', ctx)


def lab_requests(request):
    return HttpResponse('Lab requests')


def view_persons(request):
    return HttpResponse('Persons')
