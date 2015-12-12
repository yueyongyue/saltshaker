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
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import dashboard,minions,execute,jobs,states_config,code_update,groups,system_setup,account

urlpatterns = [
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.STATIC_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index.html', include('dashboard.urls')),
    url(r'^$', include('dashboard.urls')),
    url(r'minions/', include('minions.urls')),
    url(r'execute/', include('execute.urls')),
    url(r'jobs/', include('jobs.urls')),
    url(r'states_config/', include('states_config.urls')),
    #url(r'code_update/', include('code_update.urls')),
    url(r'groups/', include('groups.urls')),
    #url(r'system_setup/', include('system_setup.urls')),
    #url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'account/login.html'}),
    url(r'account/', include('account.urls')),

]
