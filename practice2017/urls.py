from django.conf.urls import include, url
from django.contrib import admin
from itis_manage import urls as manage_urls
from itis_data_niffler import urls as data_niffler_urls
from practice2017 import set_lib, parsers_view

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^manage/', include(manage_urls, namespace='manage')),
    url(r'^update/(?P<table_id>(\d+|info))$', set_lib.update, name='update_tables'),
    url(r'^parser/$', parsers_view.first, name='parser'),
    url(r'^tellme/', include("tellme.urls")),
    url(r'^', include(data_niffler_urls, namespace='data')),
]
