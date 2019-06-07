from django.shortcuts import render


def home(request):
    context = {
        'title': 'Home Page'
    }
    return render(request, 'jobportal/base.html', context)
