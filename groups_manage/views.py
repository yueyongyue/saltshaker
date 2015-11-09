from django.shortcuts import render
from django.http import JsonResponse
from shaker.shaker_core import *
from shaker.nodegroups import *
from django.http import HttpResponse


def add_group(request):
    group = NodeGroups()
    all_group = group.list_groups()
    return render(request,'groups_manage/add_group_test.html',{ 'list_groups':all_group })

def jobs_manage(request):
    sapi = SaltAPI()
    jids_running = sapi.runner("jobs.active")
    return render(request,'jobs/jobs_manage.html',{ 'jids_running': jids_running })

def ajax_list(request):
    group = NodeGroups()
    all_group = group.list_groups()
    return JsonResponse(all_group, safe=False)

def ajax_dict(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return JsonResponse(name_dict)

def add(request, a, b):
    if request.is_ajax():
        ajax_string = 'ajax request: '
    else:
        ajax_string = 'not ajax request: '
    c = int(a) + int(b)
    r = HttpResponse(ajax_string + str(c))
    return r

def del_group(request):
    group = NodeGroups()
    if request.POST:
        hostname = request.POST
        for key in hostname:
            a = hostname.get(key)
            group.del_groups(a)
            return HttpResponse(a)
    #    group.del_groups(groups)







