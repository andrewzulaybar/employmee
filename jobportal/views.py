from django.shortcuts import render

from jobportal.sidebar import Sidebar


def get_context():
    sidebar = Sidebar()
    context = {
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
                'description': """We are looking for Amazon interns to join us for Fall 2019! Amazon interns have the
                                opportunity to work alongside the industry’s brightest engineers who innovate everyday on
                                behalf of our customers. Our interns and co-ops write real software and partner with a
                                select group of experienced software development engineers, who both help and challenge
                                them as they work on projects that matter..."""
            },
            'job2': {
                'title': 'Data Analyst',
                'company': 'SAP'
            }
        }],
        'sectors': sidebar.sectors(),
        'skills': sidebar.skills(),
        'cities': sidebar.cities(),
        'education': sidebar.education(),
        'types': sidebar.job_types()
    }
    return context


def home(request):
    return render(request, 'jobportal/home/home.html', get_context())


def premium_home(request):
    return render(request, 'jobportal/home/home-prem.html', get_context())


def company_home(request):
    return render(request, 'jobportal/home/home-comp.html', get_context())


def details(request):
    return render(request, 'jobportal/details/details.html', get_context())


def premium_details(request):
    return render(request, 'jobportal/details/details-prem.html', get_context())


def company_details(request):
    return render(request, 'jobportal/details/details-comp.html', get_context())


def settings(request):
    return render(request, 'jobportal/settings/settings.html', get_context())

def settings_prem(request):
    return render(request, 'jobportal/settings/settings-prem.html', get_context())

def settings_comp(request):
    return render(request, 'jobportal/settings/settings-comp.html', get_context())

def create_posting(request):
    return render(request, 'jobportal/create-posting.html', get_context())

def saved_jobs(request):
    return render(request, 'jobportal/saved-jobs.html', get_context())

def login(request):
    return render(request, 'jobportal/login.html', get_context())