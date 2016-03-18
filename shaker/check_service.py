#!/usr/bin/env python
import os
import socket

def CheckPort(service, ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return {service: 'Up'}
    except:
        return {service: 'Down'}

def CheckProgress(service, name):
    progress = os.popen('ps aux | grep "' + name + '" | grep -v grep').readlines()
    if progress:
        return {service: 'Up'}
    else:
        return {service: 'Down'}

if __name__ == '__main__':
    CheckPort('salt_master', '127.0.01', 4505)
    CheckProgress('celery','celery')