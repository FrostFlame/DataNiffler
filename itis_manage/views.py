from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect as Redirect
from django.http import JsonResponse
from itis_data_niffler.lib import make_form
from itis_manage.models import TeacherSubject
from itis_manage.fields import ADD_THEME_FORM_FIELDS, ADD_PROGRESS_STUDENT_FIELDS
from itis_manage.models import Subject, SemesterSubject, ThemeOfEducation, Progress
from django.views.generic import *
from itis_manage.models import Laboratory
from itis_manage.forms import GroupForm, LaboratoryForm, LabRequestForm, ThemeOfEducationForm, \
    TeacherForm, get_dynamic_formset, ProgressForm, get_dynamic_model_form, MetaProgressPractice, MetaExamPractice
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


@login_required(login_url=LOGIN_URL)
def add_theme_subject(request):
    ctx = {'form': make_form('form', {'base_fields': ADD_THEME_FORM_FIELDS, 'field_order': ('semester', 'subject')})}
    ThemeFormSet = formset_factory(ThemeOfEducationForm, extra=1, can_delete=True)
    if request.method == 'POST':
        form = ctx['form'](data=request.POST)
        formset = None
        kwargs = {}
        if form.is_valid():
            kwargs = {'initial': ThemeOfEducation.objects.filter(
                semester_subject__subject=form.cleaned_data['subject']).values('name', 'id').order_by(
                'id')}
            formset = ThemeFormSet(**kwargs)
            if 'save' in request.POST:
                kwargs['data'] = request.POST
                formset = ThemeFormSet(**kwargs)
                for f in formset:
                    if f.is_valid():
                        if 'name' in f.initial:
                            instance = ThemeOfEducation.objects.get(
                                semester_subject__subject=form.cleaned_data['subject'], name=f.initial['name'])
                            data = {}
                            if 'name' in f.cleaned_data:
                                fow = ThemeOfEducationForm(data={'name': f.cleaned_data['name']}, instance=instance)
                            else:
                                fow = ThemeOfEducationForm(data={'name': f.initial['name']}, instance=instance)
                            fow.save()
                        else:
                            if 'name' in f.cleaned_data:
                                forw = ThemeOfEducation.objects.create(name=f.cleaned_data['name'],
                                                                       semester_subject=SemesterSubject.objects.get(
                                                                           subject=form.cleaned_data['subject']))
                for f in formset.deleted_forms:
                    if 'name' in f.cleaned_data:
                        ThemeOfEducation.objects.filter(
                            (Q(name=f.cleaned_data['name']) | Q(name=f.cleaned_data['name'])) & Q(
                                semester_subject__subject=form.cleaned_data['subject'])).delete()
            kwargs['initial'] = ThemeOfEducation.objects.filter(
                semester_subject__subject=form.cleaned_data['subject']).values('name', 'id').order_by(
                'id')

            ctx['formset'] = ThemeFormSet(**kwargs)
            form.fields['subject'].queryset = Subject.objects.filter(id=form.cleaned_data['subject'].id)
            ctx['form'] = form

    return render(request, 'templates/add_theme_of_education.html', ctx)


@login_required(login_url=reverse_lazy('data:login'))
def add_subject(request):
    args = {}
    if request.method == 'GET':
        return render(request, 'itis_manage/add_subject1.html', args)
    if request.method == 'POST':
        name = request.POST.get('name').title()
        if Subject.objects.filter(name=name).exists():
            args['err'] = 'subject_exists'
            return render(request, 'itis_manage/add_subject1.html', args)

        args['name'] = name
        request.session['name'] = name

        args['semesters'] = list(map(int, request.POST.getlist('semesters')))
        request.session['semesters'] = args['semesters']

        args['teacher_form'] = TeacherForm()
        args['teachers'] = Person.objects.all().values('id', 'name', 'surname', 'third_name')

        return render(request, 'itis_manage/add_subject2.html', args)


@login_required(login_url=reverse_lazy('data:login'))
def add_subject_semesters(request):
    if request.method == 'POST':
        subject = Subject(name=request.session['name'])
        subject.save()

        semesters = list(map(int, request.session['semesters']))
        for sem in semesters:
            add_points = request.POST.get('additional_points' + str(sem))
            if add_points == 'on':
                add_points = True
            else:
                add_points = False

            exam = request.POST.get('exam' + str(sem))
            sem_subj = SemesterSubject(semester=sem, subject=subject, additional_points=add_points, type_of_exam=exam)
            sem_subj.save()

            teachers = list(map(int, request.POST.getlist('teacher' + str(sem))))
            for t in teachers:
                teacher = Person.objects.get(id=t)
                teacher_type = request.POST.get('type' + str(sem) + '_' + str(t))
                if teacher_type == 'LP':
                    teacher_subject1 = TeacherSubject(subject=sem_subj, person=teacher, type='L')
                    teacher_subject2 = TeacherSubject(subject=sem_subj, person=teacher, type='P')
                    teacher_subject1.save()
                    teacher_subject2.save()
                else:
                    teacher_subject = TeacherSubject(subject=sem_subj, person=teacher, type=teacher_type)
                    teacher_subject.save()

        return render(request, 'itis_manage/add_subject1.html')


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


def add_scores(request):
    ctx = {
        'form': make_form('form', {'base_fields': ADD_PROGRESS_STUDENT_FIELDS,
                                   'field_order': ('magister', 'group', 'semester', 'type')})}
    if request.POST:
        form = ctx['form'](request.POST)
        if form.is_valid():
            magister = form.cleaned_data['magister']
            group = form.cleaned_data['group']
            semester = form.cleaned_data['semester']
            type = form.cleaned_data['type']
            model_form = get_dynamic_model_form(ProgressForm,
                                                MetaProgressPractice) if type == 'ekz' else get_dynamic_model_form(
                ProgressForm, MetaExamPractice)
            students = Student.objects.filter(group=group,
                                              person__status__name__contains='Студент' if not magister else 'Магистр', ). \
                order_by('person__surname')

            semester_subjects = SemesterSubject.objects.filter(semester=int(semester)).order_by('subject__name')

            progresses = Progress.objects.filter(semester_subject__semester=int(semester),
                                                 student__in=students).order_by(
                'semester_subject__subject__name')

            ctx['formsformsets'] = {}

            ctx['semester_subjects'] = semester_subjects

            for student in students:
                if 'save' in request.POST:
                    ctx['formsformsets'].update(
                        {student.id: get_dynamic_formset(Progress, model_form, semester_subjects.count())(
                            prefix=student.id, queryset=progresses.filter(
                                student=student, ).order_by('semester_subject__subject__name'), data=request.POST)})
                    if ctx['formsformsets'][student.id].is_valid():
                        instances = ctx['formsformsets'][student.id]
                        i = 0
                        for instance in instances:
                            instance.instance.student = student
                            instance.instance.semester_subject= semester_subjects[i]
                            instance.save()
                            i += 1
                else:
                    ctx['formsformsets'].update(
                        {student.id: get_dynamic_formset(Progress, model_form, semester_subjects.count())(
                            prefix=student.id, queryset=progresses.filter(
                                student=student).order_by('semester_subject__subject__name'), )})
            ctx['form'] = form
    return render(request, 'templates/add_score.html', ctx)
