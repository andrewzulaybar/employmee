from django.urls import path

from jobportal import views

urlpatterns = [
    path('', views.home, name='home'),
    path('premium', views.premium_home, name='premium-home'),
    path('company', views.company_home, name='company-home'),
    path('details/1', views.details, name='details'),
    path('details/prem', views.premium_details, name='premium-details'),
    path('details/comp', views.company_details, name='company-details'),
    path('login', views.login, name='login'),
    path('settings', views.settings, name='settings'),
]
