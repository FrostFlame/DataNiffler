from django import forms

from itis_manage.models import Subject


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

    criterion = forms.ChoiceField(choices=CRITERIA_CHOICES)


class TeacherStatsCriteriaForm(forms.Form):
    AVG_SCORE, NUM_DOPKAS, NUM_COMMS, NUM_SUBJECTS, NUM_HOURS, EXP, AGE = range(7)
    CRITERIA_CHOICES = (
        (AVG_SCORE, 'Средний балл'),
        (NUM_DOPKAS, 'Число доп.сессий'),
        (NUM_COMMS, 'Число комиссий'),
        (NUM_SUBJECTS, 'Число предметов'),
        (NUM_HOURS, 'Количество часов'),
        (EXP, 'Стаж'),
        (AGE, 'Возраст')
    )

    subject = forms.ModelChoiceField(Subject.objects.all(), required=False)

    criterion = forms.ChoiceField(choices=CRITERIA_CHOICES)