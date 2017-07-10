from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=30)


class Person(models.Model):
    email = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=40)
    third_name = models.CharField(max_length=40)
    birth_date = models.CharField(max_length=40, null=True, blank=True)
    status = models.ManyToManyField(Status)


class Subject(models.Model):
    name = models.CharField(max_length=30)


class Course(models.Model):
    subject = models.OneToOneField(Subject)


class Semester(models.Model):
    semester = models.IntegerField(max_length=2)


class Laboratory(models.Model):
    name = models.CharField(max_length=40)
    person = models.ForeignKey(Person, related_name='person_laboratories')


class LaboratoryRequests(models.Model):
    student = models.ForeignKey(Student, related_name='student_requests_for_labs')
    laboratory = models.ForeignKey(Laboratory, related_name='laboratory_requests')
    is_active = models.BooleanField(null=True)


class Group(models.Model):
    name = models.CharField(max_length=10)


class Student(models.Model):
    status = models.CharField(max_length=1)
    group = models.ForeignKey(Group, related_name='group_students')
    person = models.OneToOneField(Person, related_name='person_student')
    form_of_education = models.CharField(max_length=1)


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
        unique_together=(('semester', 'subject'),)


class Progress(models.Model):
    subject = models.ForeignKey(Subject)
    student = models.ForeignKey(Student)
    semester = models.IntegerField(max_length=2)
    practice = models.IntegerField(max_length=3)
    exam = models.IntegerField(max_length=3)


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
    group = models.ManyToManyField(Group)
