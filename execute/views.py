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

    _businesses = []
    all = {}
    try:
        if _user.is_superuser:
            _userprofile = UserProfiles.objects.all()
            _b = Businesses.objects.all()
        else:
            _userprofile = UserProfiles.objects.get(user=_user)
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
    except Exception as e:
        pass
    return render(request, 'execute/minions_shell_runcmd.html', {'list_groups': all})

@login_required(login_url="/account/login/")
def shell_result(request):
    sapi = SaltAPI()
    _u = request.user
    _user = User.objects.get(username=_u)
    host_list = request.POST.getlist("hosts_name")
    try:
        _userprofile = UserProfiles.objects.get(user=_user)
    except Exception as e:
        return render(request, 'execute/minions_shell_result.html')

    _privileges = _userprofile.privilege.all()

    _deny = []
    _allow = []

    line = "################################################################"
    result = {}
    minion_id_list = []

    for _p in _privileges:
        _deny.append(_p.deny)  
        _allow.append(_p.allow)

    if request.POST:
        cmd = request.POST.get("cmd").strip()
        if not _user.is_superuser:
            if len(_allow) > 0:
                if cmd not in _allow:
                    error = "error occurred : You have no permition run [ " + cmd +" ]"
                    result["result"]=error
                    return render(request, 'execute/minions_shell_result.html', {'result': result, 'cmd': cmd, 'line': line})

            if len(_deny) > 0: 
                if cmd in _deny:
                    error = "error occurred : You have no permition run [ " + cmd +" ]"
                    result["result"]=error
                    return render(request, 'execute/minions_shell_result.html', {'result': result, 'cmd': cmd, 'line': line})
        else:
            pass

        for _h in host_list:
            try:
                _host = Hosts.objects.get(name=_h)
                minion_id_list.append(_host.minion.minion_id)
            except:
                minion_id_list.append(_h)
                        
        #run cmd now
        host_str = ",".join(minion_id_list)
        # the type of result is dictionary
        result = sapi.shell_remote_execution(host_str, cmd)
        return render(request, 'execute/minions_shell_result.html', {'result': result, 'cmd': cmd, 'line': line})
    return render(request, 'execute/minions_shell_result.html')

@login_required(login_url="/account/login/")
def salt_runcmd(request):
    return render(request, 'execute/minions_salt_runcmd.html')
