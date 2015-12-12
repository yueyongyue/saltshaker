from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shaker.shaker_core import *
from shaker.nodegroups import *

@login_required(login_url="/account/login/")
def shell_runcmd(request):
    group = NodeGroups()
    all = group.list_groups_hosts()
    return render(request, 'execute/minions_shell_runcmd.html', {'list_groups': all})

@login_required(login_url="/account/login/")
def shell_result(request):
    sapi = SaltAPI()
    if request.POST:
        cmd = request.POST.get("cmd").strip()
        line = "################################################################"
        host_list = request.POST.getlist("hosts_name")
        host_str = ",".join(host_list)
        result = sapi.shell_remote_execution(host_str, cmd)
        return render(request, 'execute/minions_shell_result.html', {'result': result, 'cmd': cmd, 'line': line})
    return render(request, 'execute/minions_shell_result.html')

@login_required(login_url="/account/login/")
def salt_runcmd(request):
    return render(request, 'execute/minions_salt_runcmd.html')