import datetime


BACHELOR_YEARS = 4
MASTER_YEARS = 2

MARK_THRESHOLDS = (0, 0, 0,
                   56,
                   71,
                   86
                   )


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


def avg(l):
    """
    Calculates arithmetic average of a collection

    :param l: collection
    :return:
    :rtype float
    """
    return (sum(l) + 0.) / len(l)
