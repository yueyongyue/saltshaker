from django.db import models
from django.contrib.auth.models import User

class Command_history(models.Model):
    class Meta:
        db_table = 'salt_command_history'
    command = models.CharField(max_length=50, blank=True)
    execute_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s %s %s' % (self.command, self.execute_time, self.user)


