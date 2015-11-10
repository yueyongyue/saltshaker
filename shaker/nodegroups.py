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
        os.system("sed '1d' /etc/salt/master.d/nodegroups.conf | awk '{print $1}' |awk -F: '{print $1}' > /tmp/nodegroups")
        nodegroups = open("/tmp/nodegroups","r").readlines()
        return nodegroups

    def add_groups(self,group):
        nodegroups = file("/etc/salt/master.d/nodegroups.conf","a+")
        group_name = "  " + group + ":" + " " + "'L@'\n"
        add = [group_name]
        nodegroups.writelines(add)
        nodegroups.close()

    def del_groups(self,group):
        cmd = "sed -i '/" + group + ":/d' /etc/salt/master.d/nodegroups.conf"
        os.system(cmd)

    def modify_groups(self,group,modify_group):
        cmd = "sed -i 's/" + group + ":/" + modify_group + ":/g' /etc/salt/master.d/nodegroups.conf"
        os.system(cmd)

    def add_hosts(self,group,host):
        cmd = "sed -i 's/" + group + ":.*L@/&" + host + ",/' /etc/salt/master.d/nodegroups.conf"
        os.system(cmd)

    def del_hosts(self,host):
        cmd = "sed -i 's/" + host + ",//g' /etc/salt/master.d/nodegroups.conf"
        print cmd
        os.system(cmd)


def main():
    group = NodeGroups()
    a = group.add_groups("fgfvvvcgh")
    #print a

if __name__ == '__main__':
    main()
