from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from urllib.parse import urlencode

from jobportal import details
from jobportal.forms import SortByForm, LoginForm
from jobportal.sidebar import Sidebar, SortBy

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


class HomeView(ListView):
    template_name = 'jobportal/home/home.html'
    context_object_name = 'jobs'
    queryset = context_object_name

    def get_context_data(self, **kwargs):
        form = SortByForm(self.request.GET or None)

        if form.is_valid():
            if form.cleaned_data['sort_by'] == 'Company':
                form.sort_by = 'c.name'
            elif form.cleaned_data['sort_by'] == 'Title':
                form.sort_by = 'j.title'
            elif form.cleaned_data['sort_by'] == 'Sector':
                form.sort_by = 'j.sector, j.title'
            elif form.cleaned_data['sort_by'] == 'Deadline':
                form.sort_by = 'j.deadline'
            elif form.cleaned_data['sort_by'] == 'Location':
                form.sort_by = 'l.city'
            else:
                form.sort_by = DEFAULT
        else:
            form.sort_by = DEFAULT

        context = get_context(form.sort_by)
        context['user_name'] = self.request.GET.get('username')
        return context


def logging_in(request):
    form = LoginForm(request.GET or None)
    form.is_valid()
    form2 = {'username': form.cleaned_data.get('username')}
    url = "/login"
    if form.cleaned_data.get('premium') == 'on':
        url = '{}?{}'.format('/premium', urlencode(form2))
    if form.cleaned_data.get('regular') == 'on':
        url = '{}?{}'.format('/', urlencode(form2))
    if form.cleaned_data.get('company') == 'on':
        url = '{}?{}'.format('/company', urlencode(form2))
    return redirect(url)


def premium_home(request):
    context = get_context(DEFAULT)
    context['user_name'] = request.GET.get('username')
    return render(request, 'jobportal/home/home-prem.html', context)


def company_home(request):
    context = get_context(DEFAULT)
    context['user_name'] = request.GET.get('username')
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
