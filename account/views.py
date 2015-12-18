from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

def login_view(request):
    msg = []
    #if request.GET:
    #    request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    #elif request.POST:
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/')
            else:
                msg.append("Disabled account")
        else:
            msg.append("Password error")
    return render(request, 'account/login.html', {'errors': msg})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('../account/login')

