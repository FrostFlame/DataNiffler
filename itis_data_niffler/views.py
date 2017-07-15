from functools import reduce

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, FormView

from itis_data_niffler.forms import StudentStatsCriteriaForm
from itis_manage.forms import PersonForm, StudentForm, MagistrForm, LaboratoryForm, LabRequestForm
from itis_manage.lib import get_unique_object_or_none, LAB_REQUEST_FIELDS, lab_post
from itis_manage.models import Person, Student, Magistrate, Laboratory, LaboratoryRequests

from django.db.models import Max
from django.shortcuts import render
from datetime import datetime, date, time
from itis_data_niffler.lib import semesters, diff_month, make_form, STUDENT_STATS_SCORE_FIELDS, SEMESTER_CHOICES, \
    SEMESTER_BOTH
from itis_manage.models import SemesterSubject, Progress, Subject

import django.forms as f

MARK_TRESHOLDS = (0, 0, 0,
                  56,
                  71,
                  86
                  )


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


def common_rating(request):
    common_students_rating = {}
    semesters_of_current_course = [1, 2]
    if 'course' in request.GET:
        semesters_of_current_course = semesters(request.GET.get('course'))
    today_year = datetime.today()
    for student in Student.objects.all():
        year_of_foundation = student.group.year_of_foundation
        course = int(diff_month(today_year, year_of_foundation)) // 12 + 1
        semester = course * 2 - 1 if int(diff_month(today_year, year_of_foundation)) % 12 <= 4 else course * 2
        if semester == max(semesters_of_current_course):
            student_score = 0
            for semester_subject in SemesterSubject.objects.all():
                if semester_subject.semester.semester in list(map(str, semesters_of_current_course)):
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
    return render(request, 'itis_data_niffler/templates/common_rating.html',
                  {'common_students_score_rating': common_students_rating})


def subject_rating(request):
    subject_students_rating = {}
    subjects_scores = {}
    subject = None
    if 'subject' in request.GET:
        subject = Subject.objects.get(name=request.GET['subject'])
    else:
        subject = Subject.objects.get(name='MATH')
    today_year = datetime.today()
    for student in Student.objects.all():
        semesters_for_subject = SemesterSubject.objects.all().filter(subject=subject).only(
            'semester__semester').aggregate(Max('semester')).get('semester__max')

        year_of_foundation = student.group.year_of_foundation
        course = int(diff_month(today_year, year_of_foundation)) // 12 + 1
        semester = course * 2 - 1 if int(diff_month(today_year, year_of_foundation)) % 12 <= 4 else course * 2
        if semester >= semesters_for_subject:
            student_score = 0
            for p in Progress.objects.all().filter(student=student, semester_subject__subject=subject):
                student_score += p.exam + p.practice
            average_student_score = student_score / Progress.objects.all().filter(student=student,
                                                                                  semester_subject__subject=subject).count()
            if not subject_students_rating.get(average_student_score):
                subject_students_rating[average_student_score] = []
            subject_students_rating[average_student_score].append(student)
    subject_students_rating = sorted(subject_students_rating.items(), key=lambda items: items[0], reverse=True)
    subjects = Subject.objects.all()
    return render(request, 'itis_data_niffler/templates/subject_rating.html',
                  {'subjects_scores': subjects_scores,
                   'subject_students_rating': subject_students_rating, 'subjects': subjects})


def view_persons(request):
    return None


def index(request):
    return HttpResponse("index")


def lab_view(request, lab_id):
    ctx = {'read': True, 'lab_form': LaboratoryForm()}
    if request.method == "GET":
        lab_req = get_object_or_404(Laboratory, pk=lab_id)
        ctx['lab_form'] = LaboratoryForm(instance=lab_req, readonly=True)
    else:
        messages.add_message(request, messages.INFO, 'POST method not allowed here!')
    return render(request, 'templates/add_lab.html', ctx)


