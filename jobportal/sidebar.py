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

    def sectors(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT sector FROM Job ORDER BY sector")

            records = cursor.fetchall()

            sectors = [sector[0] for sector in records]
            return sectors

    def education(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT min_education FROM Job ORDER BY min_education")

            records = cursor.fetchall()

            educations = [education[0] for education in records]
            return educations

    def skills(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM Skill ORDER BY name")

            records = cursor.fetchall()

            skills = [skill[0] for skill in records]
            return skills

    def job_types(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT employment_type FROM Job ORDER BY employment_type")

            records = cursor.fetchall()

            job_types = [job_type[0] for job_type in records]
            return job_types


class SortBy:
    def get_jobs(self, schema, sort_by):
        with connection.cursor() as cursor:
            query = "SELECT j.job_ID, j.title, c.name, j.sector, l.city, l.state_prov, j.deadline, j.description  \
                     FROM Job j \
                     INNER JOIN Job_Location jl \
                         ON j.job_ID = jl.job_ID \
                     INNER JOIN Location l \
                         ON jl.postal_zip = l.postal_zip \
                     INNER JOIN Company c \
                         ON j.company_login_ID = c.company_login_ID \
                     ORDER BY %s;" % sort_by
            cursor.execute(query)
            jobs = cursor.fetchall()

            list_jobs = []

            for info in jobs:
                job = {}
                for key, value in zip(schema, info):
                    job[key] = value
                list_jobs.append(job)

            return list_jobs
