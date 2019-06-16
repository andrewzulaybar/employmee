from django.urls import reverse, resolve
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from urllib.parse import urlencode, urlparse

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
        credentials = {'username': request.GET.get('username')}
        form = LoginForm(self.request.GET or None)
        url = "/login"
        if form.is_valid():
            if form.cleaned_data.get('user_type') == 'regular':
                url = '{}?{}'.format('/regular', urlencode(credentials))
            if form.cleaned_data.get('user_type') == 'premium':
                url = '{}?{}'.format('/premium', urlencode(credentials))
            if form.cleaned_data.get('user_type') == 'company':
                url = '{}?{}'.format('/company', urlencode(credentials))
        return redirect(url)


class HomeView(ListView):
    template_name = 'jobportal/home/home-prem.html'
    context_object_name = 'jobs'
    queryset = context_object_name

    def get(self, request, *args, **kwargs):
        url = request.get_full_path().split("?")
        if url[0] == reverse("home"):
            self.template_name = 'jobportal/home/home.html'
        if url[0] == reverse("premium-home"):
            self.template_name = 'jobportal/home/home-prem.html'
        if url[0] == reverse("company-home"):
            self.template_name = 'jobportal/home/home-comp.html'
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

        url = self.request.get_full_path().split("?")
        context = get_context(form.sort_by,
                              self.request.GET.get('username'),
                              url[0])
        return context


class Detail(DetailView):
    template_name = 'jobportal/details/details-prem.html'
    context_object_name = 'job'

    def get(self, request, *args, **kwargs):
        url = request.get_full_path().split("/")
        if url[1] == 'regular':
            self.template_name = 'jobportal/details/details.html'
        if url[1] == 'premium':
            self.template_name = 'jobportal/details/details-prem.html'
        if url[1] == 'company':
            self.template_name = 'jobportal/details/details-comp.html'
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        url = self.request.get_full_path().split("/")
        schema = ['job_id', 'title', 'company_name', 'sector', 'min_education', 'employment_type',
                  'city', 'state_prov', 'deadline', 'description', 'skills']
        obj = details.get_job(schema, self.kwargs['pk'], self.request.GET.get('username'), url[1])
        return obj


class Settings(DetailView):
    context_object_name = 'job'

    def get(self, request, *args, **kwargs):
        url = request.get_full_path().split("?")
        if url[0] == reverse("home"):
            self.template_name = 'jobportal/settings/settings.html'
        if url[0] == reverse("premium-settings"):
            self.template_name = 'jobportal/settings/settings-prem.html'
        if url[0] == reverse("company-settings"):
            self.template_name = 'jobportal/settings/settings-comp.html'
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        url = self.request.get_full_path().split("/")
        obj = get_context(username=self.request.GET.get('username'), user_type=url[0])
        return obj


class CreatePosting(DetailView):
    template_name = 'jobportal/create-posting.html'
    context_object_name = 'job'

    def get_object(self, queryset=None):
        obj = get_context(username=self.request.GET.get('username'))
        return obj


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
