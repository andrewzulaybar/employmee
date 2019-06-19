import sys
import os
from django.db import connection
from django.db import IntegrityError

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cpsc304.settings')


def apply_to_job(resume_id, job_id):
    with connection.cursor() as cursor:
        query = "INSERT INTO Sends_Application(application_number, date, status, cover_letter, resume_ID, job_ID) \
                (SELECT max(application_number) + 1, NULL, NULL, NULL, %s, %s \
                FROM Sends_Application);" % (resume_id, job_id)

        try:
            cursor.execute(query)
        except IntegrityError:
            raise Exception


