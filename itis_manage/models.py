import datetime
from functools import reduce

from django.db import models

from practice2017.lib import today, MARK_THRESHOLDS


class Status(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField('Страна', max_length=50, default='Россия', unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    class Meta:
        unique_together = (('name', 'country'),)

    name = models.CharField('Город', max_length=50, )
    country = models.ForeignKey(Country, related_name='country_cities', default=1, auto_created=True, null=False)

    def __str__(self):
        return self.name + ' (' + self.country.name + ')'


class Event(models.Model):
    SOCIAL = 'SO'
    SPORT = 'SP'
    ENTERTAINMENT = 'ET'
    POLITICAL = 'PO'
    OTHER = 'NA'

    EVENT_TYPES = (
        (SOCIAL, 'Социальное'),
        (SPORT, 'Спортивное'),
        (ENTERTAINMENT, 'Развлекательное'),
        (POLITICAL, 'Политическое'),
        (OTHER, 'Другое')
    )

    name = models.CharField('Название', max_length=50)
    _type = models.CharField('Тип', choices=EVENT_TYPES, default=OTHER, max_length=2)
    description = models.TextField('Описание')
    points = models.SmallIntegerField('Доп. баллы')

    date = models.DateField('Дата события')
    time = models.TimeField('Время события', null=True)
    place = models.CharField('Место проведеня', null=True, max_length=50)


class Person(models.Model):
    BIRTH_YEAR_CHOICES = [year for year in range(1960, 2018)]

    email = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=40)
    third_name = models.CharField(max_length=40)
    birth_date = models.CharField(max_length=40, null=True, blank=True)
    status = models.ManyToManyField(Status, related_name='status_persons')
    city = models.ForeignKey(City, related_name='persons_city', null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now, auto_created=True)

    events = models.ManyToManyField(Event, related_name='person_event')

    def full_name(self):
        return '%s %s %s' % (self.surname, self.name, self.third_name)

    def __str__(self):
        return '%s (%s)' % (
            self.full_name(),
            reduce(lambda a, x: str(a) + ', ' + str(x), self.status.all()) if self.status.all().count() > 0  else '')


class WorkExperience(models.Model):
    exp_before = models.PositiveSmallIntegerField()
    hire_year = models.PositiveSmallIntegerField(max_length=4)
    person = models.OneToOneField(Person, models.CASCADE, related_name='experience')

    def exp_total(self):
        return self.exp_before + (today().year - self.hire_year)


class NGroup(models.Model):
    name = models.CharField(max_length=10)
    year_of_foundation = models.IntegerField()
    curator = models.ManyToManyField(Person, related_name='curator_groups')

    def __str__(self):
        return "#%s (%s)" % (self.name, self.year_of_foundation)

    class Meta:
        unique_together = (('name', 'year_of_foundation'),)


class Student(models.Model):
    STUDYING = 'STUDYING'
    ACADEM = 'ACADEMIC LEAVE'
    DEDUCTED = 'DEDUCTED'
    EXPELLED = 'EXPELLED'

    TYPE_OF_STANDING = (
        (STUDYING, 'Учится'),
        (ACADEM, 'В академическом отпуске'),
        (DEDUCTED, 'Отчислен'),
        (EXPELLED, 'Отчислился')
    )

    BUDGET = 'BUDGET'
    GRANT = 'GRANT'
    CONTRACT = 'CONTRACT'

    FORM_OF_EDUCATION = (
        (BUDGET, 'Бюджет'),
        (GRANT, 'Грант'),
        (CONTRACT, 'Договор')
    )

    standing = models.CharField('Статус', choices=TYPE_OF_STANDING, default=STUDYING, max_length=14)
    group = models.ForeignKey(NGroup, related_name='group_students')
    person = models.OneToOneField(Person, related_name='person_student')
    form_of_education = models.CharField('Форма обучения', choices=FORM_OF_EDUCATION, default=BUDGET, max_length=8,
                                         null=True)

    def __str__(self):
        return "Студент " + self.person.__str__() + ' группа ' + self.group.__str__()


class Subject(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    subject = models.OneToOneField(Subject, related_name='course_subject')

    def __str__(self):
        return self.subject.name


class CourseRequest(models.Model):
    class Meta:
        unique_together = (('course', 'student'),)

    course = models.ForeignKey(Course, related_name='courses_requests_course')
    student = models.ForeignKey(Student, related_name='students_requests_student')
    is_active = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.datetime.now, auto_created=True)

    def __str__(self):
        return self.student.__str__() + 'requested to ' + self.course.__str__()


class Laboratory(models.Model):
    name = models.CharField(max_length=40, unique=True)
    person = models.ForeignKey(Person, related_name='person_laboratories')

    def __str__(self):
        return self.name


class LaboratoryRequest(models.Model):
    fields = ('student',
              'laboratory',
              'is_active',
              'created_at',
              )

    class Meta:
        unique_together = (('student', 'laboratory'),)

    student = models.ForeignKey('Student', related_name='student_requests_for_labs')
    laboratory = models.ForeignKey(Laboratory, related_name='laboratory_requests')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.datetime.now, auto_created=True)

    def __str__(self):
        return self.student.person.__str__() + 'requested to lab ' + self.laboratory.__str__() + ' on ' + str(
            self.created_at.date())

    def __is_active__(self):
        return 'In lab' if self.is_active else 'Waiting for accept'


