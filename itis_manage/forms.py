from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.shortcuts import get_object_or_404


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
