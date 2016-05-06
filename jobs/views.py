from django.shortcuts import render
from shaker.shaker_core import *
from django.contrib.auth.decorators import login_required
import os

@login_required(login_url="/account/login/")
def jobs_history(request):
    sapi = SaltAPI()
    jids = sapi.runner("jobs.list_jobs")
    return render(request, 'jobs/jobs_history.html', {'jids': jids})

@login_required(login_url="/account/login/")
def jobs_manage(request):
    sapi = SaltAPI()
    if request.POST:
        jid = request.POST.get("kill")
        kill = "salt '*' saltutil.kill_job" + " " + jid
        os.popen(kill)
    jids_running = sapi.runner("jobs.active")
    return render(request, 'jobs/jobs_manage.html', {'jids_running': jids_running})

@login_required(login_url="/account/login/")
def jobs_detail(request,jid):
    jids = "salt-run jobs.lookup_jid" + " " + jid
    detail = os.popen(jids).read()
    return render(request, 'jobs/jobs_detail.html', {'detail': detail})

@login_required(login_url="/account/login/")
def jobs_schedule(request):
    return render(request, 'jobs/jobs_schedule.html')