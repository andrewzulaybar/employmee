from django import forms


class SortByForm(forms.Form):
    sort_by = forms.CharField(max_length=20)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)
    regular = forms.CharField(max_length=20)
    premium = forms.CharField(max_length=20)
    company = forms.CharField(max_length=20)