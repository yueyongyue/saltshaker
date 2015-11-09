from django.shortcuts import render
from shaker.shaker_core import *

def minions_status(request):
    sapi = SaltAPI()
    status_all = sapi.runner_status('status')
    return render(request,'minions/minions_status.html', {'status': status_all})

def minions_keys(request):
    sapi = SaltAPI()
    if request.POST:
        hostname = request.POST.get("delete")
        sapi.delete_key(hostname)
        hostname = request.POST.get("accept")
        sapi.accept_key(hostname)
        hostname = request.POST.get("reject")
        sapi.reject_key(hostname)
    keys_all = sapi.list_all_key()
    return render(request,'minions/minions_keys.html',{'key': keys_all})

def minions_hardware_info(request):
    sapi = SaltAPI()
    up_host = sapi.runner_status('status')['up']
    jid = []
    disk_dic = {}
    disk_all = {}
    for hostname in up_host:
        info_all = sapi.remote_noarg_execution(hostname,'grains.items')
        disk_use = sapi.remote_noarg_execution(hostname,'disk.usage')
        for key in disk_use:
            disk_info = {key : disk_use[key]['capacity']}
            disk_all.update(disk_info)
            disk_dic = {'disk' : disk_all}
            info_all.update(disk_dic)
        disk_all = {}
        jid += [info_all]
    return render(request,'minions/minions_hardware_info.html', {'jyp' : jid})

def minions_servers_status(request):
    return render(request,'minions/minions_servers_status.html',)
