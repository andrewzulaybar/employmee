from django.shortcuts import render

from jobportal.sidebar import Sidebar, SortBy


def get_context():
    sidebar = Sidebar()
    sort_by = SortBy()
    schema = ['title', 'company_name', 'sector', 'city', 'state_prov', 'deadline', 'description']
    context = {
        'title': 'Home Page',
        'jobs': sort_by.get_jobs(schema),
        'sectors': sidebar.sectors(),
        'skills': sidebar.skills(),
        'cities': sidebar.cities(),
        'education': sidebar.education(),
        'types': sidebar.job_types()
    }
    return context


def home(request):
    return render(request, 'jobportal/home.html', get_context())


def premium_home(request):
    return render(request, 'jobportal/home-prem.html', get_context())


def company_home(request):
    return render(request, 'jobportal/home-comp.html', get_context())


def details(request):
    return render(request, 'jobportal/details.html', get_context())
