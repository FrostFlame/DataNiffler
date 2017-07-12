from django.conf.urls import include, url
from itis_manage import views
from itis_manage.views import add_group, edit_group

urlpatterns = [
    url(r'auth/login$', views.auth_login, name='login'),
    # Add = person/ , edit-view-delete = person/pk
    url(r'person/(?P<person_id>(\d+)|add)$', views.view_person, name='view-edit-add-student'),
    url(r'group/add$', add_group, name='create-group'),
    url(r'group(?P<group_id>(\d+))$', edit_group, name='edit-group'),
    url(r'', views.index, name='index'),
]
