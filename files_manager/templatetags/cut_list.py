from django import template

register = template.Library()


@register.filter(is_safe=True)
def ListToStr(l,nu):
    return l[nu]
    


