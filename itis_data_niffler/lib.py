from datetime import datetime


def semesters(x):
    return {
        '1': [1, 2],
        '2': [3, 4],
        '3': [5, 6],
        '4': [7, 8]
    }.get(x)


MONTH_OF_GROUPS_FOUNDATION = 9


def diff_month(d1, d2):
    return (int(d1.year) - d2) * 12 + int(d1.month) - MONTH_OF_GROUPS_FOUNDATION
