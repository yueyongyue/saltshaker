from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shaker.shaker_core import *
import json



@login_required(login_url="/account/login/")
def index(request):
    # minion status
    status_list = []
    sapi = SaltAPI()
    status = sapi.runner_status('status')
    key_status = sapi.list_all_key()
    up = len(status['up'])
    status_list.append(up)
    down = len(status['down'])
    status_list.append(down)
    accepted = len(key_status['minions'])
    status_list.append(accepted)
    unaccepted = len(key_status['minions_pre'])
    status_list.append(unaccepted)
    rejected = len(key_status['minions_rejected'])
    status_list.append(rejected)
    # os release
    up_host = sapi.runner_status('status')['up']
    os_list = []
    os_all = []
    for hostname in up_host:
        osfullname = sapi.grains(hostname,'osfullname')[hostname]['osfullname']
        osrelease = sapi.grains(hostname,'osrelease')[hostname]['osrelease']
        os = osfullname + osrelease
        os_list.append(os)
    os_uniq = set(os_list)
    for release in os_uniq:
        num = os_list.count(release)
        os_dic = {'value': num, 'name': release}
        os_all.append(os_dic)
    os_release = list(set(os_list))

    return render(request, 'dashboard/index.html', {
            'status': json.dumps(status_list),
            'os_release': json.dumps(os_release),
            'os_all': json.dumps(os_all),
            })

