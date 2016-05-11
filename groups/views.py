from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from shaker.shaker_core import *
from groups.models import Groups,Hosts
from account.models import UserProfiles,Businesses,Privileges
from minions.models import Minions_status


#######################  manage group ###########################
@login_required(login_url="/account/login/")
def manage_group(request,*args,**kw):
    _current_user = request.user
    _u=User.objects.get(username=_current_user)
    _user_profile = UserProfiles.objects.get(user=_u)
    if _u.is_superuser == True:
        _groups = Groups.objects.all()
    else:
        _bs = []
        _tmp = _user_profile.business.all()
        for _t in _tmp:
            _bs.append(_t.name)
        _groups = Groups.objects.filter(business__in = _bs)  

    _success = kw.get("success",False)
    _error = kw.get("error",False)

    _businesses = Businesses.objects.all()
    _success = kw.get("success",False)
    _error = kw.get("error",False)
    context={
        "groups":_groups,   
        "businesses":_businesses,
        "success":_success,
        "error":_error,
        }
    return render(request,"groups/manage_group.html",context)

@login_required(login_url="/account/login/")
def del_group(request):
    context={
        }
    _success=False
    _error=False
    _ids=request.POST.getlist("id")
    try:
        _filter=Groups.objects.filter(id__in=_ids)
        _filter.delete()
        _success="Delete opearation success!"
    except Exception as e:
        _error="Delete error!"
    #return render_to_response("groups/manage_group.html",context)
    #return HttpResponseRedirect("/groups/manage_group/",context) 
    return manage_group(request,success=_success,error=_error)

@login_required(login_url="/account/login/")
def modify_group(request):
    _success=False
    _error=False
    if request.method=="POST":
        _id=request.POST.get("id")
        _name=request.POST.get("name")
        _business=request.POST.get("business")
        _enabled=request.POST.get("enabled")
        _informations=request.POST.get("informations")
        if _enabled is not None:
            _enabled=True
        else:
            _enabled=False
        try:
            _group=Groups.objects.get(id=_id)
            _name_before=_group.name
            _group.name=_name
            _group.business=_business
            _group.enabled=_enabled
            _group.informations=_informations
            _group.save()
            _success="Modify Group "+ _name +" OK"
        except Exception as e:
            _error="Modify Group "+ _name +" failed"
            
        
    return manage_group(request,success=_success,error=_error)


@login_required(login_url="/account/login/")
def add_group(request):
    context={}
    _success=False
    _error=False
    if request.method=="POST":
        _name=request.POST.get("name")
        #_current_user=request.user
        _business=request.POST.get("business")
        _informations=request.POST.get("informations")
        if request.POST.get("enabled") == "true":
            _enabled=True
        else:
            _enabled=False
        try:
            print _name,_business,_informations,_enabled
            _group=Groups(name=_name,business=_business,informations=_informations,enabled=_enabled)
            _group.save()
            _success="Add Group "+_name+" OK!!"
        except Exception as e:
            _error="name already exists or too long!"
            
    else:
        pass
    return manage_group(request,success=_success,error=_error)
###########################  end manage group ################################
###########################  mange Host #######################   
@login_required(login_url="/account/login/")
def manage_host(request,*args,**kw):
    _current_user = request.user
    _u=User.objects.get(username=_current_user)
    _user_profile = UserProfiles.objects.get(user=_u)
    if _u.is_superuser == True:
        _groups = Groups.objects.all()
    else:
        _bs = []
        _tmp = _user_profile.business.all()
        for _t in _tmp:
            _bs.append(_t.name)
        _groups = Groups.objects.filter(business__in = _bs)  

    _hosts = Hosts.objects.filter(group__in=_groups)
    _minions = Minions_status.objects.filter(minion_config=False)
    _success = kw.get("success",False)
    _error = kw.get("error",False)
    context={
        "hosts":_hosts,   
        "groups":_groups,
        "minions":_minions,
        "success":_success,
        "error":_error,
        }
    return render(request,"groups/manage_host.html",context)

@login_required(login_url="/account/login/")
def del_host(request):
    _success=False
    _error=False
    _ids=request.POST.getlist("id")
    _minion_ids=[]
    try:
        _filter=Hosts.objects.filter(id__in=_ids)
        for _m in _filter:
            _minion_ids.append(_m.minion.id)
        #delete minion_status
        _m_filter = Minions_status.objects.filter(id__in=_minion_ids)
        _m_filter.delete()
        #delete hosts
        _filter.delete()
        _success="Delete opearation success!"
    except Exception as e:
        _error="Delete opearation error!"
    return manage_host(request,success=_success,error=_error)

@login_required(login_url="/account/login/")
def modify_host(request):
    _success=False
    _error=False
    if request.method=="POST":
        _id=request.POST.get("id")
        _m=request.POST.get("minion")
        _minion=Minions_status.objects.get(minion_id=_m)
        _g=request.POST.get("group")
        _group=Groups.objects.get(name=_g)
        _name=request.POST.get("name")
        _business=request.POST.get("business")
        _enabled=request.POST.get("enabled")
        _informations=request.POST.get("informations")
        if _enabled is not None:
            _enabled=True
        else:
            _enabled=False
        try:
            _host=Hosts.objects.get(id=_id)
            _name_before=_host.name
            _host.name=_name
            _host.minion=_minion
            _host.group=_group
            _host.business=_business
            _host.enabled=_enabled
            _host.informations=_informations
            _host.save()
            _success="Modify Host "+ _name +" OK"
        except Exception as e:
            _error="Modify Host "+ _name +" failed"
            
        
    return manage_host(request,success=_success,error=_error)
@login_required(login_url="/account/login/")
def add_host(request):
    _success=False
    _error=False
    if request.method=="POST":
        _m=request.POST.get("minion")
        _minion=Minions_status.objects.get(minion_id=_m)
        _g=request.POST.get("group")
        _group=Groups.objects.get(name=_g)
        _name=request.POST.get("name")
        _informations=request.POST.get("informations")
        if request.POST.get("enabled") == "true":
            _enabled=True
        else:
            _enabled=False
        try:
     
            _host=Hosts(minion=_minion,group=_group,name=_name,informations=_informations,enabled=_enabled)
            _host.save()
            _minion_status=Minions_status.objects.get(minion_id=_m)
            _minion_status.minion_config=True
            _minion_status.save()
            _success="Add Host "+_name+" OK!!"
        except Exception as e:
            _error="name already exists or too long!"
            
    else:
        pass
    return manage_host(request,success=_success,error=_error)
###########################  end manage Host ###########################
