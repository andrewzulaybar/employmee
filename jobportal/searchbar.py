import sys
import os
from django.db import connection
from datetime import date, timedelta

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cpsc304.settings')


class SearchBar:
    def __init__(self, search_bar_input):
        self.input = search_bar_input

    def search(self):
        with connection.cursor() as cursor:
            sql = "WITH t as (SELECT * FROM Job WHERE title LIKE '%%%s%%') SELECT * FROM t UNION ALL SELECT job_id, title, sector, description, deadline, min_education, employment_type, j.company_login_id, date FROM Job j INNER JOIN Company ON j.company_login_id = Company.company_login_id WHERE name LIKE '%%%s%%' AND NOT EXISTS(SELECT * FROM t);" % (self.input, self.input)

            print(sql)

            sql.replace("'", "\\'")
            cursor.execute(sql)

            records = cursor.fetchall()
            return records


if __name__ == '__main__':
    example1 = SearchBar.search(SearchBar('amazon'))
    print(example1)
    print()
    print()
    example2 = SearchBar.search(SearchBar('Data Scientist'))
    print(example2)