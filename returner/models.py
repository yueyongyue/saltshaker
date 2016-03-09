from django.db import models
from datetime import datetime
from time import strftime

class UnixTimestampField(models.DateTimeField):
    """UnixTimestampField: creates a DateTimeField that is represented on the
    database as a TIMESTAMP field rather than the usual DATETIME field.
    """
    def __init__(self, null=False, blank=False, **kwargs):
        super(UnixTimestampField, self).__init__(**kwargs)
        # default for TIMESTAMP is NOT NULL unlike most fields, so we have to
        # cheat a little:
        self.blank, self.isnull = blank, null
        self.null = True # To prevent the framework from shoving in "not null".

    def db_type(self, connection):
        typ=['TIMESTAMP']
        # See above!
        if self.isnull:
            typ += ['NULL']
        if self.auto_created:
            typ += ['default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP']
        return ' '.join(typ)

    def to_python(self, value):
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        else:
            return models.DateTimeField.to_python(self, value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value==None:
            return None
        # Use '%Y%m%d%H%M%S' for MySQL < 4.1
        return strftime('%Y-%m-%d %H:%M:%S',value.timetuple())

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
    returns = models.TextField(blank=True)
    minion_id = models.CharField(max_length=255, blank=True)
    success = models.CharField(max_length=10, blank=True)
    full_ret = models.TextField(blank=True)
    alter_time = UnixTimestampField(auto_created=True)

    def __unicode__(self):
        return u'%s %s %s %s %s %s %s' % (self.fun, self.jid, self.returns, self.minion_id, self.success, self.full_ret, self.alter_time)

class Salt_events(models.Model):
    class Meta:
        db_table = 'salt_events'
    tag = models.CharField(max_length=255, blank=True)
    data = models.TextField(blank=True)
    alter_time = UnixTimestampField(auto_created=True)
    minion_id = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return u'%s %s %s %s' % (self.tag, self.data, self.alter_time, self.minion_id)

class Salt_grains(models.Model):
    class Meta:
        db_table = 'salt_grains'
    minion_id = models.CharField(max_length=255, null=True, blank=True)
    grains = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.minion_id, self.grains)

