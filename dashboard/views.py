from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shaker.shaker_core import *
import json
import os




@login_required(login_url="/account/login/")
def index(request):
    dashboard = open('/tmp/salt_dashboard.tmp')
    data = dashboard.readlines()
    status_list = data[0].split('\n')[0]
    os_release = data[1].split('\n')[0]
    os_all = data[2].split('\n')[0]

    return render(request, 'dashboard/index.html', {
            'status': status_list,
            'os_release': os_release,
            'os_all': os_all,
            })

