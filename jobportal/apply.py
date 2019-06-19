import sys
import os
from django.db import connection

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cpsc304.settings')


def apply_to_job(resume_id, job_id):
    with connection.cursor() as cursor:
        query = "INSERT INTO Sends_Application(application_number, date, status, cover_letter, resume_ID, job_ID) \
                SELECT max(application_number) + 1, NULL, NULL, NULL, %s, %s \
                FROM Sends_Application;" % (resume_id, job_id)

        print(query)
        cursor.execute(query)


# if __name__ == '__main__':
#     apply_to_job(6, 5)
