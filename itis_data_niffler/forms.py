from django import forms


class StudentStatsCriteriaForm(forms.Form):
    EVENTS, BALLS, DOPKAS, COMMISSIONS, ABSENCES, FIVES = range(6)
    CRITERIA_CHOICES = (
        (EVENTS, 'Мероприятия'),
        (BALLS, 'Доп. баллы'),
        (DOPKAS, 'Допки'),
        (COMMISSIONS, 'Комиссии'),
        (ABSENCES, 'Пропуски'),
        (FIVES, 'Пятерки')
    )

    course = forms.ChoiceField(choices=zip(range(1, 6), range(1, 6)))
    course_semester = forms.ChoiceField(choices=((1, 1), (2, 2)))

    year_start = forms.IntegerField()
    year_end = forms.IntegerField()

    criterion = forms.Select(choices=CRITERIA_CHOICES)

    # TODO columns

