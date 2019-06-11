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
