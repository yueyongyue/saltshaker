from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from shaker.shaker_core import *
from shaker.nodegroups import *
from shaker.highstate import *
import os
import time



def system_tools(request):
    return render(request, 'system_setup/system_tools.html')