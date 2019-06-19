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
            return self.execute_and_format(cursor, query, schema)

    def get_additional_info(self,  schema, sort_by):
        with connection.cursor() as cursor:
            query = "SELECT j.job_ID, j.title, c.name, j.sector, l.city, \
                            l.state_prov, j.deadline, j.description, a.app_no, s.salary \
                     FROM Job j \
                     INNER JOIN Job_Location jl \
                         ON j.job_ID = jl.job_ID \
                     INNER JOIN Location l \
                         ON jl.postal_zip = l.postal_zip \
                     INNER JOIN Company c \
                         ON j.company_login_ID = c.company_login_ID \
                     INNER JOIN Job_Types jt \
                         ON j.company_login_id = jt.company_login_id \
                         AND j.title = jt.title \
                         AND j.employment_type = jt.employment_type \
                    LEFT OUTER JOIN applications a \
                        on j.job_ID = a.id \
                    INNER JOIN salary s \
                    on j.job_ID = s.id \
                     ORDER BY %s" % sort_by
            return self.execute_and_format(cursor, query, schema)

    def get_saved_jobs(self, schema, sort_by, username):
        print('in get_saved_jobs')
        with connection.cursor() as cursor:
            query = "SELECT j.job_ID, j.title, c.name, j.sector, l.city, l.state_prov, j.deadline, j.description  \
                     FROM Job j \
                     INNER JOIN Saves_Job sj \
                         ON j.job_ID = sj.job_ID \
                     INNER JOIN Job_Location jl \
                         ON j.job_ID = jl.job_ID \
                     INNER JOIN Location l \
                         ON jl.postal_zip = l.postal_zip \
                     INNER JOIN Company c \
                         ON j.company_login_ID = c.company_login_ID \
                     WHERE sj.premium_login_id = '%s' \
                     ORDER BY %s;" % (username, sort_by)
            return self.execute_and_format(cursor, query, schema)

    def execute_and_format(self, cursor, query, schema):
        cursor.execute(query)
        jobs = cursor.fetchall()

        list_jobs = []

        for info in jobs:
            job = {}
            for key, value in zip(schema, info):
                job[key] = value
            list_jobs.append(job)

        return list_jobs


class CompanySidebar:
    def get_applicants(self, schema, job_id, company_username):
        username_str = "'{}'".format(company_username)

        with connection.cursor() as cursor:
            query = "SELECT DISTINCT a.first_name, a.last_name, a.contact_email\
                    FROM Sends_Application s \
                    INNER JOIN Creates_Resume c \
                        ON s.resume_ID = c.resume_ID \
                    INNER JOIN Applicant a \
                        ON c.applicant_login_ID = a.applicant_login_ID \
                    INNER JOIN Job j\
                        ON s.job_ID = j.job_ID \
                    WHERE s.job_ID = %s AND j.company_login_ID = %s;" % (job_id, username_str)

            query.replace("'", "\\'")
            cursor.execute(query)
            applicants = cursor.fetchall()

            lst_applicants = []

            for a in applicants:
                applicant = {}
                for key, value in zip(schema, a):
                    applicant[key] = value
                lst_applicants.append(applicant)

            return lst_applicants