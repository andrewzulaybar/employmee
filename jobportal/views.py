from django.shortcuts import render
from django.views.generic import ListView

from jobportal.forms import SortByForm
from jobportal.sidebar import Sidebar, SortBy


def get_context(sort_order):
    sidebar = Sidebar()
    sort_by = SortBy()
    schema = ['title', 'company_name', 'sector', 'city', 'state_prov', 'deadline', 'description']
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
    template_name = 'jobportal/home.html'
    context_object_name = 'jobs'
    queryset = context_object_name

    def get_context_data(self, **kwargs):
        form = SortByForm(self.request.GET or None)

        if form.is_valid():
            if form.cleaned_data['sort_by'] == 'Company':
                form.sort_by = 'c.name'
            elif form.cleaned_data['sort_by'] == 'Title':
                form.sort_by = 'j.title'
            else:
                form.sort_by = 'date DESC'
        else:
            form.sort_by = 'date DESC'

        context = super(HomeView, self).get_context_data(**kwargs)
        context['jobs'] = get_context(form.sort_by)['jobs']
        return context


def premium_home(request):
    return render(request, 'jobportal/home-prem.html', get_context())


def company_home(request):
    return render(request, 'jobportal/home-comp.html', get_context())


def details(request):
    return render(request, 'jobportal/details.html', get_context())
