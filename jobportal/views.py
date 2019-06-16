from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from urllib.parse import urlencode

from jobportal import details
from jobportal.forms import SortByForm, LoginForm
from jobportal.sidebar import Sidebar, SortBy

DEFAULT = 'date DESC'


def get_context(sort_order=DEFAULT, username=None, user_type=None):
    sidebar = Sidebar()
    sort_by = SortBy()
    schema = ['job_id', 'title', 'company_name', 'sector', 'city', 'state_prov', 'deadline', 'description']
    context = {
        'username': username,
        'user_type': user_type,
        'title': 'Home Page',
        'jobs': sort_by.get_jobs(schema, sort_order),
        'sectors': sidebar.sectors(),
        'skills': sidebar.skills(),
        'cities': sidebar.cities(),
        'education': sidebar.education(),
        'types': sidebar.job_types()
    }
    return context


def login(request):
    return render(request, 'jobportal/login.html', get_context())


class Login(View):
    def get(self, request):
        credentials = {'username': request.GET.get('username'),
                       'user_type': request.GET.get('user_type')}
        url = "/login"
        if request.GET.get('user_type') == 'regular':
            url = '{}?{}'.format('/', urlencode(credentials))
        if request.GET.get('user_type') == 'premium':
            url = '{}?{}'.format('/', urlencode(credentials))
        if request.GET.get('user_type') == 'company':
            url = '{}?{}'.format('/company', urlencode(credentials))
        return redirect(url)


class HomeView(ListView):
    template_name = 'jobportal/home/home-prem.html'
    context_object_name = 'jobs'
    queryset = context_object_name

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('user_type') == 'regular':
            self.template_name = 'jobportal/home/home.html'
        return super().get(request, *args, **kwargs)

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

        context = get_context(form.sort_by,
                              self.request.GET.get('username'),
                              self.request.GET.get('user_type'))
        return context


def company_home(request):
    context = get_context(DEFAULT, request.GET.get('username'))
    return render(request, 'jobportal/home/home-comp.html', context)


class Detail(DetailView):
    template_name = 'jobportal/details/details-prem.html'
    context_object_name = 'job'

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('user_type') == 'regular':
            self.template_name = 'jobportal/details/details.html'
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        schema = ['job_id', 'title', 'company_name', 'sector', 'min_education', 'employment_type',
                  'city', 'state_prov', 'deadline', 'description', 'skills']
        obj = details.get_job(schema, self.kwargs['pk'], self.request.GET.get('username'))
        return obj


def company_details(request):
    return render(request, 'jobportal/details/details-comp.html', get_context())


class Settings(DetailView):
    template_name = 'jobportal/settings/settings-prem.html'
    context_object_name = 'job'

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('user_type') == 'regular':
            self.template_name = 'jobportal/settings/settings.html'
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = get_context(username=self.request.GET.get('username'),
                          user_type=self.request.GET.get('user_type'))
        return obj


def settings_comp(request):
    return render(request, 'jobportal/settings/settings-comp.html', get_context())


def create_posting(request):
    return render(request, 'jobportal/create-posting.html', get_context())


class SavedJobs(ListView):
    template_name = 'jobportal/saved-jobs.html'
    context_object_name = 'jobs'
    queryset = context_object_name

    def get_context_data(self, *, object_list=None, **kwargs):
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

        context = get_context(form.sort_by,
                              self.request.GET.get('username'),
                              self.request.GET.get('user_type'))
        return context
