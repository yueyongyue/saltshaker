import os
import time

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from account.models import Businesses,Privileges,UserProfiles
from groups.models import Groups,Hosts
from states_config.models import Highstate
from shaker.shaker_core import *
from shaker.highstate import HighState

@login_required(login_url="/account/login/")
def highstate(request,*args,**kw):
    _error = kw.get("error")
    _success = kw.get("success")

    _u = request.user
    _user = User.objects.get(username=_u)
    _all_businesses = Businesses.objects.all()
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

        _groups = Groups.objects.filter(business__in=_businesses)
        for _group in _groups:
            _h = []
            _hosts = _group.groups_hosts_related.all()
            for _host in _hosts:
                _h.append(_host.minion.minion_id)
                all[_group.name] = _h
    except Exception as e:
        pass

    all_host = all
    _slses = Highstate.objects.all()
    context = {
        "businesses": _all_businesses,
        'list_groups': all_host,
        "slses": _slses,
        "error": _error,
        "success": _success,
        }

    return render(request, 'states_config/highstate.html', context)

@login_required(login_url="/account/login/")
def add_sls(request):
    _error = ""
    _success = ""
    if request.POST:
        _name = request.POST.get("name","")
        _content = request.POST.get("content","")
        _businesses = request.POST.getlist("business",[])
        _informations = request.POST.get("informations","")
        _enabled = request.POST.get("enabled","")
        if _enabled == 'true':
            _enabled = True
        else:
            _enabled = False
        if 1:
           _h = Highstate(name=_name,content=_content,informations=_informations,enabled=_enabled)
           _h.save()
           for _b in _businesses:
               _b_object = Businesses.objects.get(name=_b.strip())
               _h.business.add(_b_object)
           _success = "add sls "+ _name + " 0k!"

        else:
           _error = "name already exists or too long!"

        high = HighState()
        high.add_sls(_name, _content)
    return highstate(request,success=_success,error=_error)

@login_required(login_url="/account/login/")
def modify_sls(request):
    return highstate(request)

@login_required(login_url="/account/login/")
def del_sls(request):
    return highstate(request)

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

#@login_required(login_url="/account/login/")
#def add_sls(request):
#    high = HighState()
#    if request.POST:
#        sls_name = request.POST.get("filename")
#        sls_content = request.POST.get("content")
#        high.add_sls(sls_name, sls_content)
#        return HttpResponse(sls_content)
#
#@login_required(login_url="/account/login/")
#def del_sls(request):
#    high = HighState()
#    if request.POST:
#        sls_name = request.POST.get("filename")
#        high.del_sls(sls_name)
#        return HttpResponse(sls_name)
