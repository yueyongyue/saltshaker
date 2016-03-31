from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from shaker.shaker_core import *
from groups.models import Groups,Hosts,Businesses,Privileges
from minions.models import Minions_status


#######################  manage group ###########################
@login_required(login_url="/account/login/")
def manage_group(request,*args,**kw):
    print request.session
    _groups = Groups.objects.all()
    _owners = User.objects.all()
    _success = kw.get("success",False)
    _error = kw.get("error",False)
    context={
        "groups":_groups,   
        "owners":_owners,
        "success":_success,
        "error":_error,
        }
    return render_to_response("groups/manage_group.html",context)

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
        _success="Delete opearation successed!"
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
        print _id
        _name=request.POST.get("name")
        _business=request.POST.get("business")
        _enabled=request.POST.get("enabled")
        _informations=request.POST.get("informations")
        _privileges=request.POST.get("privileges")
        _o=request.POST.get("owner")
        _owner=User.objects.get(username=_o)
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
            _group.privileges=_privileges
            _group.owner=_owner
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
    context["owners"]=User.objects.all()
    if request.method=="POST":
        _name=request.POST.get("name")
        _privileges=request.POST.get("privileges")
        #_current_user=request.user
        _o=request.POST.get("owner")
        _owner=User.objects.get(username=_o)
        _business=request.POST.get("business")
        _informations=request.POST.get("informations")
        if request.POST.get("enabled") == "true":
            _enabled=True
        else:
            _enabled=False
        try:
            _group=Groups(name=_name,privileges=_privileges,owner=_owner,business=_business,informations=_informations,enabled=_enabled)
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
    _hosts = Hosts.objects.all()
    _owners = User.objects.all()
    _groups = Groups.objects.all()
    _minions = Minions_status.objects.filter(minion_config=False)
    _success = kw.get("success",False)
    _error = kw.get("error",False)
    context={
        "hosts":_hosts,   
        "owners":_owners,
        "groups":_groups,
        "minions":_minions,
        "success":_success,
        "error":_error,
        }
    return render_to_response("groups/manage_host.html",context)

@login_required(login_url="/account/login/")
def del_host(request):
    _success=False
    _error=False
    _ids=request.POST.getlist("id")
    try:
        _filter=Hosts.objects.filter(id__in=_ids)
        _filter.delete()
        _success="Delete opearation successed!"
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
        _privileges=request.POST.get("privileges")
        _o=request.POST.get("owner")
        _owner=User.objects.get(username=_o)
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
            _host.privileges=_privileges
            _host.owner=_owner
            _host.save()
            _success="Modify Group "+ _name +" OK"
        except Exception as e:
            _error="Modify Group "+ _name +" failed"
            
        
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
        _privileges=request.POST.get("privileges")
        #_current_user=request.user
        _o=request.POST.get("owner")
        _owner=User.objects.get(username=_o)
        _business=request.POST.get("business")
        _informations=request.POST.get("informations")
        print _minion,_group
        if request.POST.get("enabled") == "true":
            _enabled=True
        else:
            _enabled=False
        try:
            _host=Hosts(minion=_minion,group=_group,name=_name,privileges=_privileges,owner=_owner,business=_business,informations=_informations,enabled=_enabled)
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
###########################  mange business #######################   
@login_required(login_url="/account/login/")
def manage_business(request,*args,**kw):
    _businesses = Businesses.objects.all()
    _owners = User.objects.all()
    _success = kw.get("success",False)
    _error = kw.get("error",False)
    context={
        "businesses":_businesses,   
        "owners":_owners,
        "success":_success,
        "error":_error,
        }
    return render_to_response("groups/manage_business.html",context)

@login_required(login_url="/account/login/")
def del_business(request):
    _success=False
    _error=False
    _ids=request.POST.getlist("id")
    try:
        _filter=Businesses.objects.filter(id__in=_ids)
        _filter.delete()
        _success="Delete opearation successed!"
    except Exception as e:
        _error="Delete opearation error!"
            
    return manage_business(request,success=_success,error=_error)
