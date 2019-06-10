import sys
sys.path.append('..')

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cpsc304.settings')

from django.db import connection


# "SELECT * FROM Job WHERE sector = %s;", [self.sector])

# job -> sector, deadline, education, type,
# requires -> skill todo
# job_location -> zip todo
# Location -> city, postalzip (join with job_location) todo
class JobQuery:
    def __init__(self, sector_list, edu_list, type_list, skill_list, city_list, deadline, recent_post):
        self.sector_list = ["sector='{}'".format(x) for x in sector_list]
        self.edu_list = ["min_education = {}".format(x) for x in edu_list]
        self.type_list = ["employment_type = {}".format(x) for x in type_list]

        self.skill_list = skill_list
        self.city_list = city_list
        self.deadline = "deadline = {}".format(deadline) if deadline else ""
        self.recent_post = "date = {}".format(recent_post) if recent_post else ""

    def mysql_query(self):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Job %s" % self.build_where_content()
            sql.replace("'", "\\'")
            cursor.execute(sql)

            records = cursor.fetchall()
            return records

    def build_where_content(self):
        non_empty_lists = filter(None, [self.sector_list, self.edu_list,
                                        self.type_list, self.deadline, self.recent_post])
        processed_list = []

        for list in non_empty_lists:
            if len(list) > 1:
                processed_list.append("(" + " OR ".join(list) + ")")
            else:
                processed_list.append(list[0])

        where_filters = "WHERE " + " AND ".join(processed_list) + ";"

        if not where_filters:
            return ""
        else:
            return where_filters


if __name__ == '__main__':
    myQuery = JobQuery(["Technology", "Medical"], [], [], [], [], '', '')
    example = myQuery.mysql_query()
    print(example)

