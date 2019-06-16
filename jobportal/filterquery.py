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

        self.deadline = "deadline <= {}".format(date.today() + timedelta(days=deadline)) if deadline else ""
        self.recent_post = "date >= {}".format(date.today() - timedelta(days=recent_post)) if recent_post else ""

    def mysql_query(self, schema):
        with connection.cursor() as cursor:
            from_str = "Job"

            if self.skill_list and self.city_list:
                from_str += " INNER JOIN Job_Location ON Job.job_ID = Job_Location.job_ID INNER JOIN Location ON Job_Location.postal_zip = Location.postal_zip INNER JOIN Requires ON Job.job_ID = Requires.job_ID"
            elif self.skill_list:
                from_str += " INNER JOIN Requires ON Job.job_ID = Requires.job_ID"
            elif self.city_list:
                from_str += " INNER JOIN Job_Location ON Job.job_ID = Job_Location.job_ID INNER JOIN Location ON Job_Location.postal_zip = Location.postal_zip"

            sql = "SELECT * FROM %s %s;" % (from_str, self.build_where_content())

            sql.replace("'", "\\'")
            cursor.execute(sql)

            jobs = cursor.fetchall()

            list_jobs = []

            for info in jobs:
                job = {}
                for key, value in zip(schema, info):
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


# if __name__ == '__main__':
#     # sector_list, edu_list, type_list, skill_list, city_list, deadline, recent_post, sort_by
#
#     myQuery1 = JobQuery(["Technology", "Medical"], [], [], [], [], '', '', 'deadline')
#     example1 = myQuery1.mysql_query()
#
#     myQuery2 = JobQuery([], ['Bachelors', 'Masters'], [], [], [], '', '', 'company_login_id')
#     example2 = myQuery2.mysql_query()
#
#     myQuery3 = JobQuery([], ['Bachelors', 'Masters'], [], [], ['Vancouver', 'New York'], '', '', 'company_login_id')
#     example3 = myQuery3.mysql_query()
#
#     myQuery4 = JobQuery([], ['Bachelors', 'Masters'], [], ['C++'], ['New York'], '', '', '')
#     example4 = myQuery4.mysql_query()
#
#     print(example1)
#     print()
#     print()
#     print(example2)
#     print()
#     print()
#     print(example3)
#     print()
#     print()
#     print(example4)


