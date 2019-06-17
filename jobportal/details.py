import sys
import os
from django.db import connection

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cpsc304.settings')


def get_job(schema, job_id, username, user_type):
    with connection.cursor() as cursor:
        query = """SELECT j.job_ID, j.title, c.name, j.sector, j.min_education, j.employment_type, \
                        l.city, l.state_prov, j.deadline, j.description
                 FROM Job j 
                 INNER JOIN Job_Location jl 
                     ON j.job_ID = jl.job_ID 
                 INNER JOIN Location l 
                     ON jl.postal_zip = l.postal_zip 
                 INNER JOIN Company c 
                     ON j.company_login_ID = c.company_login_ID 
                 WHERE j.job_ID = %s""" % job_id
        cursor.execute(query)
        jobs = cursor.fetchall()

        job = {}

        for key, value in zip(schema, jobs[0]):
            job[key] = value

        get_skills(job_id, job)
        job['username'] = username
        job['user_type'] = user_type

        return job


def get_skills(job_id, job):
    with connection.cursor() as cursor:
        query = """SELECT s.name 
                 FROM Skill s 
                 INNER JOIN Requires r 
                     ON r.skill_name = s.name
                 INNER JOIN Job j
                     ON j.job_ID = r.job_ID
                 WHERE j.job_ID = %s""" % job_id
        cursor.execute(query)
        skills = cursor.fetchall()

        skill_list = [skill[0] for skill in skills]

        job['skills'] = skill_list
        return job
