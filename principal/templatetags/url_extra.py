from django import template
from django.urls import reverse
from datetime import timedelta

register = template.Library()


@register.simple_tag
def url(view_name, *args, **kwargs):
    url = reverse(view_name, args=args, kwargs=kwargs)
    url = url.replace('dec/', 'deck/')
    return url


@register.filter
def add_days(value, arg):
    """
    Adds the number of days specified in arg to the given date value.
    """
    return value + timedelta(days=int(arg))
