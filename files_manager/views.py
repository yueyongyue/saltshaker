# -*- coding:utf-8 -*-
#!/bin/env python

from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from groups.models import Groups,Hosts
from account.models import Businesses,Privileges,UserProfiles

from django.conf import settings
from utility.utility import handle_uploaded_file,walk_dir,delele_file

import os

base_dir = settings.FILE_BASE_DIR


# Create your views here.
@login_required(login_url="/account/login/")
def manage_file(request,*args,**kw):
    _u = request.user
    _user = User.objects.get(username=_u)

    _businesses = []
    all = {}
    try:
        if _user.is_superuser:
            _userprofile = UserProfiles.objects.all()
            _b = Businesses.objects.all()
        else:
            _userprofile = UserProfiles.objects.get(user=_user)
            _b = _userprofile.business.all()
        for _tmp in _b: 
            _businesses.append(_tmp.name)

        _groups=Groups.objects.filter(business__in = _businesses)
        for _group in _groups:
            _h=[]
            _hosts=_group.groups_hosts_related.all()
            for _host in _hosts:
                _h.append(_host.minion.minion_id)
                all[_group.name]=_h
    except Exception as e:
        pass

    if not os.path.exists(base_dir):
        os.mkdir(base_dir)

    _files = {}
    if request.GET.get("path"):
        path = request.GET.get("path")
        if os.path.isdir(path):
            _files = walk_dir(base_root = path)
    else:
        _files = walk_dir(base_root = base_dir)

    _success = kw.get("success",False)
    _error = kw.get("error",False)
    _results = kw.get("results",False)

    context={
        "error" : _error,
        "success" : _success,
        "results" : _results,
        "files": _files,
        "base_dir" : base_dir,
        }
    return render(request,'files_manager/manage_file.html',context)
@login_required(login_url="/account/login/")
def upload_file(request):
    if request.method == "POST":
        _results = []
        files = request.FILES.getlist("file")
        _target_dir = request.POST.get("target_dir")
        _target_dir = base_dir + _target_dir
        for file in files:
            #the type of var called file is <class 'django.core.files.uploadedfile.TemporaryUploadedFile'>
            dest = _target_dir + file.name
            _r = handle_uploaded_file(f=file,dir=dest,file=file.name)
            
            _results.append("Upload Status "+str(_r) + ' : ' + dest)
    return manage_file(request,results=_results)

@login_required(login_url="/account/login/")
def del_file(request):
    if request.method == "POST":
        _results = []
        _paths = request.POST.getlist("path")
        for _path in _paths:
            _r =  delele_file(path=_path)
            _results.append("Delete Status "+str(_r) + ' : ' + _path)

    return manage_file(request,results=_results)
        
