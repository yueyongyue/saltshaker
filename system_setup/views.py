from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from shaker.tasks import grains_task
import logging
from dashboard.models import *
from returner.models import *
from shaker.shaker_core import *
from shaker.nodegroups import *
from shaker.highstate import *
import os
import time

logger = logging.getLogger('django')

@login_required(login_url="/account/login/")
def system_tools(request):
    return render(request, 'system_setup/system_tools.html')


@login_required(login_url="/account/login/")
def update_grains(request):
    if request.POST:
        try:
            logger.info('dfdfdfdfd')
            grains_task.delay()
        except Exception as e:
            logger.error(e)

    return render(request, 'system_setup/system_tools.html')

