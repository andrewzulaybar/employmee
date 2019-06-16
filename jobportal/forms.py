from django import forms


class SortByForm(forms.Form):
    sort_by = forms.CharField(max_length=20)
