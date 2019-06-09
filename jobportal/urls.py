from django.urls import path

from jobportal import views

urlpatterns = [
    path('', views.home, name='home'),
    path('premium', views.premium_home, name='premium-home'),
    path('company', views.company_home, name='company-home'),
    path('details/1', views.details, name='details'),
]
