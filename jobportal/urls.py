from django.urls import path

from jobportal import views

urlpatterns = [
    path('', views.home, name='home'),
]
