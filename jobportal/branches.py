import sys
import os
from django.db import connection

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cpsc304.settings')


class Branches:
    def getBranchesProjection(self, address=True, email=True):
        projection = 'b.company_login_id b.contact_email, b.street_address, b.postal_zip, l.city, l.state_prov, l.country'
        username = 'google' #need to get this from self
        with connection.cursor() as cursor:
            query = "SELECT %s FROM branch b \
                            INNER JOIN Location l \
                                ON b.postal_zip = l.postal_zip \
                            WHERE b.company_login_id = '%s';" % (projection, username)
            cursor.execute(query)
            branches = cursor.fetchall()
            print(branches)
            return branches