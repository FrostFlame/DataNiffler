from collections import OrderedDict

from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Model
from django.forms import widgets, inlineformset_factory, ModelChoiceField, ModelMultipleChoiceField
from django.shortcuts import get_object_or_404
import datetime

from itis_data_niffler.lib import set_readable_related_fields
from itis_manage.models import Student, NGroup, Person, Status, Magistrate, Laboratory, LaboratoryRequests

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field


class SimpleForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(
        label="Password", required=True, widget=forms.PasswordInput)
    remember = forms.BooleanField(label="Remember Me?")

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'login', css_class='btn-primary'))


class UserForm(forms.Form):
    username = forms.CharField(required=True, error_messages={"unf": 'User not found'})
    password = forms.CharField(required=True, widget=widgets.PasswordInput, min_length=6, max_length=100,
                               error_messages={"pass_err": "Incorrect password"})

    def authorize(self, request):
        if self.is_valid():
            user = authenticate(request=request, username=self.cleaned_data['username'],
                                password=self.cleaned_data['password'], )
            if user is not None:
                login(request, user)
                return True
        self.add_error('password', self.fields['password'].error_messages['pass_err'])
        return False

    def is_valid(self):
        valid = super(UserForm, self).is_valid()
        if valid:
            try:
                user = User.objects.get(username=self.data['username'])
            except:
                self.add_error('username', self.fields['username'].error_messages['unf'])
                return False
        else:
            return False
        return valid


class GroupForm(forms.ModelForm):
    class Meta:
        model = NGroup
        fields = '__all__'


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        exclude = ('created_at',)

    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=Person.BIRTH_YEAR_CHOICES),
                                 initial=datetime.date.today, label_suffix='(не обязательно)')

    def __init__(self, readonly=False, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        if readonly:
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                set_readable_related_fields(instance, self)
                for field in self.fields:
                    self.fields[field].widget.attrs['readonly'] = True


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ('person',)

    def __init__(self, readonly=False, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        if readonly:
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                set_readable_related_fields(instance, self)
                for field in self.fields:
                    self.fields[field].widget.attrs['readonly'] = True

    def save(self, *args, **kwargs):
        if self.is_valid():
            student = super(StudentForm, self).save(commit=False)
            student.person = kwargs.pop('person', None)
            student.save()
            return student
        raise ValidationError('Save student is incorrect')


class MagistrForm(forms.ModelForm):
    class Meta:
        model = Magistrate
        fields = ('_from',)

    def __init__(self, readonly=False, *args, **kwargs):
        super(MagistrForm, self).__init__(*args, **kwargs)
        if readonly:
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                set_readable_related_fields(instance, self)
                for field in self.fields:
                    self.fields[field].widget.attrs['readonly'] = True

    def save(self, *args, **kwargs):
        if self.is_valid():
            magistr = super(MagistrForm, self).save(commit=False)
            magistr.student = kwargs.pop('student', None)
            magistr.save()
            return magistr
        raise ValidationError('Save magistr is incorrect')


class LaboratoryForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        fields = '__all__'

    def __init__(self, readonly=False, *args, **kwargs):
        super(LaboratoryForm, self).__init__(*args, **kwargs)
        if readonly:
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                set_readable_related_fields(instance, self)
                for field in self.fields:
                    self.fields[field].widget.attrs['readonly'] = True


class LabRequestForm(forms.ModelForm):
    class Meta:
        model = LaboratoryRequests
        fields = ('laboratory', 'student', 'is_active',)

    def __init__(self, readonly=False, *args, **kwargs):
        super(LabRequestForm, self).__init__(*args, **kwargs)
        if readonly:
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                set_readable_related_fields(instance, self)
                for field in self.fields:
                    self.fields[field].widget.attrs['readonly'] = True
