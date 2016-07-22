# -*- coding:utf-8 -*-
from django.db import models
import datetime
class Logs(models.Model):
    class Meta:
        db_table = 'salt_logs'
    create_time = models.DateTimeField(default=datetime.datetime.now)
    username = models.CharField(max_length=64)
    content = models.CharField(max_length=255)
    log_type = models.IntegerField(default=0)
    log_level = models.IntegerField(default=1)

    def __unicode__(self):
        return self.username

class LogExtend():
    def __init__(self):
        self.id = None
        self.create_time = None
        self.usename = None
        self.content = None
        self.log_type = None
        self.log_level = None

def log2Extend(logs):
    log_level_dict = {0: u'DEBUG', 1: u'INFO', 2: u'WARN', 3: u'ERROR'}
    log_type_dict = {0: u'USER', 1: u'SYSTEM', 2: u'NOTICE', 3: u'OTHER'}
    item_list = []
    for log in logs:
        item = LogExtend()
        item.id = log.id
        item.create_time = log.create_time.strftime("%Y-%m-%d %H:%M:%S", )
        item.username = log.username
        item.content = log.content
        item.log_type = log_type_dict[log.log_type]
        item.log_level = log_level_dict[log.log_level]
        item_list.append(item)
    return item_list
