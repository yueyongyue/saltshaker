from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse



@login_required(login_url="/account/login/")
def index(request):
    return render(request,'dashboard/index.html',)



