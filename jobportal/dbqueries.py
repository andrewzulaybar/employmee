import sys
sys.path.append('..')

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cpsc304.settings')

from django.db import connection


class JobQuery:
    def __init__(self, sector):
        self.sector = sector


    def my_custom_sql2(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM Job WHERE sector = %s;", [self.sector])

            records = cursor.fetchall()

        print('my_custom_sql2:')
        print(records)



def my_custom_sql1(sector):
    with connection.cursor() as mysql_cursor:
        mysql_cursor.callproc("getJobPostingsFromSector", [sector])
        results = mysql_cursor.fetchall()

    print('my_custom_sql1:\n')
    print(results)


if __name__ == '__main__':
    sector_input = 'Technology'
    my_custom_sql1(sector_input)
    myQuery = JobQuery('Technology')
    myQuery.my_custom_sql2()
