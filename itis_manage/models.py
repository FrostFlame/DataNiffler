from django.db import models


class Person(models.Model):
    email = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=40)
    third_name = models.CharField(max_length=40)
    birth_date = models.CharField(max_length=40, null=True, blank=True)


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
