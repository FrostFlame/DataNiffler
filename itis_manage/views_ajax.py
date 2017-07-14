from dal import autocomplete
from django.db.models import Q

from itis_manage.models import Person
from itis_manage.views import CustomLoginRequiredMixin


class CuratorAutocompleteView(autocomplete.Select2QuerySetView, CustomLoginRequiredMixin):
    queryset = Person.objects.all()

    def get_queryset(self):
        qs = Person.objects.all()
        if self.q:
            words = self.q.split(' ')
            for word in words:
                qs = qs.filter(
                    Q(name__icontains=word) | Q(surname__icontains=word) | Q(third_name__icontains=word))
        return qs
