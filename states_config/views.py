from django.shortcuts import render
from shaker.shaker_core import *
from shaker.nodegroups import *
from shaker.highstate import *

def highstate(request):
    group = NodeGroups()
    high = HighState()
    all_host = group.list_groups_hosts()
    all_sls = high.list_sls('/srv/salt/')
    #sapi = SaltAPI()
    #jids = sapi.deploy('echo','init.nginx-full')['return'][0]
    return render(request, 'states_config/highstate.html', {'list_groups': all_host, 'all_sls': all_sls})
    #return render(request,'states_config/highstate.html',{ 'result': jids } )

def highstate_result(request):
    return render(request,'states_config/highstate_result.html')

