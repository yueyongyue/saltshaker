from django.db import models
from django.contrib.auth.models import User


class Command_history(models.Model):
    class Meta:
        db_table = 'salt_command_history'
    command = models.TextField(null=True, blank=True)
    command_tag = models.IntegerField(null=True, blank=True)
    execute_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s %s %s' % (self.command, self.execute_time, self.user)

class Modindex(models.Model):
    class Meta:
        db_table = 'salt_modindex'
    module_name = models.TextField(null=True, blank=True)
    module_fun = models.TextField(null=True, blank=True)
    module_des = models.TextField(null=True, blank=True)
    module_exa = models.TextField(null=True, blank=True)


    def __unicode__(self):
        return u'%s %s %s' % (self.module_name, self.module_fun, self.module_des)




