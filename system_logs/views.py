from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from system_logs.models import Logs, log2Extend
import logging

logger = logging.getLogger('django')

@login_required(login_url="/account/login/")
def logs(request):
    logs = log2Extend(Logs.objects.all())
    return render(request, 'system_logs/logs.html', {'logs': logs})