from django import template

register = template.Library()


@register.filter
def concatenate_str(arg1, arg2):
    return str(arg1) + str(arg2)


@register.simple_tag
def add_one(val=None):
    return val+1
