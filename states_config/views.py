from django.shortcuts import render
from django.http import HttpResponse
from shaker.shaker_core import *
from shaker.nodegroups import *
from shaker.highstate import *
import os
import time

def highstate(request):
    group = NodeGroups()
    high = HighState()
    all_host = group.list_groups_hosts()
    all_sls = high.list_sls('/srv/salt/')
    return render(request, 'states_config/highstate.html', {'list_groups': all_host, 'all_sls': all_sls})

def highstate_result(request):
    sapi = SaltAPI()
    if request.POST:
        sls_name = request.POST.get("sls_name")
        host_list = request.POST.getlist("hosts_name")
        host_str = ",".join(host_list)
        jid = sapi.target_deploy(host_str, sls_name)
        jids = "salt-run jobs.lookup_jid" + " " + jid
        time.sleep(10)
        detail = os.popen(jids).read()
        test = "testestestet "
        return render(request, 'states_config/highstate_result.html', {'result': detail, "jids": jid, "cmd": jids, "test": test})
    return render(request, 'states_config/highstate_result.html')

def add_sls(request):
    high = HighState()
    if request.POST:
        sls_name = request.POST.get("filename")
        sls_content = request.POST.get("content")
        high.add_sls(sls_name, sls_content)
        return HttpResponse(sls_content)

def del_sls(request):
    high = HighState()
    if request.POST:
        sls_name = request.POST.get("filename")
        high.del_sls(sls_name)
        return HttpResponse(sls_name)
'''
jid = "20151129093930970477"
jids = "salt-run jobs.lookup_jid" + " " + jid
detail = os.popen(jids).read()
print detail
'''