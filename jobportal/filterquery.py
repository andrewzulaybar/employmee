import sys
import os
from django.db import connection
from datetime import date, timedelta

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cpsc304.settings')


class JobQuery:
    def __init__(self, sector_list, edu_list, type_list, skill_list, city_list, deadline, recent_post):
        self.sector_list = ["sector = '{}'".format(x) for x in sector_list]
        self.edu_list = ["min_education = '{}'".format(x) for x in edu_list]
        self.type_list = ["employment_type = '{}'".format(x) for x in type_list]

        self.skill_list = ["skill_name = '{}'".format(x) for x in skill_list]
        self.city_list = ["city = '{}'".format(x) for x in city_list]

        self.deadline = "deadline <= '{}'".format(date.today() + timedelta(days=deadline)) if deadline else ""
        self.recent_post = "date >= '{}'".format(date.today() - timedelta(days=recent_post)) if recent_post else ""

    def get_jobs(self, schema):
        with connection.cursor() as cursor:
            select_str = "j.job_ID, j.title, c.name, j.sector, l.city, l.state_prov, j.deadline, j.description, a.app_no, s.salary"
            from_str = """Job j INNER JOIN Company c ON j.company_login_ID = c.company_login_ID
                        INNER JOIN Job_Location jl ON j.job_ID = jl.job_ID 
                        INNER JOIN Location l ON jl.postal_zip = l.postal_zip
                        LEFT OUTER JOIN applications a ON j.job_ID = a.id
                        INNER JOIN salary s ON j.job_ID = s.id"""

            if self.skill_list:
                from_str += " INNER JOIN Requires r ON j.job_ID = r.job_ID"

            sql = "SELECT %s FROM %s %s;" % (select_str, from_str, self.build_where_content())

            # print(sql)

            sql.replace("'", "\\'")
            cursor.execute(sql)
            jobs = cursor.fetchall()

            list_jobs = []

            for j in jobs:
                job = {}
                for key, value in zip(schema, j):
                    job[key] = value
                list_jobs.append(job)

            return list_jobs

    def build_where_content(self):
        non_empty_attrs = filter(lambda x: bool(x),
                                 [self.sector_list, self.edu_list, self.type_list, self.skill_list,
                                  self.city_list, self.deadline, self.recent_post])
        processed_lst = []

        for attr in non_empty_attrs:
            if isinstance(attr, list):
                if len(attr) > 1:
                    processed_lst.append("(" + " OR ".join(attr) + ")")
                else:
                    processed_lst.append(attr[0])
            else:
                processed_lst.append(attr)

        if not processed_lst:
            return ""
        else:
            return "WHERE " + " AND ".join(processed_lst)


