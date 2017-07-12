from django.conf.urls import include, url
from itis_manage import views
from itis_manage.views import add_group, edit_group, add_subject

urlpatterns = [
    # Add = person/ , edit-delete = person/pk
    url(r'person/(?P<person_id>(\d+)|add)$', views.view_person, name='edit-add-delete-person'),
    url(r'crispy/$', views.try_crispy_form, name='try_crispy'),

    # Group
    url(r'group/add$', add_group, name='create-group'),
    url(r'group(?P<group_id>(\d+))$', edit_group, name='edit-group'),
    url(r'subject/add$', add_subject, name='create-subject'),
    url(r'', views.index, name='index'),
]
