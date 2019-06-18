from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from urllib.parse import urlencode

from jobportal import details
from jobportal.applicants import Applicants
from jobportal.forms import SortByForm, LoginForm, FilterByForm, JobIDForm, BranchForm
from jobportal.sidebar import Sidebar, SortBy, CompanySidebar
from jobportal.filterquery import JobQuery
from jobportal import savejob
from jobportal.branch import Branch
from jobportal.salary_statistics import SalaryStatistics

DEFAULT = 'j.date DESC'


def get_context(sort_order=DEFAULT, filter_form=None, job_id_form=None, username=None, user_type=None):
    sidebar = Sidebar()
    sort_by = SortBy()
    applicants = Applicants()
    company_sidebar = CompanySidebar()
    salary_statistics = SalaryStatistics()
    schema = ['job_id', 'title', 'company_name', 'sector', 'city', 'state_prov', 'deadline', 'description']
    context = {
        'username': username,
        'user_type': user_type,
        'title': 'Home Page',
        'sectors': sidebar.sectors(),
        'skills': sidebar.skills(),
        'cities': sidebar.cities(),
        'education': sidebar.education(),
        'types': sidebar.job_types(),
        'distinct_applicants': applicants.get_distinct_applicants(username),
        'applicants': 'empty'
    }
    if filter_form is not None and filter_form.is_valid():
        filter_by = JobQuery(
            filter_form.cleaned_data['sector_choices'],
            filter_form.cleaned_data['edu_choices'],
            filter_form.cleaned_data['type_choices'],
            filter_form.cleaned_data['skill_choices'],
            filter_form.cleaned_data['city_choices'],
            filter_form.cleaned_data['deadline'],
            filter_form.cleaned_data['recent']
        )
        context['jobs'] = filter_by.get_jobs(schema)
    elif job_id_form is not None and job_id_form.is_valid():
        schema = ['first_name', 'last_name', 'contact_info', 'position', 'company', 'duration', 'description']
        context['applicants'] = company_sidebar.get_applicants(schema, job_id_form.cleaned_data['job_id'], username)
        job_schema = ['job_id', 'title', 'company_name', 'sector', 'city', 'state_prov', 'deadline', 'description']
        context['jobs'] = sort_by.get_jobs(job_schema, sort_order)
    else:
        context['jobs'] = sort_by.get_jobs(schema, sort_order)
    if user_type == 'premium' or user_type == 'company':
        schema.extend(['applications', 'salary'])
        context['jobs'] = sort_by.get_additional_info(schema, sort_order)
    if user_type == 'premium':
        context['salary_statistics'] = salary_statistics.get_salary_statistics()
    return context


def get_saved_jobs_context(sort_order=DEFAULT, username=None, user_type=None):
    print('in get_saved_jobs username=%s' % username)
    sidebar = Sidebar()
    sort_by = SortBy()
    schema = ['job_id', 'title', 'company_name', 'sector', 'city', 'state_prov', 'deadline', 'description']
    context = {
        'username': username,
        'user_type': user_type,
        'title': 'Home Page',
        'jobs': sort_by.get_saved_jobs(schema, sort_order, username),
        'sectors': sidebar.sectors(),
        'skills': sidebar.skills(),
        'cities': sidebar.cities(),
        'education': sidebar.education(),
        'types': sidebar.job_types()
    }
    return context


def get_branch_context(username=None, user_type=None, form=None):
    branch = Branch()
    if form is not None:
        context = {
            'username': username,
            'user_type': user_type,
            'title': 'Settings',
            'branches': branch.branch_info(username, form),
            'branch_ID': branch.branch_id(username)
        }
    else:
        context = {
            'username': username,
            'user_type': user_type,
            'title': 'Settings',
            'branch_ID': branch.branch_id(username)
        }
    return context


