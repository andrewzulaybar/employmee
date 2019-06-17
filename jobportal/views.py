from django.shortcuts import render
from django.views.generic import ListView, DetailView

from jobportal import details
from jobportal.forms import SortByForm, FilterByForm
from jobportal.sidebar import Sidebar, SortBy
from jobportal.filterquery import JobQuery

DEFAULT = 'date DESC'


def get_context(sort_order):
    sidebar = Sidebar()
    sort_by = SortBy()
    schema = ['job_id', 'title', 'company_name', 'sector', 'city', 'state_prov', 'deadline', 'description']
    context = {
        'title': 'Home Page',
        'jobs': sort_by.get_jobs(schema, sort_order),
        'sectors': sidebar.sectors(),
        'skills': sidebar.skills(),
        'cities': sidebar.cities(),
        'education': sidebar.education(),
        'types': sidebar.job_types()
    }
    return context


def get_filter_context(filter_form):
    sidebar = Sidebar()
    filter_by = JobQuery(
        filter_form.cleaned_data['sector_choices'],
        filter_form.cleaned_data['edu_choices'],
        filter_form.cleaned_data['type_choices'],
        filter_form.cleaned_data['skill_choices'],
        filter_form.cleaned_data['city_choices'],
        filter_form.cleaned_data['deadline'],
        filter_form.cleaned_data['recent']
    )
    schema = ['job_id', 'title', 'company_name', 'sector', 'city', 'state_prov', 'deadline', 'description']
    context = {
        'title': 'Home Page',
        'jobs': filter_by.get_jobs(schema),
        'sectors': sidebar.sectors(),
        'skills': sidebar.skills(),
        'cities': sidebar.cities(),
        'education': sidebar.education(),
        'types': sidebar.job_types()
    }
    return context


class HomeView(ListView):
    template_name = 'jobportal/home/home.html'
    context_object_name = 'jobs'
    queryset = context_object_name

    def get_context_data(self, **kwargs):
        sort_form = SortByForm(self.request.GET or None)
        filter_form = FilterByForm(self.request.GET or None)

        if sort_form.is_valid():
            if sort_form.cleaned_data['sort_by'] == 'Company':
                sort_form.sort_by = 'c.name'
            elif sort_form.cleaned_data['sort_by'] == 'Title':
                sort_form.sort_by = 'j.title'
            elif sort_form.cleaned_data['sort_by'] == 'Sector':
                sort_form.sort_by = 'j.sector, j.title'
            elif sort_form.cleaned_data['sort_by'] == 'Deadline':
                sort_form.sort_by = 'j.deadline'
            elif sort_form.cleaned_data['sort_by'] == 'Location':
                sort_form.sort_by = 'l.city'
            else:
                sort_form.sort_by = DEFAULT
        else:
            sort_form.sort_by = DEFAULT

        if filter_form.is_valid():
            return get_filter_context(filter_form)

        context = get_context(sort_form.sort_by)
        return context


def premium_home(request):
    return render(request, 'jobportal/home/home-prem.html', get_context(DEFAULT))


def company_home(request):
    return render(request, 'jobportal/home/home-comp.html', get_context(DEFAULT))


class Detail(DetailView):
    template_name = 'jobportal/details/details.html'
    context_object_name = 'job'

    def get_object(self, queryset=None):
        schema = ['job_id', 'title', 'company_name', 'sector', 'min_education', 'employment_type',
                  'city', 'state_prov', 'deadline', 'description', 'skills']
        obj = details.get_job(schema, self.kwargs['pk'])
        return obj


def premium_details(request):
    return render(request, 'jobportal/details/details-prem.html', get_context(DEFAULT))


def company_details(request):
    return render(request, 'jobportal/details/details-comp.html', get_context(DEFAULT))


def settings(request):
    return render(request, 'jobportal/settings/settings.html', get_context(DEFAULT))


def settings_prem(request):
    return render(request, 'jobportal/settings/settings-prem.html', get_context(DEFAULT))


def settings_comp(request):
    return render(request, 'jobportal/settings/settings-comp.html', get_context(DEFAULT))


def create_posting(request):
    return render(request, 'jobportal/create-posting.html', get_context(DEFAULT))


def saved_jobs(request):
    return render(request, 'jobportal/saved-jobs.html', get_context(DEFAULT))


def login(request):
    return render(request, 'jobportal/login.html', get_context(DEFAULT))
