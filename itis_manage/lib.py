from django.contrib.auth.models import User

from itis_manage.models import Student


def get_unique_object_or_none(model=User, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except:
        return None
