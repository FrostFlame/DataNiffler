from dal import autocomplete
from django.db.models import Q
from django.http import JsonResponse

from itis_manage.lib import get_list_aj, get_set_sem
from itis_manage.models import City, Status, Person, Subject, SemesterSubject
from itis_manage.views import CustomLoginRequiredMixin


class GetObjects(autocomplete.Select2QuerySetView, CustomLoginRequiredMixin):
    pass


class CuratorAutocompleteView(autocomplete.Select2QuerySetView, CustomLoginRequiredMixin):
    queryset = Person.objects.filter(status__name="Куратор")


def get_subjects(request):
    course = request.GET.get('course_id', None)
    if course:
        courses = get_list_aj(course)
        semesters = get_set_sem(courses)
        subjects = SemesterSubject.objects.filter(semester__number__in=semesters).values('subject__id', 'subject__name')
        return JsonResponse(list(subjects), safe=False)
