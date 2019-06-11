import sys
import os
from django.db import connection

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cpsc304.settings')


class Sidebar:
    def cities(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT city FROM Location ORDER BY city;")

            records = cursor.fetchall()

            cities = [city[0] for city in records]
            return cities
