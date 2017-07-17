from django.conf.urls import url
from itis_manage import views
from itis_manage.models import Student, NGroup
from itis_manage.views import add_subject, AddGroupView, EditGroupView, add_theme_subject
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

    # Subject
    url(r'^subject/add$', views.add_subject, name='create-subject'),
    url(r'^subject/semesters/add$', views.add_subject_semesters, name='create-subject-semesters'),
    url(r'^subject_theme/add$', add_theme_subject, name='add-theme-subjecy'),

    # Lab
    url(r'^lab/(?P<lab_id>(\d+)|add)$', views.lab_view, name='add-edit-delete-lab'),

    # Requests
    url(r'^request/lab/(?P<lab_id>(\d+)|add)$', views.lab_request, name='lab-request-add-edit-delete'),
    url(r'^request/labs$', views.lab_requests, name='lab-requests'),

    # Progress(student balls :D)
    url(r'^scores/add/$', views.add_scores, name='add-scores'),

    # Ajax requests
    url(r'^ajax/cities$', GetObjects.as_view(**{'model': City}), name='ajax-cities'),
    url(r'^ajax/curators$', CuratorAutocompleteView.as_view(), name='ajax-curators'),
    url(r'^ajax/statuses$', GetObjects.as_view(**{'model': Status}), name='ajax-statuses'),
    url(r'^ajax/students$', GetObjects.as_view(**{'model': Student}), name='ajax-students'),
    url(r'^ajax/get_teachers/$', views.teachers_ajax, name='ajax-teachers'),
    url(r'^ajax/get_subjects/$', get_subjects, name='ajax-get-subjects'),
    url(r'^ajax/groups$', GetObjects.as_view(**{'model': NGroup}), name='ajax-groups'),

]
