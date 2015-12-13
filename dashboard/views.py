from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shaker.shaker_core import *
from django.http import HttpResponse



@login_required(login_url="/account/login/")
def index(request):
    status_list = []
    sapi = SaltAPI()
    status = sapi.runner_status('status')
    up = len(status['up'])
    status_list.append(up)
    down = len(status['down'])
    status_list.append(down)
    key_status = sapi.list_all_key()
    accepted = len(key_status ['minions'])
    status_list.append(accepted)
    unaccepted = len(key_status ['minions_pre'])
    status_list.append(unaccepted)
    rejected = len(key_status ['minions_rejected'])
    status_list.append(rejected)
    return render(request, 'dashboard/index.html', {'status': status_list})

