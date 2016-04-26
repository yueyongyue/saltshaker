from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from shaker.tasks import grains_task
import logging
import subprocess
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
        update = request.POST.get("update")
        if update:
            try:
                grains_task.delay()
            except Exception as e:
                logger.error(e)
    return render(request, 'system_setup/system_tools.html')

@login_required(login_url="/account/login/")
def restart_server(request):
    if request.POST:
        server = request.POST.get("restart")
        if server == 'master':
            restart_master = subprocess.Popen("/etc/init.d/salt-minion restart", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            restart_master_stdout, restart_master_stderr = restart_master.communicate()
            logging.error(restart_master_stderr)
        elif server == 'api':
            restart_api = subprocess.Popen("/etc/init.d/salt-api restart", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            restart_api_stdout, restart_api_stderr = restart_api.communicate()
            logging.error(restart_api_stderr)
        elif server == 'minion':
            restart_minion = subprocess.Popen("/etc/init.d/salt-minion start", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            restart_minion_stdout, restart_minion_stderr = restart_minion.communicate()
            logging.error(restart_minion_stderr)
        elif server == 'rabbitmq':
            restart_rabbitmq = subprocess.Popen("/etc/init.d/rabbitmq-server restart", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            restart_rabbitmq_stdout, restart_rabbitmq_stderr = restart_rabbitmq.communicate()
            logging.error(restart_rabbitmq_stderr)
        elif server == 'management':
            restart_management = subprocess.Popen("/etc/init.d/rabbitmq-server restart", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            restart_management_stdout, restart_management_stderr = restart_management.communicate()
            logging.error(restart_management_stderr)
        else:
            restart_celery = subprocess.Popen("/etc/init.d/salt-minion restart", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            restart_celery_stdout, restart_celery_stderr = restart_celery.communicate()
            logging.error(restart_celery_stderr)

    return render(request, 'system_setup/system_tools.html')
