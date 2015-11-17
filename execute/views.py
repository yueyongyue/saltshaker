from django.shortcuts import render
from shaker.shaker_core import *
from shaker.nodegroups import *
from django.http import HttpResponseRedirect


def shell_runcmd(request):
    group = NodeGroups()
    all = group.list_groups_hosts()
    return render(request,'execute/minions_shell_runcmd.html',{ 'list_groups': all })

def shell_result(request):
    sapi = SaltAPI()
    if request.POST:
        cmd = request.POST.get("cmd")
        host_list = request.POST.getlist("host")
        host_str = ",".join(host_list)
        result = sapi.shell_remote_execution(host_str,cmd)
        return render(request,'execute/minions_shell_result.html', {'result': result })
    return render(request,'execute/minions_shell_result.html')

def salt_runcmd(request):
    return render(request,'execute/minions_salt_runcmd.html',)
