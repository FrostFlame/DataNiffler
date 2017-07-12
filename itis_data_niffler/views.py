
from django.contrib import messages
from django.shortcuts import render, get_object_or_404

from itis_manage.forms import PersonForm, StudentForm, MagistrForm
from itis_manage.lib import get_unique_object_or_none
from itis_manage.models import Person, Student, Magistrate

from django.db.models import Max
from django.shortcuts import render
from datetime import datetime, date, time
from itis_data_niffler.lib import semesters, diff_month
from itis_manage.models import SemesterSubject, Progress, Subject


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
            else:
                subject_students_rating[average_student_score].append(student)
    subject_students_rating = sorted(subject_students_rating.items(), key=lambda items: items[0], reverse=True)
    subjects = Subject.objects.all()
    return render(request, 'itis_data_niffler/templates/subject_rating.html',
                  {'subjects_scores': subjects_scores,
                   'subject_students_rating': subject_students_rating, 'subjects': subjects})


def view_persons(request):
    return None


def index(request):
    return None