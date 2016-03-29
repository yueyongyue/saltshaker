"""saltshaker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^manage_group', views.manage_group,name='manage_group'),
    url(r'^del_group', views.del_group,name='del_group'),
    url(r'^add_group', views.add_group,name='add_group'),
    url(r'^modify_group', views.modify_group,name='modify_group'),

    url(r'^manage_host', views.manage_host,name='manage_host'),
    url(r'^modify_host', views.modify_host,name='modify_host'),
    url(r'^add_host', views.add_host,name='add_host'),
    url(r'^del_host', views.del_host,name='del_host'),

    url(r'^manage_business', views.manage_business,name='manage_business'),
    url(r'^modify_business', views.modify_business,name='modify_business'),
    url(r'^add_business', views.add_business,name='add_business'),
    url(r'^del_business', views.del_business,name='del_business'),

    url(r'^manage_privilege', views.manage_privilege,name='manage_privilege'),
    url(r'^modify_privilege', views.modify_privilege,name='modify_privilege'),
    url(r'^add_privilege', views.add_privilege,name='add_privilege'),
    url(r'^del_privilege', views.del_privilege,name='del_privilege'),
]
