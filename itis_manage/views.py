from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect as Redirect
from django.http import JsonResponse
from itis_manage.models import Subject, SemesterSubject, Course, Status
from django.views.generic import CreateView, UpdateView
from itis_manage.models import Laboratory
from itis_manage.forms import GroupForm, LaboratoryForm, LabRequestForm, TeacherForm
from itis_manage.models import NGroup, LaboratoryRequest
from itis_manage.forms import MagistrForm
from django.shortcuts import render, get_object_or_404
from itis_manage.forms import UserForm, StudentForm, PersonForm, SimpleForm
from itis_manage.lib import get_unique_object_or_none, person_student_save, lab_post
from itis_manage.models import Person, Student, Magistrate

LOGIN_URL = reverse_lazy('data:login')


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = LOGIN_URL


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
    magistr = get_unique_object_or_none(Magistrate, **{'student': student.id if student else None})

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


class AddGroupView(CustomLoginRequiredMixin, CreateView):
    model = NGroup
    form_class = GroupForm
    template_name = 'templates/add_group.html'

    def get_success_url(self):
        return reverse_lazy('manage:edit-group', args=(self.object.id,))


class EditGroupView(CustomLoginRequiredMixin, UpdateView):
    model = NGroup
    form_class = GroupForm
    template_name = 'templates/add_group.html'

    def get_success_url(self):
        return reverse_lazy('manage:edit-group', args=(self.object.id,))


@login_required(login_url=reverse_lazy('data:login'))
def add_subject(request):
    if request.method == 'GET':
        return render(request, 'itis_manage/add_subject1.html')
    if request.method == 'POST':
        name = request.POST.get('name').title()
        new_subject = Subject.objects.get_or_create(name=name)
        args = {}
        args['semesters'] = list(map(int, request.POST.getlist('semesters')))
        args['name'] = name
        args['teacher_form'] = TeacherForm()

        return render(request, 'itis_manage/add_subject2.html', args)


@login_required(login_url=reverse_lazy('data:login'))
def add_subject_semesters(request):
    if request.method == 'POST':

        return render(request, 'itis_manage/add_subject2.html', args)


def teachers_ajax(request):
    name = request.GET.get('q', '')
    persons = None
    for term in name.split():
        persons = Person.objects.filter(Q(name__icontains=term) | Q(surname__icontains=term) |
                                        Q(third_name__icontains=term)).values('id', 'name', 'surname', 'third_name')
    return JsonResponse({'results': list(persons)})


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
        lab_req = get_object_or_404(LaboratoryRequest, pk=lab_id)
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
