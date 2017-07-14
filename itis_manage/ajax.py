from dal import autocomplete
from django.db.models import Q

from itis_manage.models import City, Country
from itis_manage.views import CustomLoginRequiredMixin


class GetCities(autocomplete.Select2QuerySetView, CustomLoginRequiredMixin):
    queryset = City.objects.all()

    def get_queryset(self):
        return self.queryset.filter(
            Q(name__icontains=self.q) | Q(country__name__icontains=self.q)) if self.q else self.queryset
