import sys
import os
from django.db import connection
import json

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cpsc304.settings')

def save_prem_job(username, job_id):
    with connection.cursor() as cursor:
        query = """INSERT INTO saves_job(premium_login_ID, job_ID) VALUES ('%s', %s)""" % (username, job_id)
        print(query)
        try:
            cursor.execute(query)
            print ("Record inserted successfully into saves_job table")
        except:
            print('problem inserting %s, %s from saves_job' % (username, job_id))



def un_save_prem_job(username, job_id):
    with connection.cursor() as cursor:
        query = """DELETE FROM saves_job WHERE premium_login_id='%s' AND job_id='%s'""" % (username, job_id)
        try:
            cursor.execute(query)
            print ("Record deleted successfully from saves_job table")
        except:
            print('problem deleting %s, %s from saves_job' % (username, job_id))


def job_type_change(old_job, new_job):
    if new_job['employment_type'] is not old_job['employment_type'] or new_job['employment_type'] is not None:
        return True
    if new_job['title'] is not old_job['title'] or new_job['title'] is not None:
        return True
    if new_job['salary'] is not old_job['salary'] or new_job['salary'] is not None:
       return True
    return False


def merge_jobs(old_job, new_job):
    merge = {}
    for key in old_job:
        if old_job[key] != new_job[key]:
            merge[key] = new_job[key]
        else:
            merge[key] = old_job[key]
    return merge



def update_job(username, job_id, old_job, new_job):
    with connection.cursor() as cursor:
        merged_job = merge_jobs(old_job, new_job)
        print('in update_job')
        print('old job:')
        print(old_job)
        print('new job:')
        print(new_job)
        print('merged')
        print(merged_job)

        if job_type_change(old_job, new_job):
            print('need to update job_types')
            #stubb
            try:
                query1 = """INSERT INTO job_types(company_login_ID, title, employment_type, salary) VALUES ('%s', '%s', '%s', '%s')""" % ()
                # cursor.execute(query1)
                print(query1)
            except:
                print('unable to insert new job_type')

        query2 = """UPDATE table job set description='%s' WHERE job_ID='%s'""" % (new_job['description'], job_id)
        print(query2)
        try:
            #cursor.execute(query)
            print('Job successfuly updated')
        except:
            print('problem updating job')


def getNewJob(job_id, username, request):
    newJob = {'job_id': job_id,
              'title': request.GET.get('new_title'),
              'company_name': username,
              'sector': request.GET.get('new_sector'),
              'min_education': request.GET.get('new_education'),
              'employment_type': request.GET.get('new_type'),
              'salary': request.GET.get('new_salary'),
              'description': request.GET.get('new_description'),
              }
    return newJob


def getOldJob(job_id, username, request):
    old_job = {'job_id': job_id,
              'title': request.GET.get('old_title'),
              'company_name': username,
              'sector': request.GET.get('old_sector'),
              'min_education': request.GET.get('old_education'),
              'employment_type': request.GET.get('old_type'),
              'salary': request.GET.get('old_salary'),
              'description': request.GET.get('old_description'),
              }
    return old_job