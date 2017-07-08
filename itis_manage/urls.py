from django.conf.urls import include, url

from itis_manage.views import index

urlpatterns = [
    url(r'index/$', index, name='index'),
]