from shaker.shaker_core import *

def dashboard_scheduled_job(self):
    print "a"

''''
#class Dashboard(object):
def dashboard_scheduled_job(self):
    # minion status
    status_list = []
    sapi = SaltAPI()
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
        info_all = sapi.remote_noarg_execution(hostname, 'grains.items')
        #osfullname = sapi.grains(hostname,'osfullname')[hostname]['osfullname']
        #osrelease = sapi.grains(hostname,'osrelease')[hostname]['osrelease']
        osfullname = info_all['osfullname']
        osrelease = info_all['osrelease']
        os = osfullname + osrelease
        os_list.append(os)
    os_uniq = set(os_list)
    for release in os_uniq:
        num = os_list.count(release)
        os_dic = {'value': num, 'name': release}
        os_all.append(os_dic)
    os_release = list(set(os_list))

    salt_dashboard = file("/tmp/salt_dashboard.tmp","w+")
    #status_list_tmp = [status_list + "\n"]
    #os_release_tmp = [os_release + "\n"]
    #os_all_tmp = [os_all + "\n"]
    print status_list
    print os_release
    print os_all
    salt_dashboard.writelines(str(status_list) + '\n')
    salt_dashboard.writelines(str(os_release) + '\n')
    salt_dashboard.writelines(str(os_all) + '\n')
    salt_dashboard.close()

def main():
    a = Dashboard()
    a.dashboard_scheduled_job()

if __name__ == '__main__':
    main()
'''