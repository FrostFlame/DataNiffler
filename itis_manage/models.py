from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Person(models.Model):
    BIRTH_YEAR_CHOICES = [year for year in range(1960, 2018)]

    email = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=40)
    third_name = models.CharField(max_length=40)
    birth_date = models.CharField(max_length=40, null=True, blank=True)
    status = models.ManyToManyField(Status, related_name='status_persons')
    country = models.ForeignKey('City', related_name='city_persons')

    def __str__(self):
        return '%s %s %s (%s)' % (self.surname, self.name, self.third_name, self.status)


class Semester(models.Model):
    semester = models.CharField(max_length=2)



class NGroup(models.Model):
    name = models.CharField(max_length=10)
    year_of_foundation = models.IntegerField()
    curator = models.ManyToManyField(Person, related_name='curator_group')

    class Meta:
        unique_together = (('name', 'year_of_foundation'),)

    def __str__(self):
        return "#%s (%s)" % (self.name, self.year_of_foundation)


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


class Subject(models.Model):
    name = models.CharField(max_length=30, unique=True)
    semester = models.ManyToManyField(Semester)


class Course(models.Model):
    subject = models.OneToOneField(Subject)


class Laboratory(models.Model):
    name = models.CharField(max_length=40)
    person = models.ForeignKey(Person, related_name='person_laboratories')


class LaboratoryRequests(models.Model):
    student = models.ForeignKey('Student', related_name='student_requests_for_labs')
    laboratory = models.ForeignKey(Laboratory, related_name='laboratory_requests')
    is_active = models.BooleanField(default=False)


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
    semester = models.ForeignKey(Semester, related_name='semester_subjects')
    type_of_exam = models.CharField(
        max_length=2,
        choices=TYPE_OF_EXAM_CHOICES,
        default=EXAM
    )

    class Meta:
        unique_together = (('semester', 'subject'),)


class Progress(models.Model):
    semester_subject = models.ForeignKey(SemesterSubject, related_name='semester_subject_progresses')
    student = models.ForeignKey(Student, related_name='student_progresses')
    practice = models.IntegerField()
    exam = models.IntegerField()

    class Meta:
        unique_together = (('semester_subject', 'student'),)


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

    subject = models.ForeignKey(Subject)
    person = models.ForeignKey(Person)
    group = models.ManyToManyField(NGroup)


class City(models.Model):
    name = models.CharField('Город', max_length=50, unique=True)

    def __str__(self):
        return self.name


class Magistrate(models.Model):
    _from = models.CharField('Предыдущее место обучения', max_length=60, )
    student = models.OneToOneField(Student, related_name='magistr_student')

    def __str__(self):
        return self._from
