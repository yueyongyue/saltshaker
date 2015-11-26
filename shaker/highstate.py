import os

class HighState(object):
    def __init__(self):
        if os.path.isfile('/etc/salt/master.d/file_roots.conf') == True:
            print ""
        else:
            file_roots = file("/etc/salt/master.d/file_roots.conf","w+")
            add = ["file_roots:\n","  base:\n","    - /srv/salt\n"]
            file_roots.writelines(add)
            file_roots.close()


def main():
    highstate = HighState()



if __name__ == '__main__':
    main()

