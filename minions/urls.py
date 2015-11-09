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
    url(r'^minions_status', views.minions_status,name='minions_status'),
    url(r'^minions_keys', views.minions_keys,name='minions_keys'),
    url(r'^minions_hardware_info', views.minions_hardware_info,name='minions_hardware_info'),
    url(r'^minions_servers_status', views.minions_servers_status,name='minions_servers_status'),
]
