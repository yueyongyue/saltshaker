from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from shaker.shaker_core import *
from shaker.nodegroups import *



def manage_group(request):
    group = NodeGroups()
    all_group = group.list_groups()
    return render(request,'groups/manage_group.html',{ 'list_groups': all_group })

def add_group(request):
    group = NodeGroups()
    if request.POST:
        groups = request.POST
        for key in groups:
            group_name = groups.get(key)
            group.add_groups(group_name)
            return HttpResponse(group_name)

def del_group(request):
    group = NodeGroups()
    if request.POST:
        groups = request.POST
        for key in groups:
            group_name = groups.get(key)
            group.del_groups(group_name)
            return HttpResponse(group_name)

def modify_group(request):
    group = NodeGroups()
    if request.POST:
        group_name = request.POST.get("groups_name")
        modify_group_name = request.POST.get("modify")
        group.modify_groups(group_name,modify_group_name)
        return HttpResponse(group_name)


def manage_host(request):
    group = NodeGroups()
    all = group.list_groups_hosts()
    return render(request,'groups/manage_host.html',{ 'list_groups':all })

def add_host(request):
    host = NodeGroups()
    if request.POST:
        group_name = request.POST.get("groups_name")
        host_name = request.POST.get("hosts_name")
        host.add_hosts(group_name,host_name)
        return HttpResponse(host_name)

def del_host(request):
    host = NodeGroups()
    if request.POST:
        group_name = request.POST.get("groups_name")
        host_name = request.POST.get("hosts_name")
        host.del_hosts(group_name,host_name)
        return HttpResponse(host_name)







