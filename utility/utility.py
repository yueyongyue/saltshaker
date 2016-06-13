# -*- coding:utf-8 -*-
#!/bin/env python
import os
import shutil

from django.conf import settings

def handle_uploaded_file(*args,**kwargs):
    _dest = kwargs.get("dir",None)
    _dir = os.path.dirname(_dest)
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    
    _f = kwargs.get("f",None)
    
    if _dest == None and _f == None:
        return False

    with open(_dest, 'wb+') as destination:
        for chunk in _f.chunks():
            destination.write(chunk)
        destination.close()
    return True

def walk_dir(*args,**kwargs):
    _files = {}
    base_dir = kwargs.get("base_root")
    if not base_dir.endswith("/"):
        base_dir = base_dir+"/"
    for root in  os.listdir(base_dir):
        path = base_dir+root
        if os.path.isdir(path):
            tmp = ["DIR","4",path]
            _files[root] = tmp
        else:
            size = round(os.path.getsize(path)/1024,3)
            
            tmp = ["FILE",size,path]
            _files[root] = tmp
    return _files

def delele_file(*args,**kwargs):
    _path = kwargs.get("path")
    try:
        if os.path.isdir(_path):
            shutil.rmtree(_path)
        else:
            os.remove(_path)
        return True
    except Exception as e :
        pass
        return False
