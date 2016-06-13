# -*- coding:utf-8 -*-
#!/bin/env python

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^manage_file', views.manage_file,name='manage_file'),
    url(r'^del_file', views.del_file,name='del_file'),
    url(r'^upload_file', views.upload_file,name='upload_file'),
]
