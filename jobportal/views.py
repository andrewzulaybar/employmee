from django.shortcuts import render


def home(request):
    context = {
        'title': 'Home Page',
        'jobs': [{
            'job1': {
                'title': 'Software Developer Co-Op',
                'company': 'Amazon',
                'deadline': '5',
                'applications': '65',
                'salary': '30,000',
                'sector': 'Tech',
                'city': 'Seattle',
                'prov_state': 'WA'
            },
            'job2': {
                'title': 'Data Analyst',
                'company': 'SAP'
            }
        }],
        'job_list': ['Amazon', 'Apple', 'Google']
    }
    return render(request, 'jobportal/base.html', context)
