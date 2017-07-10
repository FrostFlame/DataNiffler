from django.conf.urls import include, url
from itis_manage import views

urlpatterns = [
    url(r'auth/login$', views.auth_login, name='login'),
    url(r'person/add$', views.add_person, name='add-student'),
    url(r'person/(?P<person_id>(\d+))', views.view_person, name='view-student'),
    url(r'$', views.index, name='index'),
]


