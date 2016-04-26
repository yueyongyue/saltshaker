from django.db import models

class Dashboard_status(models.Model):
    class Meta:
        db_table = "dashboard_status"
    up = models.IntegerField(null=True, blank=True)
    down = models.IntegerField(null=True, blank=True)
    accepted = models.IntegerField(null=True, blank=True)
    unaccepted = models.IntegerField(null=True, blank=True)
    rejected = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return u'%s %s %s %s %s' % (self.up, self.down, self.accepted, self.unaccepted, self.rejected)

'''
class Dashboard_os(models.Model):
    class Meta:
        db_table = "dashboard_os"
    release = models.CharField(max_length=32, null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.release, self.count)
'''

class Dashboard_queue(models.Model):
    class Meta:
        db_table = "dashboard_queue"
    update_time = models.CharField(max_length=32, null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.update_time, self.count)