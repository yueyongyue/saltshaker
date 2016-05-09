from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shaker.shaker_core import *
from minions.models import Minions_status
from returner.models import Salt_grains
from shaker.tasks import accept_grains_task, minions_status_task
import logging

logger = logging.getLogger('django')

@login_required(login_url="/account/login/")
def minions_status(request):
    status = Minions_status.objects.all()
    return render(request, 'minions/minions_status.html', {'status': status})

@login_required(login_url="/account/login/")
def minions_keys(request):
    sapi = SaltAPI()
    alert_info = ""
    if request.POST:
        minion_id_a = request.POST.get("accept")
        minion_id_r = request.POST.get("reject")
        minion_id_d = request.POST.get("delete")
        if minion_id_a:
            sapi.accept_key(minion_id_a)
            try:
                accept_grains_task.delay(minion_id_a)
            except Exception as e:
                logger.error(e)
            try:
                minions_status_task.delay()
                alert_info = "Minion: " + minion_id_a + " Accept Key Success"
            except Exception as e:
                alert_info = "Minion: " + minion_id_a + " Accept Key Fault"
                logger.error(e)
        elif minion_id_r:
            sapi.reject_key(minion_id_r)
        else:
            sapi.delete_key(minion_id_d)
            try:
                Minions_status.objects.get(minion_id=minion_id_d).delete()
            except Exception as e:
                logger.error(e)
            try:
                Salt_grains.objects.get(minion_id=minion_id_d).delete()
            except Exception as e:
                logger.error(e)
            try:
                minions_status_task.delay()
                alert_info = "Minion: " + minion_id_d + " Accept Key Success"
            except Exception as e:
                alert_info = "Minion: " + minion_id_d + " Accept Key Fault"
                logger.error(e)

    keys_all = sapi.list_all_key()

    return render(request, 'minions/minions_keys.html', {'key': keys_all, 'alert_info': alert_info})

@login_required(login_url="/account/login/")
def minions_asset_info(request):
    '''
    sapi = SaltAPI()
    up_host = sapi.runner_status('status')['up']
    jid = []
    disk_all = {}
    for hostname in up_host:
        info_all = sapi.remote_noarg_execution(hostname, 'grains.items')
        disk_use = sapi.remote_noarg_execution(hostname, 'disk.usage')
        for key in disk_use:
            disk_info = {key: int(disk_use[key]['capacity'][:-1])}
            disk_all.update(disk_info)
            disk_dic = {'disk': disk_all}
            info_all.update(disk_dic)
        disk_all = {}
        jid += [info_all]
    return render(request, 'minions/minions_asset_info.html', {'jyp': jid})
    '''
    salt_grains = Salt_grains.objects.all()
    asset_list = []
    for asset in salt_grains:
        asset_dic = {asset.minion_id.decode('string-escape'): eval(asset.grains)}
        asset_dics = asset_dic.copy()
        asset_list.append(asset_dics)
    return render(request, 'minions/minions_asset_info.html', {'asset': asset_list})

@login_required(login_url="/account/login/")
def minions_servers_status(request):
    return render(request, 'minions/minions_servers_status.html',)
