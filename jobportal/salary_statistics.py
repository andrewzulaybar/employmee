import sys
import os
from django.db import connection

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cpsc304.settings')

class SalaryStatistics:
    def get_salary_statistics(self):
        with connection.cursor() as cursor:
            query = "SELECT j.sector, min(salary), avg(salary), max(salary) \
                     FROM job j INNER JOIN job_types jt \
                     ON j.company_login_ID = jt.company_login_ID AND j.title = jt.title \
                     AND j.employment_type = jt.employment_type \
                     GROUP BY j.sector;"
            cursor.execute(query)
            stats = cursor.fetchall()

            statistics = [stat for stat in stats]
            print(statistics)
            return statistics
