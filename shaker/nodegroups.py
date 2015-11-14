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
        return hosts

    def add_hosts(self,group,host):
        cmd = "sed -i 's/^  " + group + ":.*L@/&" + host + ",/' /etc/salt/master.d/nodegroups.conf"
        os.system(cmd)

    def del_hosts(self,host):
        cmd = "sed -i 's/" + host + ",//g' /etc/salt/master.d/nodegroups.conf"
        os.system(cmd)


def main():
    host = NodeGroups()
    #b = host.add_hosts('SAX','192.168.10.8')
    #print  b
    a = host.list_hosts('DMP0001')
    print a

if __name__ == '__main__':
    main()
