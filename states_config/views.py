from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from account.models import Businesses,Privileges,UserProfiles
from groups.models import Groups,Hosts
from shaker.shaker_core import *
from shaker.nodegroups import *
from shaker.highstate import *
import os
import time

@login_required(login_url="/account/login/")
def highstate(request):
    high = HighState()
    #group = NodeGroups()
    #all_host = group.list_groups_hosts()
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
    all_host = all
    all_sls = high.list_sls('/srv/salt/')
    return render(request, 'states_config/highstate.html', {'list_groups': all_host, 'all_sls': all_sls})

@login_required(login_url="/account/login/")
def highstate_result(request):
    sapi = SaltAPI()
    if request.POST:
        sls_name = request.POST.get("sls_name")
        host_list = request.POST.getlist("hosts_name")
        host_str = ",".join(host_list)
        jid = sapi.target_deploy(host_str, sls_name)
        jids = "salt-run jobs.lookup_jid " + jid
        time.sleep(60)
        result = os.popen(jids).read()
        if result == "":
            result = "Execute time too long, Please see jid:" + jid + " history."
            return render(request, 'states_config/highstate_result.html', {'result': result})
        else:
            return render(request, 'states_config/highstate_result.html', {'result': result})
    return render(request, 'states_config/highstate_result.html')

@login_required(login_url="/account/login/")
def add_sls(request):
    high = HighState()
    if request.POST:
        sls_name = request.POST.get("filename")
        sls_content = request.POST.get("content")
        high.add_sls(sls_name, sls_content)
        return HttpResponse(sls_content)

@login_required(login_url="/account/login/")
def del_sls(request):
    high = HighState()
    if request.POST:
        sls_name = request.POST.get("filename")
        high.del_sls(sls_name)
        return HttpResponse(sls_name)
