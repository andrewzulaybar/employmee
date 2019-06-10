import sys
import os
from django.db import connection
from datetime import date, timedelta

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cpsc304.settings')


# job -> sector, deadline, education, type,
# requires -> skill todo
# job_location -> zip todo
# Location -> city, postalzip (join with job_location) todo
class JobQuery:
    def __init__(self, sector_list, edu_list, type_list, skill_list, city_list, deadline, recent_post, sort_by):
        self.sector_list = ["sector='{}'".format(x) for x in sector_list]
        self.edu_list = ["min_education = '{}'".format(x) for x in edu_list]
        self.type_list = ["employment_type = '{}'".format(x) for x in type_list]

        self.skill_list = skill_list
        self.city_list = city_list

        #todo
        self.deadline = "deadline = {}".format(date.today() + timedelta(days=deadline)) if deadline else ""
        self.recent_post = "date = {}".format(date.today() + timedelta(days=recent_post)) if recent_post else ""

        self.sort_by = sort_by

    def mysql_query(self):
        with connection.cursor() as cursor:

            if not self.sort_by:
                sql = "SELECT * FROM Job %s;" % self.build_where_content()
            else:
                sql = "SELECT * FROM Job %s ORDER BY %s;" % (self.build_where_content(), self.sort_by)

            sql.replace("'", "\\'")
            cursor.execute(sql)

            records = cursor.fetchall()
            return records

    def build_where_content(self):
        non_empty_lists = filter(None, [self.sector_list, self.edu_list,
                                        self.type_list, self.deadline, self.recent_post])
        processed_list = []

        for lst in non_empty_lists:
            if len(lst) > 1:
                processed_list.append("(" + " OR ".join(lst) + ")")
            else:
                processed_list.append(lst[0])

        where_filters = "WHERE " + " AND ".join(processed_list)

        if not where_filters:
            return ""
        else:
            return where_filters


if __name__ == '__main__':
    myQuery = JobQuery(["Technology", "Medical"], [], [], [], [], '', '', 'deadline')
    example = myQuery.mysql_query()

    myQuery2 = JobQuery([], ['Bachelors', 'Masters'], [], [], [], '', '', 'company_login_id')
    example2 = myQuery2.mysql_query()

    print('This is Query1')
    print(example)
    print()
    print()
    print('This is Query2')
    print(example2)

