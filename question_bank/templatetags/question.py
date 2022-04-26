from django import template
from django.urls import reverse
from django.http import QueryDict
from utils import urls

register = template.Library()


@register.filter
def cut(value, arg):
    if arg.lower() != 'p':
        return value.replace(arg, '')
    for i in ('<p>', '</p>', '_x000D_'):
        value = value.replace(i, '')
    return value


@register.simple_tag
def memory_url(request, name, *args, **kwargs):
    """
    生成带有原搜索条件的URL（替代了模板中的url）
    :param request:
    :param name:
    :return:
    """
    return urls.memory_url(request, name, *args, **kwargs)
