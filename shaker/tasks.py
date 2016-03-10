from celery import task
from shaker.shaker_core import *
from minions.models import Minions_status
from dashboard.models import *
from returner.models import *
import logging

logger = logging.getLogger('django')
sapi = SaltAPI()

@task()
def dashboard_task():
    # minion status data save to mysql
    status = sapi.runner_status('status')
    key_status = sapi.list_all_key()
    up = len(status['up'])
    down = len(status['down'])
    accepted = len(key_status['minions'])
    unaccepted = len(key_status['minions_pre'])
    rejected = len(key_status['minions_rejected'])
    dashboard_status = Dashboard_status()
    try:
        Dashboard_status.objects.get(id=1)
    except:
        dashboard_status.id = 1
        dashboard_status.up = up
        dashboard_status.down = down
        dashboard_status.accepted = accepted
        dashboard_status.unaccepted = unaccepted
        dashboard_status.rejected = rejected
        dashboard_status.save()
    Dashboard_status.objects.filter(id=1).update(id=1, up=up, down=down, accepted=accepted, unaccepted=unaccepted, rejected=rejected)

@task()
def grains_task():
    # grains data save to mysql
    salt_grains = Salt_grains()
    minions_status = Minions_status()
    status = sapi.runner_status('status')
    status_up = status['up']
    status_down = status['down']
    for host_name in status_up:
        grains = sapi.remote_noarg_execution(host_name, 'grains.items')
        try:
            Salt_grains.objects.get(minion_id=host_name)
        except:
            salt_grains.grains = grains
            salt_grains.minion_id = host_name
            salt_grains.save()
        Salt_grains.objects.filter(minion_id=host_name).update(grains=grains, minion_id=host_name)

    # minion status , version data save to mysql
    for host_name in status_up:
        salt_grains = Salt_grains.objects.filter(minion_id=host_name)
        version = eval(salt_grains[0].grains).get('saltversion').decode('string-escape')
        try:
            Minions_status.objects.get(minion_id=host_name)
        except:
            minions_status.minion_id = host_name
            minions_status.minion_version = version
            minions_status.minion_status = 'Up'
            minions_status.save()
        Minions_status.objects.filter(minion_id=host_name).update(minion_id=host_name, minion_version=version, minion_status='Up')
    for host_name in status_down:
        try:
            Minions_status.objects.get(minion_id=host_name)
        except:
            minions_status.minion_id = host_name
            minions_status.minion_version = version
            minions_status.minion_status = 'Down'
            minions_status.save()
        Minions_status.objects.filter(minion_id=host_name).update(minion_id=host_name, minion_version=version, minion_status='Down')


'''
@task()
def minions_status_task():
    status = Minions_status()
    status_all = sapi.runner_status('status')
    for host_name in status_all['up']:
        salt_grains = Salt_grains.objects.filter(minion_id=host_name)
        version = eval(salt_grains[0].grains).get('saltversion').decode('string-escape')
        try:
            Minions_status.objects.get(minion_id=host_name)
        except:
            status.minion_id = host_name
            status.minion_version = version
            status.minion_status = 'Up'
            status.save()
        Minions_status.objects.filter(minion_id=host_name).update(minion_id=host_name, minion_version=version, minion_status='Up')
    for host_name in status_all['down']:
        try:
            Minions_status.objects.get(minion_id=host_name)
        except:
            status.minion_id = host_name
            status.minion_version = version
            status.minion_status = 'Down'
            status.save()
        Minions_status.objects.filter(minion_id=host_name).update(minion_id=host_name, minion_version=version, minion_status='Down')
'''
