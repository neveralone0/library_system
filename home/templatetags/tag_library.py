# templatetags/tag_library.py

from django import template

register = template.Library()


@register.filter()
def to_int(value):
    print('=====================')
    print(value)
    return int(value)