def lab_request_view(request, lab_id):
    ctx = {'read': True, 'lab_form': LabRequestForm()}
    if request.method == 'GET':
        lab_req = get_object_or_404(LaboratoryRequests, pk=lab_id)
        ctx['lab_form'] = LabRequestForm(instance=lab_req, readonly=True)
    else:
        messages.add_message(request, messages.INFO, 'POST method not allowed here!')
    return render(request, 'templates/add_lab_request.html', ctx)


def lab_requests(request):
    return HttpResponse('Labs')


def students_stats_score(request):
    init = {'base_fields': STUDENT_STATS_SCORE_FIELDS,
            'field_order': ('date_begin', 'date_end', 'course', 'semester', 'subject')}
    ctx = {'form': make_form(form_name='form', form_init=init)}

    if request.method == 'POST':
        form = ctx['form'](data=request.POST)
        ctx['form'] = form
        if form.is_valid():
            courses = form.cleaned_data['course']  # May list
            semester = form.cleaned_data['semester']  # May 3 Both
            subjects = form.cleaned_data['subject']  # May list
            year_start, year_end = int(form.cleaned_data['date_begin']), int(form.cleaned_data['date_end'])

            years_list = set()  # Group years
            for i in courses:
                for j in list(range(year_start, year_end)):
                    years_list.add(j - int(i) + 1)
            kwargs = {
                'group__year_of_foundation__in': years_list,
                'progresses__semester_subject__subject__in': subjects,
            }
            students = Student.objects.filter(**kwargs).order_by('progresses__semester_subject__subject')
            student_rating = {}
            for student in students:
                progresses = Progress.objects.filter(student=student, semester_subject__subject__in=subjects)
                student_score = 0
                student_rating[student.id] = {}
                for p in progresses:
                    student_score += p.get_final_points()
                    student_rating[student.id].update({p.semester_subject.id: p.get_final_points()})
                student_rating[student.id].update({'final': student_score})
                # student_score / progresses.count()
            print(student_rating.items())
            student_rating = sorted(student_rating.items(), key=lambda x: x[1]['final'], reverse=True)
            ctx['student_rating'] = student_rating
            ctx['student_subjects'] = SemesterSubject.objects.filter(id__in=subjects).order_by('id')
    return render(request, 'itis_data_niffler/templates/students_stats_score.html', ctx)


class StudentStatsCriteriaView(FormView):
    model = Student
    template_name = 'students_stats_criteria.html'
    form_class = StudentStatsCriteriaForm

    def form_valid(self, form):
        qs = Student.objects.all()

        semester = int(form.cleaned_data['course']) * 2 + int(form.cleaned_data['course_semester'])
        year_start, year_end = form.cleaned_data['year_start'], form.cleaned_data['year_end']

        qs = qs.filter(group__year_of_foundation__range=[year_start - semester // 2, year_end - semester // 2])

        students = qs
        for stud in students:
            stud.events = stud.events.filter(date__year__range=[year_start, year_end])
            stud.dopkas = stud.dopkas.filter(subject__semester__semester=semester)
            stud.commissions = stud.commissions.filter(subject__semester__semester=semester)
            stud.attendance = stud.attendance.filter(
                _class__teacher_group__subject__subject__semester__semester=semester)
            stud.progresses = stud.progresses.filter(semester_subject__semester__semester=semester)

            stud.balls = reduce(lambda ev1, ev2: ev1.balls + ev2.balls, stud.events, 0)
            stud.five_count = len(list(filter(
                lambda progress: progress.practice + progress.exam >= MARK_TRESHOLDS[5], stud.progresses)))

        ctx = {
            'form': form,
            'students': students
        }

        # TODO columns

        return self.render_to_response(self.get_context_data(**ctx))

def group_rating(request):
    if request.method=='GET':
        init = {'base_fields': STUDENT_STATS_SCORE_FIELDS,
                'field_order': ('date_begin', 'date_end', 'course', 'semester', 'subject')}
        ctx = {'form': make_form(form_name='form', form_init=init)}
        return render(request, 'itis_data_niffler/templates/group_rating.html', ctx)
    else:
        return HttpResponse('hi')
