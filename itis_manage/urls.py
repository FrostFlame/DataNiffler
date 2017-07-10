from django.conf.urls import include, url
from itis_manage import views

urlpatterns = [
    url(r'auth/login$', views.auth_login, name='login'),
    url(r'students/add$', views.add_student, name='add-student'),
    url(r'', views.index, name='index'),
]


