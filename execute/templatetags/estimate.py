from django import template

register = template.Library()

@register.filter(is_safe=True)
def to_str(value):
    if type(value) == list:
        value_str = '\n'.join(value)
        return value_str
    elif type(value) == dict:
        value_l = []
        for key in value:
            tmp = str(key) + '\n    ' + str(value[key])
            value_l.append(tmp)
        value_str = '\n'.join(value_l)
        return value_str
    else:
        return value

@register.filter(is_safe=True)
def sort_ip(ip_ob):
    try:
        ip_list = []
        for ip in ip_ob:
            ip_list.append(ip.minion.minion_id)
        ip_list.sort(lambda x, y: int(x.split('.')[3])-int(y.split('.')[3]))
        return ip_list
        _f.write(str(ip_list))
        _f.close()
    except:
        ip_list = []
        for ip in ip_ob:
            ip_list.append(ip.minion.minion_id)
        return ip_list



@register.filter(is_safe=True)
def ListToStr(l,nu):
    return l[nu]
    


