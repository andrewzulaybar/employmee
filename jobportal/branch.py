import sys
import os
from django.db import connection

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cpsc304.settings')


class Branch:
    def branch_info(self, username, form):
        var = ''
        if len(form.cleaned_data['data']) >= 2:
            var = ' , b.street_address, b.postal_zip, b.contact_email'
        elif len(form.cleaned_data['data']) == 0:
            var = ''
        elif form.cleaned_data['data'][0] == 'Address':
            var = ' , b.street_address, b.postal_zip'
        elif form.cleaned_data['data'][0] == 'Contact Email':
            var = ' , b.contact_email'
        with connection.cursor() as cursor:
            query = "SELECT b.branch_ID{0} \
                    from Branch b \
                    WHERE b.company_login_id ='{1}' AND b.branch_ID = '{2}';" .format(var, username, form.cleaned_data['id'])
            cursor.execute(query)
            info = cursor.fetchall()
            ids = [branch for branch in info]
            return ids

    def branch_id(self, username):
        with connection.cursor() as cursor:
            query = "SELECT b.branch_ID \
                    from Branch b \
                    WHERE b.company_login_id ='{0}';" .format(username)
            cursor.execute(query)
            info = cursor.fetchall()
            ids = [branch[0] for branch in info]
            return ids