from django.shortcuts import render
from shaker.shaker_core import *
from shaker.nodegroups import *

def highstate(request):
    group = NodeGroups()
    all = group.list_groups_hosts()
    sapi = SaltAPI()
    jids = sapi.deploy('echo','init.nginx-full')['return'][0]
    return render(request,'states_config/highstate.html',{ 'list_groups': all } )
    #return render(request,'states_config/highstate.html',{ 'result': jids } )

def highstate_result(request):
    return render(request,'states_config/highstate_result.html')

