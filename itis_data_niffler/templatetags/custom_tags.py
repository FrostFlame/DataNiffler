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
    try:
        return dict[subject_id]
    except:
        return 'None'


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='getattr')
def get_attr(obj, key):
    return getattr(obj, key, None)


@register.filter(name='getattr2')
def get_attr_nested(obj, key):
    """
    Retrieves object attribute, supports dot separated nested paths
    All the callables are called without parameters (just like in Django templates)

    :param obj: object to get attribute from
    :param key: attribute or callable, or path
        (i.e. get_attr_nested(obj, 'foo.bar') will return either
        obj.foo.bar, or obj.foo.bar(), or obj.foo().bar(), or obj.foo().bar)
    :return: value of specified attribute or callable
    """
    if not key:
        return obj
    path = key.split('.')
    attr = getattr(obj, path[0], {})
    if callable(attr):
        attr = attr()
    return get_attr_nested(attr, '.'.join(path[1:]))
