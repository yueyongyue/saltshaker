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
    url(r'login', views.login_view, name='login_view'),
    url(r'logout', views.logout_view, name='logout_view'),
    url(r'add_user', views.add_user, name='add_user'),
    url(r'del_user', views.del_user, name='del_user'),
    url(r'set_password', views.set_password, name='set_password'),
    url(r'setup_user', views.setup_user, name='setup_user'),
    url(r'manage_user', views.add_user, name='manage_user'),

    url(r'^manage_business', views.manage_business,name='manage_business'),
    url(r'^modify_business', views.modify_business,name='modify_business'),
    url(r'^add_business', views.add_business,name='add_business'),
    url(r'^del_business', views.del_business,name='del_business'),

    url(r'^manage_privilege', views.manage_privilege,name='manage_privilege'),
    url(r'^modify_privilege', views.modify_privilege,name='modify_privilege'),
    url(r'^add_privilege', views.add_privilege,name='add_privilege'),
    url(r'^del_privilege', views.del_privilege,name='del_privilege'),

]
