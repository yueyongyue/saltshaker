from django import template

register = template.Library()

@register.filter(is_safe=True)
def to_str(value):
    if type(value) == list:
        value_str = '\n'.join(value)
        return value_str
    elif type(value) == dict:
        b = ''
        for key, values in value.items():
            a = key + '\n    ' + values
            #b = a + b
            return a
    else:
        return value



