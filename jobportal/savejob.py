import sys
import os
from django.db import connection

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cpsc304.settings')

def save_prem_job(username, job_id):
    with connection.cursor() as cursor:
        query = """INSERT INTO saves_job(premium_login_ID, job_ID) VALUES ('%s', %s)""" % (username, job_id)
        print(query)
        result = cursor.execute(query)
        print(result)
        print ("Record inserted successfully into python_users table")