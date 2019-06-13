from django.urls import path

from jobportal import views

urlpatterns = [
    path('', views.home, name='home'),
    path('premium', views.premium_home, name='premium-home'),
    path('company', views.company_home, name='company-home'),
    path('details/1', views.details, name='details'),
    path('details/prem', views.premium_details, name='premium-details'),
    path('details/comp', views.company_details, name='company-details'),
    path('settings', views.settings, name='settings'),
    path('settings/prem', views.settings_prem, name='settings-prem'),
    path('settings/comp', views.settings_comp, name='settings-comp'),
    path('create-posting', views.create_posting, name='create-posting'),
    path('saved-jobs', views.saved_jobs, name='saved-jobs'),
    path('login', views.login, name='login'),
]
