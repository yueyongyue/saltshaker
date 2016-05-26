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
import logging

logger = logging.getLogger('django')

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
            _slses = Highstate.objects.all()
        else:
            _userprofile = UserProfiles.objects.get(user=_user)
            _b = _userprofile.business.all()

            _slses = Highstate.objects.filter(business__in = _b)
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
           _success = "add sls "+ _name + " ok!"

        else:
           _error = "name already exists or too long!"

        high = HighState()
        high.add_sls(_name, _content)
    return highstate(request,success=_success,error=_error)

@login_required(login_url="/account/login/")
def modify_sls(request):
    _success = False
    _error = False
    if request.method == "POST":
        _id = request.POST.get("id")
        _name = request.POST.get("name")
        _businesses = request.POST.getlist("business")
        _content = request.POST.get("content")
        _informations = request.POST.get("informations")
        _enabled=request.POST.get("enabled")
        if _enabled is not None:
            _enabled = True
        else:
            _enabled = False
        #try:
        if 1:
            _highstate = Highstate.objects.get(id=_id)
            _name_before =_highstate.name
            _highstate.name = _name
            _highstate.content = _content
            _highstate.enabled = _enabled
            _highstate.informations = _informations
            _highstate.save()
            for _b in _businesses:
                _b_object = Businesses.objects.get(name=_b.strip())
                _highstate.business.add(_b_object)
            _success = "Modify SLS " + _name + " OK"
        #except Exception as e:
        else:
            _error = "Modify SLS " + _name + " failed"

        high = HighState()
        high.add_sls(_name, _content)
            
    return highstate(request,success=_success,error=_error)

@login_required(login_url="/account/login/")
def del_sls(request):
    _success = False
    _error = False
    _ids = request.POST.getlist("id")
    try:
        _filter = Highstate.objects.filter(id__in=_ids)

        high = HighState()
        for sls_name in _filter:
            high.del_sls(sls_name.name)

        _filter.delete()
        _success = "Delete opearation success!"
    except Exception as e:
        _error = "Delete error!"

    return highstate(request,success=_success,error=_error)

@login_required(login_url="/account/login/")
def highstate_result(request):
    sapi = SaltAPI()
    if request.POST:
        host_list = request.POST.getlist("hosts_name")
        execute = request.POST.get("execute")
        if execute:
            host_str = ",".join(host_list)
            jid = sapi.target_deploy(host_str, execute)
            while 1:
                jids = "salt-run jobs.lookup_jid " + jid
                result = os.popen(jids).read()
                if len(result) > 0:
                    break
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
