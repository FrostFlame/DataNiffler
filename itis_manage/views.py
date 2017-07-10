from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect as Redirect
from django.shortcuts import render, render_to_response as render_resp
from django.views.generic import View

from itis_manage.forms import UserForm


def auth_login(request):
    form = UserForm()
    if request.method == 'GET':
        return render(request, 'login.html', context={'form': form})
    else:
        form = UserForm(data=request.POST)
        if form.authorize(request):
            return Redirect(reverse('manage:index'))
        else:
            return render(request, 'login.html', {'form': form})


def add_student(request):
    return None


@login_required(login_url=reverse_lazy('manage:login'))
def index(request):
    return HttpResponse("index")
