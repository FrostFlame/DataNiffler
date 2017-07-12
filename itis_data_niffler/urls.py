from django.conf.urls import include, url

from itis_manage import views as manage_views
from itis_data_niffler import views

urlpatterns = [
    # Auth
    url(r'auth/login$', manage_views.auth_login, name='login'),

    # Persons
    url(r'person/(?P<person_id>(\d+))$', views.view_person, name='view-person'),
    url(r'persons$', views.view_persons, name='view-persons'),

    # Rating
    url(r'common-rating/$', views.common_rating, name='common-rating'),
    url(r'subject-rating/$', views.subject_rating, name='subject-rating'),

    # Index
    url(r'', views.index, name='index'),
]