class SemesterSubject(models.Model):
    EXAM = 'EX'
    NOT_DIFF_TEST = "ND"
    DIFF_TEST = "DT"

    TYPE_OF_EXAM_CHOICES = (
        (EXAM, 'Экзамен'),
        (NOT_DIFF_TEST, 'Недифференцированный зачет'),
        (DIFF_TEST, 'Дифференцированный зачет'),
    )

    subject = models.ForeignKey(Subject, related_name='subject_semesters')
    semester = models.IntegerField(choices=((i, str(i)) for i in range(1, 9)))
    type_of_exam = models.CharField(
        max_length=2,
        choices=TYPE_OF_EXAM_CHOICES,
        default=EXAM
    )
    additional_points = models.NullBooleanField()

    class Meta:
        unique_together = (('semester', 'subject'),)

    def __str__(self):
        return self.subject.name + ' #sem = ' + str(self.semester.__str__())


class Progress(models.Model):
    semester_subject = models.ForeignKey(SemesterSubject, related_name='semester_subject_progresses')
    student = models.ForeignKey(Student, related_name='progresses')
    practice = models.IntegerField()
    exam = models.IntegerField()

    class Meta:
        unique_together = (('semester_subject', 'student'),)

    def total(self):
        return self.practice + self.exam

    def gold_eligible(self):
        return self.total() >= MARK_THRESHOLDS[5]


class TeacherSubject(models.Model):
    PRACTICE = 'P'
    LECTURE = 'L'
    TYPE_CHOICES = (
        (PRACTICE, 'Практика'),
        (LECTURE, 'Лекция'),
    )
    type = models.CharField(max_length=1,
                            choices=TYPE_CHOICES,
                            default=LECTURE)

    subject = models.ForeignKey(SemesterSubject, related_name='teachers')
    person = models.ForeignKey(Person, related_name='teacher_subjects')
    lesson_count = models.SmallIntegerField('Количество часов')


class TeacherGroup(models.Model):
    subject = models.ForeignKey(TeacherSubject, related_name='groups')
    group = models.ForeignKey(NGroup, related_name='teachers')


class Magistrate(models.Model):
    _from = models.CharField('Предыдущее место обучения', max_length=60, )
    student = models.OneToOneField(Student, related_name='magistr_student')

    def __str__(self):
        return self._from


class AdditionalSession(models.Model):
    student = models.ForeignKey(Student, related_name='dopkas')
    subject = models.ForeignKey(SemesterSubject, related_name='dopkas')
    datetime = models.DateTimeField('Дата пересдачи')


class Commission(models.Model):
    student = models.ForeignKey(Student, related_name='commissions')
    subject = models.ForeignKey(SemesterSubject, related_name='commissions')
    datetime = models.DateTimeField('Дата пересдачи')


class AcademicVacation(models.Model):
    student = models.ForeignKey(Student, related_name='vacations')
    prev_group = models.ForeignKey(NGroup, related_name='students_vacated')
    year = models.PositiveSmallIntegerField('Год')


class Lesson(models.Model):
    num = models.SmallIntegerField('Номер пары')
    begin = models.TimeField('Время начала')
    end = models.TimeField('Время конца')


class TimetableClass(models.Model):
    EACH = 0
    ODD = 1
    EVEN = 2

    PERIOD_TYPES = (
        (EACH, 'Каждую неделю'),
        (EVEN, 'По четным неделям'),
        (ODD, 'По нечетным неделям')
    )

    classroom = models.CharField('Номер аудитории', max_length=10)
    day_of_week = models.SmallIntegerField('День недели')
    teacher_group = models.ForeignKey(TeacherGroup, related_name='classes')
    period = models.SmallIntegerField(choices=PERIOD_TYPES, default=EACH)
    lesson = models.ForeignKey(Lesson, related_name='+')


class AbsenceEntry(models.Model):
    _class = models.ForeignKey(TimetableClass, related_name='attendance')
    student = models.ForeignKey(Student, related_name='attendance')
    date = models.DateField('Дата занятия')


class Dormitory(models.Model):
    name = models.CharField('Название', max_length=50)
    address = models.CharField('Адрес', max_length=200)


class StudentDormitory(models.Model):
    student = models.ForeignKey(Student, related_name='dorms')
    dormitory = models.ForeignKey(Dormitory, related_name='all_students')
    year = models.PositiveSmallIntegerField('Год')