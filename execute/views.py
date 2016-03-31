from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from shaker.shaker_core import *
from shaker.nodegroups import *
from groups.models import Groups,Hosts,Privileges

@login_required(login_url="/account/login/")
def shell_runcmd(request):
    _u = request.user
    _user = User.objects.get(username=_u)
    _groups = []
    all = {}
    if _user.is_superuser:
        _groups = Groups.objects.all()
    else:
        _groups = Groups.objects.filter(owner=_user)
    for _group in _groups:
        _h=[]
        _hosts=Hosts.objects.filter(group=_group)
        for _host in _hosts:
            _h.append(_host.name)
            all[_group.name]=_h
    return render(request, 'execute/minions_shell_runcmd.html', {'list_groups': all})

@login_required(login_url="/account/login/")
def shell_result(request):
    sapi = SaltAPI()
    if request.POST:
        cmd = request.POST.get("cmd").strip()
        
        line = "################################################################"
        host_list = request.POST.getlist("hosts_name")
        result = []
        _user=request.user
        _u = User.objects.get(username=_user)
        if not _u.is_superuser:
            for _h in host_list:
                _host = Hosts.objects.get(name=_h)
                _deny=_h.privilege.deny
                _allow=_h.privilege.allow
                if cmd in _deny:
                    error = "error occoureda:host"+ _host+"have no permition run " + cmd
                    result.append(error)
            if len(result) > 0:
                return render(request, 'execute/minions_shell_result.html', {'result': result, 'cmd': cmd, 'line': line})
        else:
            host_str = ",".join(host_list)
            result = sapi.shell_remote_execution(host_str, cmd)
            return render(request, 'execute/minions_shell_result.html', {'result': result, 'cmd': cmd, 'line': line})
    return render(request, 'execute/minions_shell_result.html')

@login_required(login_url="/account/login/")
def salt_runcmd(request):
    return render(request, 'execute/minions_salt_runcmd.html')
