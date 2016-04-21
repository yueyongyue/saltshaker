from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from shaker.shaker_core import *
from shaker.nodegroups import *
from groups.models import Groups,Hosts
from account.models import Businesses,Privileges,UserProfiles

@login_required(login_url="/account/login/")
def shell_runcmd(request):
    _u = request.user
    _user = User.objects.get(username=_u)
    _userprofile = UserProfiles.objects.get(user=_user)

    _businesses = []
    all = {}

    _b = _userprofile.business.all()
    for _tmp in _b:
        _businesses.append(_tmp.name)

    _groups=Groups.objects.filter(business__in = _businesses)

    for _group in _groups:
        _h=[]
        _hosts=_group.groups_hosts_related.all()
        for _host in _hosts:
            _h.append(_host.minion.minion_id)
            all[_group.name]=_h
    return render(request, 'execute/minions_shell_runcmd.html', {'list_groups': all})

@login_required(login_url="/account/login/")
def shell_result(request):
    _u = request.user
    _user = User.objects.get(username=_u)
    _userprofile = UserProfiles.objects.get(user=_user)
    _privileges = _userprofile.privilege.all()
    host_list = request.POST.getlist("hosts_name")

    line = "################################################################"
    result = {}
    minion_id_list = []

    _deny = []
    _allow = []
    for _p in _privileges:
        _deny.append(_p.deny)  
        _allow.append(_p.allow)

    sapi = SaltAPI()
    if request.POST:
        cmd = request.POST.get("cmd").strip()
        if len(_deny) > 0 or len(_allow) > 0:
            if cmd in _deny or cmd not in _allow:
                error = "error occurred : You have no permition run [ " + cmd +" ]"
                result["result"]=error
                return render(request, 'execute/minions_shell_result.html', {'result': result, 'cmd': cmd, 'line': line})

        for _h in host_list:
            _host = Hosts.objects.get(name=_h)
            minion_id_list.append(_host.minion.minion_id)
                        
        if len(result) > 0:
            return render(request, 'execute/minions_shell_result.html', {'result': result, 'cmd': cmd, 'line': line})
        #run cmd now
        host_str = ",".join(minion_id_list)
        # the type of result is dictionary
        result = sapi.shell_remote_execution(host_str, cmd)
        return render(request, 'execute/minions_shell_result.html', {'result': result, 'cmd': cmd, 'line': line})
    return render(request, 'execute/minions_shell_result.html')

@login_required(login_url="/account/login/")
def salt_runcmd(request):
    return render(request, 'execute/minions_salt_runcmd.html')
