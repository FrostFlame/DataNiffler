from django import template

from itis_manage.lib import get_unique_object_or_none
from itis_manage.models import Student

register = template.Library()


@register.simple_tag
def return_user(arg, field):
    return get_unique_object_or_none(Student, **{'pk': arg}).field
