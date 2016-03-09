from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.models import *
from returner.models import *
from shaker.shaker_core import *
import json
import os




@login_required(login_url="/account/login/")
def index(request):
    #dashboard = open('/var/cache/salt/master/salt_dashboard.tmp')
    #data = dashboard.readlines()
    #status_list = data[0].split('\n')[0]
    #os_release = data[1].split('\n')[0]
    #os_all = data[2].split('\n')[0]
    try:
        dashboard_status = Dashboard_status.objects.get(id=1)
    except:
        status_list = [0, 0, 0, 0, 0]
    else:
        status_list = [int(dashboard_status.up),
                   int(dashboard_status.down),
                   int(dashboard_status.accepted),
                   int(dashboard_status.unaccepted),
                   int(dashboard_status.rejected),
                   ]

    salt_grains = Salt_grains.objects.all()
    release_list = []
    os_all = []
    os_release = []
    for release in salt_grains:
        release_dic = eval(release.grains)
        release_info = release_dic.get('osfullname').decode('string-escape') + release_dic.get('osrelease').decode('string-escape')
        release_list.append(release_info)
        os_release = list(set(release_list))

    for release_name in os_release:
        os_dic = {'name': release_name, 'value': release_list.count(release_name)}
        os_all.append(os_dic)

    return render(request, 'dashboard/index.html', {'status': status_list,
                                                    'os_release': os_release,
                                                    'os_all': os_all,
                                                    })
