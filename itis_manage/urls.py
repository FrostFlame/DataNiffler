from django.conf.urls import include, url
from itis_manage import views

urlpatterns = [
    # Add = person/ , edit-delete = person/pk
    url(r'person/(?P<person_id>(\d+)|add)$', views.view_person, name='edit-add-delete-person'),
    url(r'crispy/$', views.try_crispy_form, name='try_crispy'),
]
