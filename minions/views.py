from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shaker.shaker_core import *
from shaker.nodegroups import *
from minions.models import Minions_status
from returner.models import Salt_grains


@login_required(login_url="/account/login/")
def minions_status(request):
    status = Minions_status.objects.all()
    return render(request, 'minions/minions_status.html', {'status': status})

@login_required(login_url="/account/login/")
def minions_keys(request):
    sapi = SaltAPI()
    if request.POST:
        hostname = request.POST.get("delete")
        sapi.delete_key(hostname)
        Minions_status.objects.get(minion_id=hostname).delete()
        Salt_grains.objects.get(minion_id=hostname).delete()
        hostname = request.POST.get("accept")
        sapi.accept_key(hostname)
        hostname = request.POST.get("reject")
        sapi.reject_key(hostname)
    keys_all = sapi.list_all_key()
    return render(request, 'minions/minions_keys.html', {'key': keys_all})

@login_required(login_url="/account/login/")
def minions_hardware_info(request):
    sapi = SaltAPI()
    up_host = sapi.runner_status('status')['up']
    jid = []
    disk_all = {}
    for hostname in up_host:
        info_all = sapi.remote_noarg_execution(hostname, 'grains.items')
        disk_use = sapi.remote_noarg_execution(hostname, 'disk.usage')
        for key in disk_use:
            disk_info = {key: int(disk_use[key]['capacity'][:-1])}
            disk_all.update(disk_info)
            disk_dic = {'disk': disk_all}
            info_all.update(disk_dic)
        disk_all = {}
        jid += [info_all]
    return render(request, 'minions/minions_hardware_info.html', {'jyp': jid})

@login_required(login_url="/account/login/")
def minions_servers_status(request):
    return render(request, 'minions/minions_servers_status.html',)
