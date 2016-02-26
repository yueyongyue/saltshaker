from django.db import models
import datetime


class Jids(models.Model):
    class Meta:
        db_table = 'jids'
    jid = models.CharField(max_length=225, blank=True, unique=True)
    load = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.jid, self.load)

class Salt_returns(models.Model):
    class Meta:
        db_table = 'salt_returns'
    fun = models.CharField(max_length=50, blank=True)
    jid = models.CharField(max_length=255, blank=True)
    #`'return'` = models.TextField(blank=True)
    id = models.CharField(primary_key=True,max_length=255, blank=True)
    success = models.CharField(max_length=10, blank=True)
    full_ret = models.TextField(blank=True)
    alter_time = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return u'%s %s %s %s %s %s' % (self.fun, self.jid, self.id, self.success, self.full_ret, self.alter_time)

'''
class Salt_events(models.Model):
    id = models.IntegerField(max_length=20)
    tag = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.id, self.tag)
'''
