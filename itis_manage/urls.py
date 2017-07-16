from django.conf.urls import url
from itis_manage import views
from itis_manage.models import Student
from itis_manage.views import add_subject, AddGroupView, EditGroupView
from itis_manage.ajax import *
from itis_manage.views import add_subject

urlpatterns = [
    url(r'^index/$', views.index, name='index'),

    # Add = person/ , edit-delete = person/pk
    url(r'^person/(?P<person_id>(\d+)|add)$', views.view_person, name='edit-add-delete-person'),
    url(r'^persons$', views.view_persons, name='view-persons'),
    url(r'^crispy/$', views.try_crispy_form, name='try_crispy'),

    # Group
    url(r'^group/add$', AddGroupView.as_view(), name='create-group'),
    url(r'^group/(?P<pk>(\d+))$', EditGroupView.as_view(), name='edit-group'),
    url(r'^subject/add$', add_subject, name='create-subject'),

    # Lab
    url(r'^lab/(?P<lab_id>(\d+)|add)$', views.lab_view, name='add-edit-delete-lab'),

    # Requests
    url(r'^request/lab/(?P<lab_id>(\d+)|add)$', views.lab_request, name='lab-request-add-edit-delete'),
    url(r'^request/labs$', views.lab_requests, name='lab-requests'),

    # Ajax requests
    url(r'^ajax/cities$', GetObjects.as_view(**{'model': City}), name='ajax-cities'),
    url(r'^ajax/curators$', CuratorAutocompleteView.as_view(), name='ajax-curators'),
    url(r'^ajax/statuses$', GetObjects.as_view(**{'model': Status}), name='ajax-statuses'),
    url(r'^ajax/students$', GetObjects.as_view(**{'model': Student}), name='ajax-students'),
    url(r'^get_teachers/$', views.teachers_ajax, name='teacher-ajax'),
    url(r'^ajax/get_subjects/$', get_subjects, name='ajax-get-subjects'),
]
