import sys
from django import template

from itis_manage.lib import get_unique_object_or_none
from itis_manage.models import Student

register = template.Library()


@register.simple_tag
def return_model_object_field(model, id, field):
    return getattr(get_unique_object_or_none(getattr(sys.modules['itis_manage.models'], model), **{'pk': id}), field)


@register.simple_tag
def progress_id_subject_id(dict, subject_id):
    return dict[subject_id]

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

