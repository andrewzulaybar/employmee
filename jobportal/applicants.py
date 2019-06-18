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

    def get_top_fans(self, username):
        with connection.cursor() as cursor:
            query = "SELECT a.first_name, a.last_name, a.contact_email \
                        FROM applicant a \
                        WHERE NOT EXISTS \
                            (SELECT * from job j \
                            WHERE j.company_login_ID='%s' AND NOT EXISTS \
                            (SELECT s.resume_ID \
                            FROM sends_application s, creates_resume r \
                            WHERE r.resume_ID=s.resume_ID AND s.job_ID=j.job_ID AND \
                                    a.applicant_login_ID=r.applicant_login_ID));" % username
            cursor.execute(query)
            info = cursor.fetchall()
            applicants = [app for app in info]
            return applicants
