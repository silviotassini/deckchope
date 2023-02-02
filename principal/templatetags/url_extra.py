from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def url(view_name, *args, **kwargs):
    url = reverse(view_name, args=args, kwargs=kwargs)
    url = url.replace('dec/', 'deck/')
    return url
