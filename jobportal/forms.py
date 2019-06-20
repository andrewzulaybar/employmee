from django import forms
from jobportal.sidebar import Sidebar


class SortByForm(forms.Form):
    sort_by = forms.CharField(max_length=20)


class FilterByForm(forms.Form):
    sidebar = Sidebar()

    sector_choices = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,required=False,
                                               choices=[(s, s) for s in sidebar.sectors()])
    edu_choices = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False,
                                            choices=[(e, e) for e in sidebar.education()])
    type_choices = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False,
                                             choices=[(t, t) for t in sidebar.job_types()])
    skill_choices = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False,
                                              choices=[(k, k) for k in sidebar.skills()])
    city_choices = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False,
                                             choices=[(c, c) for c in sidebar.cities()])
    deadline = forms.IntegerField(required=False)
    recent = forms.IntegerField(required=False)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)
    user_type = forms.CharField(max_length=20)


class JobIDForm(forms.Form):
    job_id = forms.IntegerField()


class BranchForm(forms.Form):
    id = forms.IntegerField()
    data = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False,
                                     choices=[('Address', 'Address'), ('Contact Email', 'Contact Email')])


class ApplyForm(forms.Form):
    CHOICES = (("1", "1"), ("6", "6"), ("7", "7"), ("8", "8"))
    resume_id = forms.ChoiceField(choices=CHOICES)

class CreateJobForm(forms.Form):
    title = forms.CharField(max_length=100)
    sector = forms.CharField(max_length=20)
    description = forms.CharField(max_length=2500)
    deadline = forms.DateField()
    min_education = forms.CharField(max_length=50)
    employment_type = forms.CharField(max_length=100)
    salary = forms.IntegerField()

