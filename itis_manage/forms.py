from collections import OrderedDict

from dal import autocomplete
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Model
from django.forms import widgets, inlineformset_factory, ModelChoiceField, ModelMultipleChoiceField
from django.shortcuts import get_object_or_404
import datetime

from django.urls import reverse, reverse_lazy

from itis_data_niffler.lib import set_readable_related_fields
from itis_manage.models import Student, NGroup, Person, Status, Magistrate, Laboratory, LaboratoryRequests
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from datetimewidget.widgets import DateTimeInput, DateWidget, DateTimeWidget

# Select2 widget settings
forms.ModelMultipleChoiceField.widget = autocomplete.ModelSelect2Multiple
forms.ModelChoiceField.widget = autocomplete.ModelSelect2


class SimpleForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(
        label="Password", required=True, widget=forms.PasswordInput)
    remember = forms.BooleanField(label="Remember Me?")

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'login', css_class='btn-primary'))


class ReadOnlySupportMixin(object):
    def __init__(self, readonly=False, *args, **kwargs):
        super(ReadOnlySupportMixin, self).__init__(*args, **kwargs)
        if readonly:
            self.readonly = True
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                set_readable_related_fields(instance, self)
                for field in self.fields:
                    self.fields[field].disabled = True


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
        widgets = {
            'curator': autocomplete.ModelSelect2Multiple(url='manage:ajax-curators', )
        }


class PersonForm(ReadOnlySupportMixin, forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        exclude = ('created_at',)
        widgets = {
            'city': autocomplete.ModelSelect2(url='manage:ajax-cities'),
        }

    birth_date = forms.DateField(initial='01.01.2001',
                                 widget=DateWidget(attrs={'id': "id_birth_date", }, usel10n=True, bootstrap_version=3))


class StudentForm(ReadOnlySupportMixin, forms.ModelForm):
    class Meta:
        model = Student
        exclude = ('person',)
        widgets = {'standing': autocomplete.ModelSelect2(),
                   'form_of_education': autocomplete.ListSelect2(), }

    def save(self, *args, **kwargs):
        if self.is_valid():
            student = super(StudentForm, self).save(commit=False)
            student.person = kwargs.pop('person', None)
            student.save()
            return student
        raise ValidationError('Save student is incorrect')


class MagistrForm(ReadOnlySupportMixin, forms.ModelForm):
    class Meta:
        model = Magistrate
        fields = ('_from',)

    def save(self, *args, **kwargs):
        if self.is_valid():
            magistr = super(MagistrForm, self).save(commit=False)
            magistr.student = kwargs.pop('student', None)
            magistr.save()
            return magistr
        raise ValidationError('Save magistr is incorrect')


class LaboratoryForm(ReadOnlySupportMixin, forms.ModelForm):
    class Meta:
        model = Laboratory
        fields = '__all__'


class LabRequestForm(ReadOnlySupportMixin, forms.ModelForm):
    class Meta:
        model = LaboratoryRequests
        fields = ('laboratory', 'student', 'is_active',)
        widgets = {
            'student': autocomplete.ModelSelect2(url='manage:ajax-students')}
