import os
import sys


def generate(file_name):
    f = open_file(file_name)
    try:
        model_class = getattr(sys.modules['itis_manage.models'], file_name)
    except:
        model_class = getattr(sys.modules['itis_data_niffler.models'], file_name)
    for line in f.readlines():
        try:
            model_class.objects.create(**{'name': line[:len(line) - 1]})
        except:
            pass


def open_file(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name), mode='r')
