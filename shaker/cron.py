from shaker.shaker_core import *
from minions.models import Minions_status
from shaker.nodegroups import *
from dashboard.models import *
from returner.models import *
import logging
import subprocess
import time

logger = logging.getLogger('django')
sapi = SaltAPI()

def dashboard_scheduled_job():
    '''
    # minion status save to file
    status_list = []
    status = sapi.runner_status('status')
    key_status = sapi.list_all_key()
    up = len(status['up'])
    status_list.append(up)
    down = len(status['down'])
    status_list.append(down)
    accepted = len(key_status['minions'])
    status_list.append(accepted)
    unaccepted = len(key_status['minions_pre'])
    status_list.append(unaccepted)
    rejected = len(key_status['minions_rejected'])
    status_list.append(rejected)
    # os release
    up_host = status['up']
    os_list = []
    os_all = []
    for hostname in up_host:
        #info_all = sapi.remote_noarg_execution(hostname, 'grains.items')
        osfullname = sapi.grains(hostname, 'osfullname')[hostname]['osfullname'].decode('string-escape')
        osrelease = sapi.grains(hostname, 'osrelease')[hostname]['osrelease'].decode('string-escape')
        #osfullname = info_all['osfullname'].decode('string-escape')
        #osrelease = info_all['osrelease'].decode('string-escape')
        os = osfullname + osrelease
        os_list.append(os)
    os_uniq = set(os_list)
    for release in os_uniq:
        num = os_list.count(release)
        os_dic = {'value': num, 'name': release}
        os_all.append(os_dic)
    os_release = list(set(os_list))

    salt_dashboard = file("/var/cache/salt/master/salt_dashboard.tmp", "w+")
    salt_dashboard.writelines(str(status_list) + '\n')
    salt_dashboard.writelines(str(os_release) + '\n')
    salt_dashboard.writelines(str(os_all) + '\n')
    salt_dashboard.close()
    '''
    # minion status save to mysql
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



def minions_status_scheduled_job():
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



def grains_scheduled_job():
    salt_grains = Salt_grains()
    status = Minions_status.objects.filter(minion_status='Up')
    for host_name in status:
        grains = sapi.remote_noarg_execution(host_name.minion_id, 'grains.items')
        try:
            Salt_grains.objects.get(minion_id=host_name.minion_id)
        except:
            salt_grains.grains = grains
            salt_grains.minion_id = host_name.minion_id
            salt_grains.save()
        Salt_grains.objects.filter(minion_id=host_name.minion_id).update(grains=grains, minion_id=host_name.minion_id)


def dashboard_queue_scheduled_job():
    for i in range(0, 6):
        queued = subprocess.Popen("/usr/sbin/rabbitmqctl list_queues |grep -w celery |head -n 1 |awk '{printf $2}'", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        queued_stdout, queued_stderr = queued.communicate()
        now_time = time.strftime('%H:%M:%S', time.localtime())
        logger.error(queued_stderr)
        if len(Dashboard_queue.objects.all()) < 6:
            dashboard_queue = Dashboard_queue()
            dashboard_queue.count = int(queued_stdout)
            dashboard_queue.update_time = now_time
            dashboard_queue.save()
        else:
            dashboard_queue = Dashboard_queue()
            dashboard_queue.count = int(queued_stdout)
            dashboard_queue.update_time = now_time
            dashboard_queue.save()
            Dashboard_queue.objects.all()[0].delete()
        time.sleep(9)