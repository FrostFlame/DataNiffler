from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Avg, Sum, Max
from django.forms import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect as Redirect
from django.shortcuts import render, render_to_response as render_resp, get_object_or_404
from django.views.generic import View

from itis_manage.helper import semesters
from itis_manage.forms import UserForm, StudentForm, PersonForm, SimpleForm, GroupForm
from itis_manage.lib import get_unique_object_or_none, person_student_save
from itis_manage.models import Person, Student, Progress, Subject, SemesterSubject, NGroup


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


def view_person(request, person_id="add"):
    ctx = {}
    ctx['person_form'] = PersonForm()
    ctx['student_form'] = StudentForm()
    if person_id == 'add' and request.method == 'GET':
        return render(request, 'itis_manage/templates/add_student.html', ctx)
    elif person_id == 'add':
        person = person_student_save(ctx, request)
        if person is not None:
            return Redirect(reverse('manage:view-edit-add-student', args=(person.id,)))
        else:
            return render(request, 'itis_manage/templates/add_student.html', ctx)
    person = get_object_or_404(Person, pk=person_id)
    if request.method == 'GET':
        student = get_unique_object_or_none(Student, **{'person': person.id})
        ctx['person_form'] = PersonForm(instance=person)
        if student:
            ctx['student_form'] = StudentForm(instance=student)
    else:
        f = get_unique_object_or_none(Student, **{'person': person})
        person_student_save(ctx, request, person, f)
    return render(request, 'itis_manage/templates/add_student.html', ctx)


def try_crispy_form(request):
    return render(request, 'crispy_form_example.html', {'form': SimpleForm()})


@login_required(login_url=reverse_lazy('manage:login'))
def add_group(request):
    args = {'group_form': GroupForm()}
    if request.method == 'GET':
        return render(request, 'itis_manage/add_group.html', args)
    if request.method == 'POST':
        group = GroupForm(data=request.POST)
        group.save()
        return render(request, 'itis_manage/add_group.html', args)


@login_required(login_url=reverse_lazy('manage:login'))
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


def common_rating(request):
    common_students_rating = {}
    semesters_of_current_course = ['1', '2']
    if 'course' in request.GET:
        semesters_of_current_course = semesters(request.GET.get('course'))

    for student in Student.objects.all():

        if student.group.semester.semester in semesters_of_current_course:
            student_score = 0
            for semester_subject in SemesterSubject.objects.all():
                if semester_subject.semester.semester in semesters_of_current_course:
                    progress = Progress.objects.all().get(student=student, semester_subject=semester_subject)
                    student_score += progress.exam + progress.practice
            subjects_for_course = SemesterSubject.objects.all().filter(
                semester__semester__in=semesters_of_current_course)
            subjects_quantity = Progress.objects.all().filter(student=student,
                                                              semester_subject__in=subjects_for_course).count()
            if subjects_quantity != 0:
                if not common_students_rating.get(student_score / subjects_quantity):
                    common_students_rating[student_score / subjects_quantity] = []
                    common_students_rating[student_score / subjects_quantity].append(student)
                else:
                    common_students_rating[student_score / subjects_quantity].append(student)

    common_students_rating = sorted(common_students_rating.items(), key=lambda x: x[0], reverse=True)
    return render(request, 'itis_manage/templates/common_rating.html',
                  {'common_students_score_rating': common_students_rating})


def subject_rating(request):
    subject_students_rating = {}
    subjects_scores = {}
    subject = None
    if 'subject' in request.GET:
        subject = Subject.objects.get(name=request.GET['subject'])
    else:
        subject = Subject.objects.get(name='MATH')
    for student in Student.objects.all():
        semesters_for_subject = SemesterSubject.objects.all().filter(subject=subject).only(
            'semester__semester').aggregate(Max('semester')).get('semester__max')
        print(semesters_for_subject)
        print(student.group.semester.semester > str(semesters_for_subject))
        if student.group.semester.semester > str(semesters_for_subject):
            student_score = 0
            for p in Progress.objects.all().filter(student=student, semester_subject__subject=subject):
                student_score += p.exam + p.practice
            average_student_score = student_score / Progress.objects.all().filter(student=student,
                                                                                  semester_subject__subject=subject).count()
            print(average_student_score)
            if not subject_students_rating.get(average_student_score):
                subject_students_rating[average_student_score] = []
                subject_students_rating[average_student_score].append(student)
            else:
                subject_students_rating[average_student_score].append(student)
            print(subject_students_rating)
    subject_students_rating = sorted(subject_students_rating.items(), key=lambda items: items[0], reverse=True)
    print(subject_students_rating)
    # print(common_students_rating)
    subjects = Subject.objects.all()
    return render(request, 'itis_manage/templates/subject_rating.html',
                  {'subjects_scores': subjects_scores,
                   'subject_students_rating': subject_students_rating, 'subjects': subjects})
