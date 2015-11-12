from django.shortcuts import render
from django.http import JsonResponse
from shaker.shaker_core import *
from shaker.nodegroups import *
from django.http import HttpResponse


def all_group(request):
    group = NodeGroups()
    all_group = group.list_groups()
    return render(request,'groups_manage/add_group_test.html',{ 'list_groups':all_group })

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
        hostname = request.POST
        for key in hostname:
            a = hostname.get(key)
            group.del_groups(a)
            return HttpResponse(a)

def modify_group(request):
    group = NodeGroups()
    if request.POST:
        groups = request.POST
        for key in groups:
            group_name = groups.get(key)
            a = group_name + "1234"
            group.modify_groups(group_name,a)
            return HttpResponse("ok")


def ajax_list(request):
    group = NodeGroups()
    all_group = group.list_groups()
    return JsonResponse(all_group, safe=False)

def ajax_dict(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return JsonResponse(name_dict)







