#-*- coding:utf-8 -*-
from django.db import models



class Minions_status(models.Model):
    class Meta:
        db_table = "minions_status"
    minion_id = models.CharField(max_length=128, null=True, blank=True)
    minion_version = models.CharField(max_length=128, null=True, blank=True)
    minion_status = models.CharField(max_length=128, null=True, blank=True)
    minion_config = models.BooleanField(default=False)


    def __unicode__(self):
        return u'%s %s %s' % (self.minion_id, self.minion_version, self.minion_status)