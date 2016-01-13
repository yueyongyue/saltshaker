import os

class NodeGroups(object):
    def __init__(self):
        if os.path.isfile('/etc/salt/master.d/nodegroups.conf') == True:
            print ""
        else:
            nodegroups = file("/etc/salt/master.d/nodegroups.conf","w+")
            add = ["nodegroups:\n"]
            nodegroups.writelines(add)
            nodegroups.close()

    def list_groups(self):
        nodegroups = []
        os.system("sed '1d' /etc/salt/master.d/nodegroups.conf | awk '{print $1}' |awk -F: '{print $1}' > /tmp/nodegroups")
        nodegroup = open("/tmp/nodegroups","r").readlines()
        for i in nodegroup:
            z = i.split('\n')[0]
            nodegroups += [z]
        return nodegroups

    def list_groups_hosts(self):
        all_group_host = {}
        os.system("sed '1d' /etc/salt/master.d/nodegroups.conf | awk '{print $1}' |awk -F: '{print $1}' > /tmp/nodegroups")
        nodegroup = open("/tmp/nodegroups","r").readlines()
        for i in nodegroup:
            group = i.split('\n')[0]
            cmd = ''' sed -n "s/^  ''' + group + '''.*@/'/gp" /etc/salt/master.d/nodegroups.conf | sed -n "s/'//gp"'''
            hosts = os.popen(cmd).read().split('\n')[0].split(',')[0:-1]
            sort_hosts = sorted(hosts, key=lambda ele: ele)
            group_host_dic = {group: sort_hosts}
            all_group_host.update(group_host_dic)
        return all_group_host

    def add_groups(self,group):
        nodegroups = file("/etc/salt/master.d/nodegroups.conf","a+")
        group_name = "  " + group + ":" + " " + "'L@'\n"
        add = [group_name]
        nodegroups.writelines(add)
        nodegroups.close()

    def del_groups(self,group):
        if group.strip() == "":
            print "group null"
        else:
            cmd = "sed -i '/^  " + group + ":/d' /etc/salt/master.d/nodegroups.conf"
            os.system(cmd)

    def modify_groups(self,group,modify_group):
        cmd = "sed -i 's/^  " + group + ":/  " + modify_group + ":/g' /etc/salt/master.d/nodegroups.conf"
        os.system(cmd)

    def list_hosts(self,group):
        cmd = ''' sed -n "s/^  ''' + group + '''.*@/'/gp" /etc/salt/master.d/nodegroups.conf | sed -n "s/'//gp"'''
        hosts = os.popen(cmd).read().split('\n')[0].split(',')[0:-1]
        sort_hosts = sorted(hosts, key=lambda ele: ele)
        return sort_hosts

    def add_hosts(self,group,host):
        cmd = "sed -i 's/^  " + group + ":.*L@/&" + host + ",/g' /etc/salt/master.d/nodegroups.conf"
        os.system(cmd)

    def del_hosts(self,group,host):
        cmd = "sed -i '/.*" + group + ".*/s/" + host + ",//g' /etc/salt/master.d/nodegroups.conf"
        os.system(cmd)

    def hosts_in_group(self,host):
        cmd = "grep " + host + " /etc/salt/master.d/nodegroups.conf | awk -F: '{print $1}'"
        gname = os.popen(cmd).read()
        gname_dic = {'group': gname}
        return gname_dic



def main():
    host = NodeGroups()
    #c = host.list_groups_hosts()
    #b = host.del_hosts('SAX','192.168.10.8')
    #print  b
    # = host.list_hosts('Salt')
    #rint a
    c = host.hosts_in_group("echoeee")
    print c

if __name__ == '__main__':
    main()
