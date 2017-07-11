from django.conf.urls import include, url
from itis_manage import views

urlpatterns = [
    url(r'auth/login$', views.auth_login, name='login'),
    # Add = person/ , edit-view-delete = person/pk
    url(r'person/(?P<person_id>(\d+)|)$', views.view_person, name='view-edit-add-student'),
    url(r'crispy/$', views.try_crispy_form, name='try_crispy'),
]
