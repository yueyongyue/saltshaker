from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from groups.models import Groups,Hosts
from account.models import UserProfiles,Businesses,Privileges

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
    _businesses = Businesses.objects.all()
    _privileges = Privileges.objects.all()
    _u=User.objects.get(username=_supermen)
    if _u.is_superuser == True:
        _users = UserProfiles.objects.all()
    else:
        _userobject = User.objects.get(username=_supermen)
        _users = [UserProfiles.objects.get(user=_userobject)]
    _success = kw.get("success",False)
    _error = kw.get("error",False)
    context={
        "users":_users,   
        "success":_success,
        "error":_error,
        "businesses":_businesses,
        "privileges":_privileges,
        }
    return render(request,"account/manage_user.html",context)

@login_required(login_url="/account/login/")
def del_user(request):
    _supermen = request.user
    _u=User.objects.get(username=_supermen)
    if _u.is_superuser == True:
        _users = UserProfiles.objects.all()
    else:
        return render_to_response("account/error.html",)
    _success = False
    _error = False
    _ids = request.POST.getlist("id")
    try:
        _filter = User.objects.filter(id__in=_ids)
        _filter.delete()
        _success = "Delete opearation successed!"
    except Exception as e:
        _error = "Delete opearation error!"
            
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
        else:
            _error="password error or the twice password not equal"
    return manage_user(request,success=_success,error=_error)

@login_required(login_url="/account/login/")
def setup_user(request):
    _supermen = request.user
    _u=User.objects.get(username=_supermen)
    if _u.is_superuser == True:
        _users = UserProfiles.objects.all()
    else:
        return render_to_response("account/error.html",)
    _success=False
    _error=False
    if request.method == "POST":

        _username = request.POST.get("username")
        _email = request.POST.get("email")
        _issuperuser = request.POST.get("issuperuser")
        _login_user = request.user
        
        _businesses = request.POST.getlist("business")
        _privileges =request.POST.getlist("privilege")

        _telephone = request.POST.get("telephone")
        _department = request.POST.get("department")

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
            _user.is_superuser = _issuperuser
            _user.save()
            # modify user profiles
            _userobject = User.objects.get(username=_username)
            _userprofile = UserProfiles.objects.get(user=_userobject)
            _userprofile.department = _department
            _userprofile.telephone = _telephone
            _userprofile.save()

            # clear relationship first
            _userprofile.privilege.clear()
            _userprofile.business.clear()
            # add relationship 
            for p in _privileges:
                if len(p) > 0:
                    _tmp = Privileges.objects.get(name=p)
                    _userprofile.privilege.add(_tmp)
            for b in _businesses:
                if len(b) > 0:  
                    _tmp = Businesses.objects.get(name=b)
                    _userprofile.business.add(_tmp)

            _success = "Modify user " + _username + " OK"

        except Exception as e:
            _error ="Modify user " + _username + " failed" 
       
    return manage_user(request,success=_success,error=_error)

@login_required(login_url="/account/login/")
def add_user(request):
    _success=False
    _error=False
    
    if request.method=="POST":
        _supermen = request.user
        _u=User.objects.get(username=_supermen)
        if _u.is_superuser == True:
            _users = UserProfiles.objects.all()
        else:
            return render_to_response("account/error.html",)
        _username = request.POST.get("username")
        _password = request.POST.get("password")
        _passwordagain = request.POST.get("passwordagain")
        _email = request.POST.get("email")

        _businesses = request.POST.getlist("business")
        _privileges = request.POST.getlist("privilege")

        _telephone = request.POST.get("telephone")
        _department = request.POST.get("department")

        if _password != _passwordagain:
            _error="the twice password that you typed not equal"
            return manage_user(request,success=_success,error=_error)
            
        if request.POST.get("superuser") == "true":
            _superuser=True
        else:
            _superuser=False
        try:
            _user=User.objects.create_user(username=_username,password=_password,email=_email)
            _user.is_superuser=_superuser
            _user.save()
            # add profile for user
            _userobject=User.objects.get(username=_username)
            _userprofile = UserProfiles(user=_userobject,department=_department,telephone=_telephone)

            _userprofile.save()
            
            for p in _privileges:
                if len(p) > 0:
                   _tmp = Privileges.objects.get(name=p)
                   _userprofile.privilege.add(_tmp)
            for b in _businesses:
                if len(b) > 0:
                    _tmp = Businesses.objects.get(name=b)
                    _userprofile.business.add(_tmp)

            _success="Add user "+_username+" OK!!"

        except Exception as e:
            _error="user already exists or too long!"
    else:
        pass
    return manage_user(request,success=_success,error=_error)

###########################  mange business #######################   
@login_required(login_url="/account/login/")
def manage_business(request,*args,**kw):
    _supermen = request.user
    _u=User.objects.get(username=_supermen)
    if _u.is_superuser == True:
        pass 
    else:
        return render_to_response("account/error.html",)
    _businesses = Businesses.objects.all()
    _success = kw.get("success",False)
    _error = kw.get("error",False)
    context={
        "businesses":_businesses,   
        "success":_success,
        "error":_error,
        }
    return render(request,"account/manage_business.html",context)

