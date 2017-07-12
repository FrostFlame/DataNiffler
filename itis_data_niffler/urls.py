from django.conf.urls import include, url

from itis_manage import views as manage_views
from itis_data_niffler import views

urlpatterns = [
    url(r'auth/login$', manage_views.auth_login, name='login'),
    url(r'person/(?P<person_id>(\d+))$', views.view_person, name='view-edit-add-student'),
    url(r'person/(?P<person_id>(\d+)|add)$', views.view_person, name='view-edit-add-student'),
    url(r'persons$', views.view_persons, name='view-persons'),
    url(r'common-rating/$',views.common_rating,name='common-rating'),
    url(r'subject-rating/$',views.subject_rating,name='subject-rating')
]
