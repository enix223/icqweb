from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def settings_value(name):
    '''Get value from Settings module'''
    return getattr(settings, name, "")