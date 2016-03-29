from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import logging
ErrorLogger = logging.getLogger("error")
AccessLogger = logging.getLogger("access")



def login_view(request):
    msg = []
    if request.POST:
        if len(request.POST.get('next')) > 0:
            _next = request.POST.get('next')
        else:
            _next = "/"
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(_next)
            else:
                msg.append("Disabled account")
        else:
            msg.append("Password error")
    return render(request, 'account/login.html', {'errors': msg})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/account/login')


@login_required(login_url="/account/login/")
def manage_user(request,*args,**kw):
    _supermen = request.user
    _u=User.objects.get(username=_supermen)
    if _u.is_superuser == True:
        _users = User.objects.all()
    else:
        _users = [User.objects.get(username=_supermen)]
    _success = kw.get("success",False)
    _error = kw.get("error",False)
    context={
        "users":_users,   
        "success":_success,
        "error":_error,
        }
    AccessLogger.info(request.path)
    return render_to_response("account/manage_user.html",context)

@login_required(login_url="/account/login/")
def del_user(request):
    _success = False
    _error = False
    _ids = request.POST.getlist("id")
    try:
        _filter = User.objects.filter(id__in=_ids)
        _filter.delete()
        _success = "Delete opearation successed!"
    except Exception as e:
        _error = "Delete opearation error!"
        ErrorLogger.error(str(e))
            
    return manage_user(request,success=_success,error=_error)
@login_required(login_url="/account/login/")
def set_password(request):
    _success=False
    _error=False
    if request.method == "POST":
        _username = request.POST.get("username")
        _origin = request.POST.get("origin")
        _new = request.POST.get("new")
        _newagain = request.POST.get("newagain")
        print _username,_origin,_new,_newagain
        if _new == _newagain and len(_new)>0:
            try:
                _user=User.objects.get(username=_username)
                user = authenticate(username=_username, password=_origin)
                if user is not None and user.is_active:
                    _user.set_password(_new)
                    _user.save()
                    _success = "Set password for "+ _username +" OK"
                else:
                    _error = "Origin password is not correct!"
            except Exception as e:
                _error="Set password for "+ _username +" failed"
                ErrorLogger.error(str(e))
        else:
            _error="password error or the twice password not equal"
    return manage_user(request,success=_success,error=_error)

@login_required(login_url="/account/login/")
def setup_user(request):
    _success=False
    _error=False
    if request.method == "POST":
        _username = request.POST.get("username")
        _email = request.POST.get("email")
        _issuperuser = request.POST.get("issuperuser")
        _login_user = request.user
        if User.objects.get(username=_login_user).is_superuser == True:
            if _issuperuser is not None:
                _issuperuser = True
            else:
                _issuperuser = False  
        else:
            _issuperuser = False
        try:
            _user = User.objects.get(username=_username)
            _user.email = _email
            _user.issuperuser = _issuperuser
            _user.save()
            _success = "modify user " + _username + " OK"
        except Exception as e:
            print str(e)
            _error ="your don't have permission to do this!" 
       
    return manage_user(request,success=_success,error=_error)
@login_required(login_url="/account/login/")

@login_required(login_url="/account/login/")
def add_user(request):
    _success=False
    _error=False
    if request.method=="POST":
        _username=request.POST.get("username")
        _password=request.POST.get("password")
        _passwordagain=request.POST.get("passwordagain")
        _email=request.POST.get("email")
        if _password != _passwordagain:
            _error="the twice password you typed not equal"
            return manage_user(request,success=_success,error=_error)
            
        if request.POST.get("superuser") == "true":
            _superuser=True
        else:
            _superuser=False
        try:
            _user=User.objects.create_user(username=_username,password=_password,email=_email)
            _user.is_superuser=_superuser
            _user.save()
            _success="Add user "+_username+" OK!!"
        except Exception as e:
            _error="user already exists or too long!"
            ErrorLogger.error(str(e))
    else:
        pass
    return manage_user(request,success=_success,error=_error)

@login_required(login_url="/account/login/")
def SuperUser(request):
    return HttpResponse("coding")
