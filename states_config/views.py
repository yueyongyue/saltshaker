from django.shortcuts import render
from shaker.shaker_core import *
from shaker.nodegroups import *

def highstate(request):
    group = NodeGroups()
    all = group.list_groups_hosts()
    return render(request,'states_config/highstate.html',{ 'list_groups': all } )


