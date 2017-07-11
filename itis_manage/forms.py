from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Model
from django.forms import widgets, inlineformset_factory
from django.shortcuts import get_object_or_404

from itis_manage.models import Student, NGroup, Person, Status

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

    status = forms.ModelMultipleChoiceField(queryset=Status.objects.all())

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            statuses = kwargs['instance'].status.all()
            super(PersonForm, self).__init__(*args, **kwargs)
            self.fields['status'].initial = statuses
        else:
            super(PersonForm, self).__init__(*args, **kwargs)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ('person',)

    group = forms.ModelChoiceField(queryset=NGroup.objects.all())

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            group = kwargs['instance'].group
            super(StudentForm, self).__init__(*args, **kwargs)
            self.fields['group'].initial = group
        else:
            super(StudentForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.is_valid():
            student = super(StudentForm, self).save(commit=False)
            student.person = kwargs.pop('person', None)
            student.save()
            return student
        raise ValidationError('Save student is incorrect')
