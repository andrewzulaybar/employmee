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


class BranchForm(forms.Form):
    id = forms.IntegerField()
    data = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False,
                                     choices=[('Address', 'Address'), ('Contact Email', 'Contact Email')])