def get_fan_context(username=None, user_type=None):
    applicants = Applicants()
    context = {
        'applicants': applicants.get_top_fans(username),
        'username': username
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


class SaveJob(View):
    def get(self, request):
        print('in saveJob redirect')
        credentials = {'username': request.GET.get('username')}
        savejob.save_prem_job(request.GET.get('username'), request.GET.get('job_id'))
        url = '{}?{}'.format('/premium', urlencode(credentials))
        return redirect(url)


class UnSaveJob(View):
    def get(self, request):
        print('in unsaveJob redirect')
        credentials = {'username': request.GET.get('username')}
        savejob.un_save_prem_job(request.GET.get('username'), request.GET.get('job_id'))
        url = '{}?{}'.format('/premium/saved-jobs', urlencode(credentials))
        return redirect(url)


class HomeView(ListView):
    context_object_name = 'jobs'
    queryset = context_object_name

    def get(self, request, *args, **kwargs):
        url = request.get_full_path().split("?")
        if '/regular' in url[0]:
            self.template_name = 'jobportal/home/home.html'
        if '/premium' in url[0]:
            self.template_name = 'jobportal/home/home-prem.html'
        if '/company' in url[0]:
            self.template_name = 'jobportal/home/home-comp.html'
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        url = self.request.get_full_path().split("?")
        user_type = url[0].split("/")[1]
        if 'company' in url[0]:
            job_id_form = JobIDForm(self.request.GET or None)
            context = get_context(job_id_form=job_id_form,
                                  username=self.request.GET.get('username'),
                                  user_type=user_type)
        elif 'sort' in url[0]:
            sort_form = SortByForm(self.request.GET or None)
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

            context = get_context(sort_order=sort_form.sort_by,
                                  username=self.request.GET.get('username'),
                                  user_type=user_type)
        elif 'filter' in url[0]:
            filter_form = FilterByForm(self.request.GET or None)
            context = get_context(filter_form=filter_form,
                                  username=self.request.GET.get('username'),
                                  user_type=user_type)
        else:
            context = get_context(username=self.request.GET.get('username'),
                                  user_type=user_type)
        return context


class Detail(DetailView):
    template_name = 'jobportal/details/details-prem.html'
    context_object_name = 'job'

    def get(self, request, *args, **kwargs):
        url = request.get_full_path().split("/")
        if 'regular' in url[1]:
            self.template_name = 'jobportal/details/details.html'
        if 'premium' in url[1]:
            self.template_name = 'jobportal/details/details-prem.html'
        if 'company' in url[1]:
            self.template_name = 'jobportal/details/details-comp.html'
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        url = self.request.get_full_path().split("/")
        schema = ['job_id', 'title', 'company_name', 'sector', 'min_education', 'employment_type',
                  'city', 'state_prov', 'deadline', 'description', 'skills']
        if 'premium' in url[1] or 'company' in url[1]:
            schema.insert(10, 'applications')
            schema.insert(11, 'salary')
            obj = details.get_job_prem_comp(schema, self.kwargs['pk'], self.request.GET.get('username'), url[1])
        else:
            obj = details.get_job(schema, self.kwargs['pk'], self.request.GET.get('username'), url[1])
        return obj


class Settings(ListView):
    context_object_name = 'job'
    queryset = context_object_name

    def get(self, request, *args, **kwargs):
        url = request.get_full_path().split("/")
        if 'regular' in url[1]:
            self.template_name = 'jobportal/settings/settings.html'
        if 'premium' in url[1]:
            self.template_name = 'jobportal/settings/settings-prem.html'
        if 'company' in url[1]:
            self.template_name = 'jobportal/settings/settings-comp.html'
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        form = BranchForm(self.request.GET or None)
        url = self.request.get_full_path().split("/")
        obj = {'username': self.request.GET.get('username')}
        if form is not None and form.is_valid():
            obj=get_branch_context(username=self.request.GET.get('username'), user_type=url[1], form=form)
        else:
            obj=get_branch_context(username=self.request.GET.get('username'), user_type=url[1])
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
        print('in get context data for SavedJobs')
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

        url = self.request.get_full_path().split("/")
        context = get_saved_jobs_context(form.sort_by,
                              self.request.GET.get('username'),
                              url[1])
        return context


class EditPosting(DetailView):
    template_name = 'jobportal/edit-posting.html'
    context_object_name = 'job'

    def get_object(self, queryset=None):
        url = self.request.get_full_path().split("/")
        obj = get_context(username=self.request.GET.get('username'), user_type=url[1])
        return obj


class TopFans(DetailView):
    template_name = 'jobportal/top-fans.html'
    context_object_name = 'job'

    def get_object(self, queryset=None):
        url = self.request.get_full_path().split("/")
        obj = get_fan_context(username=self.request.GET.get('username'), user_type=url[1])
        return obj