@login_required(login_url="/account/login/")
def del_business(request):
    _supermen = request.user
    _u=User.objects.get(username=_supermen)
    if _u.is_superuser == True:
        pass
    else:
        return render_to_response("account/error.html",)
    _success=False
    _error=False
    _ids=request.POST.getlist("id")
    try:
        _filter=Businesses.objects.filter(id__in=_ids)
        _filter.delete()
        _success="Delete opearation successed!"
    except Exception as e:
        _error="Delete opearation error!"
            
    return manage_business(request,success=_success,error=_error)
@login_required(login_url="/account/login/")
def modify_business(request):
    _supermen = request.user
    _u=User.objects.get(username=_supermen)
    if _u.is_superuser == True:
        pass
    else:
        return render_to_response("account/error.html",)
    _success=False
    _error=False
    if request.method=="POST":
        _id=request.POST.get("id")
        _name=request.POST.get("name")
        _enabled=request.POST.get("enabled")
        _informations=request.POST.get("informations")
        if _enabled is not None:
            _enabled=True
        else:
            _enabled=False
        try:
            _business=Businesses.objects.get(id=_id)
            _name_before=_business.name
            _business.name=_name
            _business.enabled=_enabled
            _business.informations=_informations
            _business.save()
            _success="Modify Business "+ _name +" OK"
        except Exception as e:
            _error="Modify Business "+ _name +" failed"
        
    return manage_business(request,success=_success,error=_error)
@login_required(login_url="/account/login/")
def add_business(request):
    _supermen = request.user
    _u=User.objects.get(username=_supermen)
    if _u.is_superuser == True:
        pass
    else:
        return render_to_response("account/error.html",)
    _success=False
    _error=False
    if request.method=="POST":
        _name=request.POST.get("name")
        _informations=request.POST.get("informations")
        if request.POST.get("enabled") == "true":
            _enabled=True
        else:
            _enabled=False
        try:
            _business=Businesses(name=_name,informations=_informations,enabled=_enabled)
            _business.save()
            _success="Add business line "+_name+" OK!!"
        except Exception as e:
            _error="name already exists or too long!"
            
    else:
        pass
    return manage_business(request,success=_success,error=_error)
###########################  end mange business #######################   
###########################  mange privilege #######################   

@login_required(login_url="/account/login/")
def manage_privilege(request,*args,**kw):
    _supermen = request.user
    _u=User.objects.get(username=_supermen)
    if _u.is_superuser == True:
        pass
    else:
        return render_to_response("account/error.html",)
    _privileges = Privileges.objects.all()
    _success = kw.get("success",False)
    _error = kw.get("error",False)
    context={
        "privileges":_privileges,   
        "success":_success,
        "error":_error,
        }
    return render(request,"account/manage_privilege.html",context)

@login_required(login_url="/account/login/")
def del_privilege(request):
    _supermen = request.user
    _u=User.objects.get(username=_supermen)
    if _u.is_superuser == True:
        pass
    else:
        return render_to_response("account/error.html",)
    _success=False
    _error=False
    _ids=request.POST.getlist("id")
    try:
        _filter=Privileges.objects.filter(id__in=_ids)
        _filter.delete()
        _success="Delete opearation successed!"
    except Exception as e:
        _error="Delete opearation error!"
            
    return manage_privilege(request,success=_success,error=_error)
@login_required(login_url="/account/login/")
def modify_privilege(request):
    _supermen = request.user
    _u=User.objects.get(username=_supermen)
    if _u.is_superuser == True:
        pass
    else:
        return render_to_response("account/error.html",)
    _success=False
    _error=False
    if request.method=="POST":
        _id=request.POST.get("id")
        _name=request.POST.get("name")
        _allow=request.POST.get("allow")
        _deny=request.POST.get("deny")
        _enabled=request.POST.get("enabled")
        _informations=request.POST.get("informations")
        if _enabled is not None:
            _enabled=True
        else:
            _enabled=False
        try:
            _privilege=Privileges.objects.get(id=_id)
            _name_before=_privilege.name
            _privilege.name=_name
            _privilege.allow=_allow
            _privilege.deny=_deny
            _privilege.enabled=_enabled
            _privilege.informations=_informations
            _privilege.save()
            _success="Modify privilege "+ _name +" OK"
        except Exception as e:
            _error="Modify privilege "+ _name +" failed"
        
    return manage_privilege(request,success=_success,error=_error)
@login_required(login_url="/account/login/")
def add_privilege(request):
    _supermen = request.user
    _u=User.objects.get(username=_supermen)
    if _u.is_superuser == True:
        pass
    else:
        return render_to_response("account/error.html",)
    _success=False
    _error=False
    if request.method=="POST":
        _name=request.POST.get("name")
        _deny=request.POST.get("deny")
        _allow=request.POST.get("allow")
        _informations=request.POST.get("informations")
        if request.POST.get("enabled") == "true":
            _enabled=True
        else:
            _enabled=False
        try:
            _privilege=Privileges(name=_name,allow=_allow,deny=_deny,informations=_informations,enabled=_enabled)
            _privilege.save()
            _success="Add privilege "+_name+" OK!!"
        except Exception as e:
            _error="name already exists or too long!"
            
    else:
        pass
    return manage_privilege(request,success=_success,error=_error)
###########################  end manage privilege ###########################
