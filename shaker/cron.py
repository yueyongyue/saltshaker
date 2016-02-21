from shaker.shaker_core import *
from minions.models import Minions_status
from shaker.nodegroups import *


sapi = SaltAPI()

def dashboard_scheduled_job():
    # minion status
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

    salt_dashboard = file("/tmp/salt_dashboard.tmp", "w+")
    salt_dashboard.writelines(str(status_list) + '\n')
    salt_dashboard.writelines(str(os_release) + '\n')
    salt_dashboard.writelines(str(os_all) + '\n')
    salt_dashboard.close()

dashboard = dashboard_scheduled_job()


def minions_status_scheduled_job():
    #status_up = []
    #status_down = []
    group = NodeGroups()
    #sapi = SaltAPI()
    status = Minions_status()
    status_all = sapi.runner_status('status')
    for host_name in status_all['up']:
        version = sapi.remote_noarg_execution(host_name, 'grains.items')['saltversion']
        #version = "2015.5.5 (Lithium)"
        #version_dic = {'version': version}
        #group_dic = group.hosts_in_group(host_name)
        #status_dic = {'host': host_name}
        #status_dic.update(group_dic)
        #status_dic.update(version_dic)
        #status_up += [status_dic]
        #minion_id = Minions_status.objects.get(minion_id=host_name)
        #minion_id.delete()
        #status = Minions_status(minion_id=host_name)
        #update(blog=b)
        #if minion_id
        try:
            Minions_status.objects.get(minion_id=host_name)
        except:
            status.minion_id = host_name
            status.minion_version = version
            status.minion_status = 'Up'
            status.save()
        Minions_status.objects.filter(minion_id=host_name).update(minion_id=host_name, minion_version=version, minion_status='Up')
    for host_name in status_all['down']:
        #version_dic = {'version': ""}
        #group_dic = group.hosts_in_group(host_name)
        #status_dic = {'host': host_name}
        #status_dic.update(group_dic)
        #status_dic.update(version_dic)
        #status_down += [status_dic]
        #minion_id = Minions_status.objects.get(minion_id=host_name)
        #minion_id.delete()
        try:
            minion_id = Minions_status.objects.get(minion_id=host_name)
        except:
            status.minion_id = host_name
            status.minion_version = version
            status.minion_status = 'Down'
            status.save()
        Minions_status.objects.filter(minion_id=host_name).update(minion_id=host_name, minion_version=version, minion_status='Down')

minions_status = minions_status_scheduled_job()

