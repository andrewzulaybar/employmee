from django import forms


class SortByForm(forms.Form):
    sort_by = forms.CharField(max_length=20)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)
    user_type = forms.CharField(max_length=20)
