from django.db import models

'''
class Jids(models.Model):
    jid = models.CharField(max_length=225, blank=True, unique=True)
    load = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.jid, self.load)

class Salt_returns(models.Model):
    fun = models.CharField(max_length=50, blank=True)
    jid = models.CharField(max_length=255, blank=True)
    returns = models.TextField(blank=True)
    ids = models.CharField(max_length=255, blank=True)
    success = models.CharField(max_length=10, blank=True)
    full_ret = models.TextField(blank=True)
    alter_time = models.TimeField()

    def __unicode__(self):
        return u'%s %s' % (self.fun, self.jid)


class Salt_events(models.Model):
    id = models.IntegerField(max_length=20)
    tag = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.id, self.tag)
'''