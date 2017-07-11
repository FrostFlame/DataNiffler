from django.http import HttpResponse

from trash.generate_cities import generate


def get_parser_value(parser, type, subtype):
    return parser.get(type, subtype)


def get_database(config_parser, debug):
    if debug:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': config_parser.get('TEST_DATABASE', 'NAME'),
                'USER': config_parser.get('TEST_DATABASE', 'USER'),
                'PASSWORD': config_parser.get('TEST_DATABASE', 'PASSWORD'),
                'HOST': config_parser.get('TEST_DATABASE', 'HOST'),
                'PORT': config_parser.get('TEST_DATABASE', 'PORT'),
            }
        }
        print('\nUsing test database')
    else:
        DATABASES = {
            'default': {
                'ENGINE': config_parser.get('DATABASE', 'ENGINE'),
                'NAME': config_parser.get('DATABASE', 'NAME'),
                'USER': config_parser.get('DATABASE', 'USER'),
                'PASSWORD': config_parser.get('DATABASE', 'PASSWORD'),
                'HOST': '',
                'PORT': '',
                'OPTIONS': dict(config_parser.items('DATABASE_OPTIONS')) or {}
            }
        }
    return DATABASES


TABLES = {
    1: 'City',
}


def update(request, table_id='info'):
    if table_id == 'info':
        return HttpResponse(str(TABLES))
    else:
        if int(table_id) in TABLES:
            generate(TABLES[int(table_id)])
            return HttpResponse(TABLES[int(table_id)] + ' successfully updated!')
