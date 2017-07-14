from dal import autocomplete
from django.db.models import Q

from itis_manage.models import City, Status, Person
from itis_manage.views import CustomLoginRequiredMixin


class GetObjects(autocomplete.Select2QuerySetView, CustomLoginRequiredMixin):
    pass



class CuratorAutocompleteView(autocomplete.Select2QuerySetView, CustomLoginRequiredMixin):
    queryset = Person.objects.filter(status__name="Куратор")


