from system_logs.models import Logs

def system_logs_save(username,content,log_type,log_level,*args):
    logs = Logs()
    logs.username = username
    logs.content = content
    logs.log_type = log_type
    logs.log_level = log_level
    logs.save()