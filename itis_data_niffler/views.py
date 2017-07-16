from datetime import datetime
from functools import reduce

from django.contrib import messages
from django.db.models import Max, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import FormView

from itis_data_niffler.forms import StudentStatsCriteriaForm, TeacherStatsCriteriaForm
from itis_data_niffler.lib import semesters, diff_month, make_form, STUDENT_STATS_SCORE_FIELDS
from practice2017.lib import age
from itis_manage.forms import PersonForm, StudentForm, MagistrForm, LaboratoryForm, LabRequestForm
from itis_manage.lib import get_unique_object_or_none, get_set_sem
from itis_manage.models import Person, Student, Magistrate, Laboratory, LaboratoryRequest, NGroup, TeacherSubject, \
    AdditionalSession, Commission
from itis_manage.models import SemesterSubject, Progress, Subject

MARK_THRESHOLDS = (0, 0, 0,
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
        lab_req = get_object_or_404(LaboratoryRequest, pk=lab_id)
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
                student_rating[student.id].update({'final': student_score / progresses.count()})
            print(student_rating.items())
            student_rating = sorted(student_rating.items(), key=lambda x: x[1]['final'], reverse=True)
            ctx['student_rating'] = student_rating
            ctx['student_subjects'] = SemesterSubject.objects.filter(id__in=subjects).order_by('id')
            form.fields['subject'].queryset = form.cleaned_data['subject']
            ctx['form'] = form
    return render(request, 'itis_data_niffler/templates/students_stats_score.html', ctx)


class StudentStatsCriteriaView(FormView):
    model = Student
    template_name = 'student_stats_criteria.html'
    form_class = StudentStatsCriteriaForm

    def form_valid(self, form):
        qs = Student.objects.all()

        course = int(form.cleaned_data['course'])
        semester = course * 2 + int(form.cleaned_data['course_semester'])
        year_start, year_end = form.cleaned_data['year_start'], form.cleaned_data['year_end']

        # Students studied on the given course during the given period of time
        qs = qs.filter(group__year_of_foundation__range=[year_start - (course - 1), year_end - (course - 1)])

        students = qs

        # Prefetch all the fields we will now process for efficiency
        students.prefetch_related('dopkas', 'commissions', 'attendance', 'progresses')
        for stud in students:
            stud.events = stud.events.filter(date__year__range=[year_start, year_end])
            stud.dopkas = stud.dopkas.filter(subject__semester__semester=semester)
            stud.commissions = stud.commissions.filter(subject__semester__semester=semester)
            stud.attendance = stud.attendance.filter(
                _class__teacher_group__subject__subject__semester__semester=semester)
            stud.progresses = stud.progresses.filter(semester_subject__semester__semester=semester)

            stud.balls = reduce(lambda ev1, ev2: ev1.balls + ev2.balls, stud.events, 0)
            stud.five_count = len(list(filter(
                lambda progress: progress.practice + progress.exam >= MARK_THRESHOLDS[5], stud.progresses)))

        ctx = {
            'form': form,
            'students': students
        }

        # TODO columns

        return self.render_to_response(self.get_context_data(**ctx))


class TeacherStatsCriteriaView(FormView):
    template_name = 'generic_stats_criteria.html'
    form_class = TeacherStatsCriteriaForm

    def form_valid(self, form):
        qs = Person.objects.filter(teacher_subjects__isnull=False)
        subject = form.cleaned_data.get('subject', None)
        if subject is not None:
            qs = qs.filter(teacher_subjects__subject__subject=subject)

        teachers = qs
        teachers.prefetch_related('teacher_subjects')
        for teacher in teachers:
            teacher.num_hours = sum([subject.lesson_count for subject in teacher.teacher_subjects])
            teacher.num_subjects = len(teacher.teacher_subjects)
            teacher.age = age(teacher.birth_date)

            teacher_subjects = teacher.teacher_subjects if not subject \
                else TeacherSubject.objects.filter(subject__subject=subject)
            teacher_subjects = teacher_subjects.filter(type=TeacherSubject.LECTURE)

            teacher_subjects.prefetch_related('groups')
            scores = []
            teacher.dopkas = 0
            teacher.commissions = 0
            for teacher_subject in teacher_subjects:
                progresses = Progress.objects.filter(Q(semester_subject=teacher_subject.subject)
                                                     & Q(student__group__in=teacher_subject.groups))
                dopkas = AdditionalSession.objects.filter(Q(semester_subject=teacher_subject.subject)
                                                          & Q(student__group__in=teacher_subject.groups))
                commissions = Commission.objects.filter(Q(semester_subject=teacher_subject.subject)
                                                        & Q(student__group__in=teacher_subject.groups))

                teacher.dopkas += len(dopkas)
                teacher.commissions += len(commissions)
                scores += [progress.practice + progress.exam for progress in progresses]

            teacher.avg_score = sum(scores) / len(scores)

        ctx = {
            'form': form,
            'objects': teachers,
            'fields': {
                'Имя': 'full_name',
                'Число предметов': 'num_subjects',
                'Возраст': 'age',
                'Число часов': 'num_hours',
                'Страна': 'city.country',
                'Город': 'city',
                'Стаж': 'experience.exp_total',
                'Средний балл': 'avg_score',
                'Доп. сессии': 'dopkas',
                'Комиссии': 'commissions'
            }
        }

        return self.render_to_response(self.get_context_data(**ctx))


def group_rating(request):
    init = {'base_fields': STUDENT_STATS_SCORE_FIELDS,
            'field_order': ('date_begin', 'date_end', 'course', 'semester', 'subject')}
    ctx = {'form': make_form(form_name='form', form_init=init)}
    group_rating = {}
    group_score_by_subjects = {}
    subjects = None
    if request.method == 'POST':
        form = ctx['form'](data=request.POST)
        if form.is_valid():
            courses = list(form.cleaned_data['course'])
            semester = form.cleaned_data['semester']
            subjects = form.cleaned_data['subject']
            year_start, year_end = form.cleaned_data['date_begin'], form.cleaned_data['date_end']
            years = []
            for course in courses:
                for year in list(range(year_start + 1, year_end + 1)):
                    years.append(year - int(course))
                years = list(set(years))
            groups = NGroup.objects.all().filter(
                year_of_foundation__in=years)
            sems = [int(course - 1) * 2 + 1 for course in courses] if semester in [1, 2] else get_set_sem(
                list(map(int, courses)))
            semester_subject = SemesterSubject.objects.filter(subject__in=subjects, semester__in=sems)
            for group in groups:

                group_score = 0
                progresses = Progress.objects.all().filter(semester_subject__in=semester_subject,
                                                           student__in=group.group_students.all())
                for p in progresses:
                    group_score += p.exam + p.practice
                if progresses.count() != 0:
                    if not group_rating.get(group_score / progresses.count()):
                        group_rating[group_score / progresses.count()] = []
                        group_rating[group_score / progresses.count()].append(group)
                    else:
                        group_rating[group_score / progresses.count()].append(group)
                group_score_by_subjects[group.id] = []
                for subject in subjects:
                    group_subject_score = 0
                    subject_progresses = Progress.objects.filter(semester_subject__subject=subject,
                                                                 student__in=group.group_students.all())
                    for p in subject_progresses:
                        group_subject_score += p.exam + p.practice
                    if subject_progresses.count() != 0:
                        group_subject_score = group_subject_score / subject_progresses.count()
                        group_score_by_subjects[group.id].append((group_subject_score, subject))
                    else:
                        group_score_by_subjects[group.id].append(('-', subject))
                    print(group_score_by_subjects)
            group_rating = sorted(group_rating.items(), key=lambda x: x[0], reverse=True)
            form.fields['subject'].queryset = form.cleaned_data['subject']
        return render(request, 'itis_data_niffler/templates/group_rating.html',
                      {'form': form, 'group_rating': group_rating,
                       'group_score_by_subjects': group_score_by_subjects, 'subjects': subjects})
    return render(request, 'itis_data_niffler/templates/group_rating.html', ctx)
