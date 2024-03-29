import sys
import os
from django.db import connection
import json
import time

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
            print(query)
            print ("Record deleted successfully from saves_job table")
        except:
            print('problem deleting %s, %s from saves_job' % (username, job_id))


def job_type_change(old_job, merged_job):
    if merged_job['employment_type'] != old_job['employment_type']:
        return True
    if merged_job['title'] != old_job['title']:
        return True
    return False


def merge_jobs(old_job, new_job):
    #print(old_job['salary'])
    #print(new_job['salary'])
    merge = {}
    for key in old_job:
        if new_job[key] == '' or old_job[key] == new_job[key]:
            merge[key] = old_job[key]
        else:
            merge[key] = new_job[key]
    merge['salary'] = old_job['salary'] #no salary change possible at this time
    return merge



def update_job(username, job_id, old_job, new_job):
    with connection.cursor() as cursor:
        merged_job = merge_jobs(old_job, new_job)
        print(merged_job)
        execute_update = True
        if job_type_change(old_job, merged_job):
            print('need to update job_types')
            try:
                query1 = """INSERT INTO job_types(company_login_ID, title, employment_type, salary) VALUES ('%s', '%s', '%s', %s)""" \
                         % (merged_job['company_name'], merged_job['title'], merged_job['employment_type'], merged_job['salary'])
                print(query1)
                cursor.execute(query1)
                print('inserted new job_type')
            except Exception as error:
                #execute_update = False
                print("unable to insert a new job type")
                print(error)

        if execute_update:
            query2 = """UPDATE job set title='%s', sector='%s', min_education='%s', employment_type='%s' WHERE job_ID='%s'""" \
                     % (merged_job['title'], merged_job['sector'],
                        merged_job['min_education'], merged_job['employment_type'], merged_job['job_id'])
            print(query2)
            try:
                cursor.execute(query2)
                print('Job successfuly updated')
            except Exception as error:
                print('problem updating job')
                print(error)


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


def delete_job(username, job_id):
    with connection.cursor() as cursor:
        print(username)
        print(job_id)
        query = """delete from job where job_id=%s""" % (job_id)
        print(query)
        try:
            cursor.execute(query)
            print ("record successfully deleted")
        except:
            print('problem deleting %s from job' % (job_id))
    return None

def create_job(job_id, username, form):
    current_date = time.strftime('%Y-%m-%d')
    title = form.cleaned_data.get('title')
    emp_type = form.cleaned_data.get('employment_type')
    salary = form.cleaned_data.get('salary')
    sector = form.cleaned_data.get('sector')
    description = form.cleaned_data.get('description')
    min_education = form.cleaned_data.get('min_education')
    deadline = form.cleaned_data.get('deadline')
    print(title)
    queryType = """INSERT into Job_Types values('%s', '%s', '%s', %s);""" % (username, title, emp_type, salary)
    print(queryType)
    with connection.cursor() as cursor:
        try:
            cursor.execute(queryType)
            print('successfully created job type')
        except Exception as error:
            print('problem creating job type')
            print(error)

        queryJob = """INSERT into Job values('%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s');""" \
               % (job_id, title, sector, description, deadline, min_education, emp_type, username, current_date)
        print(queryJob)
        try:
            cursor.execute(queryJob)
            print('successfully created job')
        except Exception as error:
            print('problem creating job')
            print(error)
        queryJobLoc = """INSERT into Job_Location values(%s, 'M4B2K2');""" \
                   % (job_id)
        print(queryJobLoc)
        try:
            cursor.execute(queryJobLoc)
            print('successfully added job_location')
        except Exception as error:
            print('problem creating job_location')
            print(error)

    return None


def get_next_job_id():
    with connection.cursor() as cursor:
        query = """select max(job_id) + 1 from job;"""
        cursor.execute(query)
        result = cursor.fetchall()
    return result[0][0]
