from django.conf.urls import include, url
from itis_data_niffler.ajax import *
from itis_manage import views as manage_views
from itis_data_niffler import views

urlpatterns = [
    # Auth
    url(r'^auth/login$', manage_views.auth_login, name='login'),

    # Persons
    url(r'^person/(?P<person_id>(\d+))$', views.view_person, name='view-person'),
    url(r'^persons$', views.view_persons, name='view-persons'),

    # Rating
    url(r'^common-rating/$', views.common_rating, name='common-rating'),
    url(r'^subject-rating/$', views.subject_rating, name='subject-rating'),
    url(r'^students/stats/score/$', views.students_stats_score, name='student-rating'),
    url(r'^students/stats/criteria$', views.StudentStatsCriteriaView.as_view(), name='student-criteria'),
    url(r'^group/stats/score/$', views.group_rating, name='group-rating'),

    # Lab
    url(r'^lab/(?P<lab_id>(\d+))$', views.lab_view, name='add-edit-delete-lab'),

    # Requests
    url(r'^request/lab/(?P<lab_id>(\d+))$', views.lab_request_view, name='lab-request-add-edit-delete'),
    url(r'^request/labs$', views.lab_requests, name='lab-requests'),

    # Ajax
    url(r'^ajax/students/stats/score$', get_filtered_students, name='get-filtered-students'),

    # Index
    #url(r'', views.index, name='index'),
]
