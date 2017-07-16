import datetime


def today():
    """
    Returns today's date
    :return: datetime.date.today()
    """
    return datetime.date.today()


def age(born):
    """
    Calculates age in years of object created at specified date
    :param born: date of object creation (i.e. person birth date)
    :type born datetime.date
    :return: age in years
    :rtype: int
    """
    return today().year - born.year - ((today().month, today().day) < (born.month, born.day))