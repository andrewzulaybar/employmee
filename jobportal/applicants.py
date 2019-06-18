import sys
import os
from django.db import connection

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cpsc304.settings')


class Applicants:
    def get_distinct_applicants(self, username):
        with connection.cursor() as cursor:
            query = "SELECT COUNT(DISTINCT r.applicant_login_ID) \
                     FROM Job j, Sends_Application s, Creates_resume r \
                     WHERE j.company_login_ID = '%s' AND s.resume_ID = r.resume_ID AND j.job_ID = s.job_ID;" % username
            cursor.execute(query)
            count = cursor.fetchall()[0][0]
            return count
