import os

class HighState(object):
    def __init__(self):
        if os.path.isfile('/etc/salt/master.d/file_roots.conf') == True:
            print ""
        else:
            file_roots = file("/etc/salt/master.d/file_roots.conf", "w+")
            add = ["file_roots:\n", "  base:\n", "    - /srv/salt\n"]
            file_roots.writelines(add)
            file_roots.close()

    def list_sls(self, dir):
        all_sls = {}
        list_filename = os.listdir(dir)
        for filename in list_filename:
            content = open(dir+filename).readlines()
            name = filename.split('.')[0]
            dic_sls = {name: content}
            all_sls.update(dic_sls)
        return all_sls

    def add_sls(self, filename, content):
        files = file("/srv/salt/"+filename+".sls", "w+")
        files.writelines(content)
        files.close()



def main():
    highstate = HighState()
    #a = highstate.list_sls("/srv/salt/")
    b = ['12345\n','  67890f\n']
    a = highstate.add_sls("rsync", b)
    print a



if __name__ == '__main__':
    main()

