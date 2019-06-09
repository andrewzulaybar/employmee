from django.shortcuts import render

CONTEXT = {
    'title': 'Home Page',
    'jobs': [{
        'job1': {
            'id': '1',
            'title': 'Software Developer Co-Op',
            'company': 'Amazon',
            'deadline': '5',
            'applications': '65',
            'salary': '30,000',
            'sector': 'Tech',
            'city': 'Seattle',
            'prov_state': 'WA',
            'type': 'Internship',
            'education': 'High school',
            'skills': ['java', 'c++'],
        },
        'job2': {
            'title': 'Data Analyst',
            'company': 'SAP'
        }
    }]
}


def home(request):
    return render(request, 'jobportal/home.html', CONTEXT)


def premium_home(request):
    return render(request, 'jobportal/home-prem.html', CONTEXT)


def company_home(request):
    return render(request, 'jobportal/home-comp.html', CONTEXT)


def details(request):
    return render(request, 'jobportal/details.html', CONTEXT)
