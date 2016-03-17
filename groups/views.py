from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from shaker.shaker_core import *
from groups.models import Groups,Hosts


@login_required(login_url="/account/login/")
def manage_group(request,*args,**kw):
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
    context={}
    context["owners"]=User.objects.all()
    if request.method=="GET":
        _name=request.GET.get("name")
        _info=Groups.objects.get(name=_name)
        context["info"]=_info
    if request.method=="POST":
        _id=request.POST.get("id")
        _name=request.POST.get("name")
        _business=request.POST.get("business")
        _enabled=request.POST.get("enabled")
        print _enabled
        _informations=request.POST.get("informations")
        _privileges=request.POST.get("privileges")
        _o=request.POST.get("owner")
        _owner=User.objects.get(username=_o)
        if _enabled is not None:
            _enabled=True
        else:
            _enabled=False
        _save=request.POST.get("save")
        if _save=="save":
            _group=Groups.objects.get(id=_id)
            _name_before=_group.name
            _group.name=_name
            _group.business=_business
            _group.enabled=_enabled
            _group.informations=_informations
            _group.privileges=_privileges
            _group.owner=_owner
            _group.save()
        _info=Groups.objects.get(name=_name)
        context["info"]=_info
        context["result"]="Edit Group " + _name_before + " OK!!"
        
    return render_to_response("groups/modify_group.html",context)


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
    #return render_to_response("groups/manage_group.html",context)
    #return HttpResponseRedirect("/groups/manage_group/",context) 
    return manage_group(request,success=_success,error=_error)

@login_required(login_url="/account/login/")
def manage_host(request):
    group = NodeGroups()
    all = group.list_groups_hosts()
    return render(request, 'groups/manage_host.html', {'list_groups': all})

@login_required(login_url="/account/login/")
def add_host(request):
    host = NodeGroups()
    if request.POST:
        group_name = request.POST.get("groups_name")
        host_name = request.POST.get("hosts_name")
        host.add_hosts(group_name, host_name)
        return HttpResponse(host_name)

@login_required(login_url="/account/login/")
def del_host(request):
    host = NodeGroups()
    if request.POST:
        group_name = request.POST.get("groups_name")
        host_name = request.POST.get("hosts_name")
        host.del_hosts(group_name, host_name)
        return HttpResponse(host_name)