@login_required(login_url="/account/login/")
def modify_business(request):
    _success=False
    _error=False
    if request.method=="POST":
        _id=request.POST.get("id")
        _name=request.POST.get("name")
        _enabled=request.POST.get("enabled")
        _informations=request.POST.get("informations")
        _o=request.POST.get("owner")
        _owner=User.objects.get(username=_o)
        if _enabled is not None:
            _enabled=True
        else:
            _enabled=False
        try:
            _business=Businesses.objects.get(id=_id)
            _name_before=_business.name
            _business.name=_name
            _business.enabled=_enabled
            _business.informations=_informations
            _business.owner=_owner
            _business.save()
            _success="Modify Business "+ _name +" OK"
        except Exception as e:
            _error="Modify Business "+ _name +" failed"
        
    return manage_business(request,success=_success,error=_error)
@login_required(login_url="/account/login/")
def add_business(request):
    _success=False
    _error=False
    if request.method=="POST":
        _name=request.POST.get("name")
        _o=request.POST.get("owner")
        _owner=User.objects.get(username=_o)
        _informations=request.POST.get("informations")
        if request.POST.get("enabled") == "true":
            _enabled=True
        else:
            _enabled=False
        try:
            _business=Businesses(name=_name,owner=_owner,informations=_informations,enabled=_enabled)
            _business.save()
            _success="Add business line "+_name+" OK!!"
        except Exception as e:
            _error="name already exists or too long!"
            
    else:
        pass
    return manage_business(request,success=_success,error=_error)
###########################  end mange business #######################   
###########################  mange privilege #######################   

@login_required(login_url="/account/login/")
def manage_privilege(request,*args,**kw):
    _privileges = Privileges.objects.all()
    _owners = User.objects.all()
    _success = kw.get("success",False)
    _error = kw.get("error",False)
    context={
        "privileges":_privileges,   
        "owners":_owners,
        "success":_success,
        "error":_error,
        }
    return render_to_response("groups/manage_privilege.html",context)

@login_required(login_url="/account/login/")
def del_privilege(request):
    _success=False
    _error=False
    _ids=request.POST.getlist("id")
    try:
        _filter=Privileges.objects.filter(id__in=_ids)
        _filter.delete()
        _success="Delete opearation successed!"
    except Exception as e:
        _error="Delete opearation error!"
            
    return manage_privilege(request,success=_success,error=_error)
@login_required(login_url="/account/login/")
def modify_privilege(request):
    _success=False
    _error=False
    if request.method=="POST":
        _id=request.POST.get("id")
        _name=request.POST.get("name")
        _enabled=request.POST.get("enabled")
        _informations=request.POST.get("informations")
        _o=request.POST.get("owner")
        _owner=User.objects.get(username=_o)
        if _enabled is not None:
            _enabled=True
        else:
            _enabled=False
        try:
            _privilege=Privileges.objects.get(id=_id)
            _name_before=_privilege.name
            _privilege.name=_name
            _privilege.enabled=_enabled
            _privilege.informations=_informations
            _privilege.owner=_owner
            _privilege.save()
            _success="Modify privilege "+ _name +" OK"
        except Exception as e:
            _error="Modify privilege "+ _name +" failed"
        
    return manage_privilege(request,success=_success,error=_error)
@login_required(login_url="/account/login/")
def add_privilege(request):
    _success=False
    _error=False
    if request.method=="POST":
        _name=request.POST.get("name")
        _o=request.POST.get("owner")
        _owner=User.objects.get(username=_o)
        _informations=request.POST.get("informations")
        if request.POST.get("enabled") == "true":
            _enabled=True
        else:
            _enabled=False
        try:
            _privilege=Privileges(name=_name,owner=_owner,informations=_informations,enabled=_enabled)
            _privilege.save()
            _success="Add privilege "+_name+" OK!!"
        except Exception as e:
            _error="name already exists or too long!"
            
    else:
        pass
    return manage_privilege(request,success=_success,error=_error)
###########################  end manage privilege ###########################
