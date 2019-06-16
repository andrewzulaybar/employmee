from django.urls import path

from jobportal import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('premium', views.premium_home, name='premium-home'),
    path('company', views.company_home, name='company-home'),
    path('details/<int:pk>/', views.Detail.as_view(), name='details'),
    path('details/prem', views.premium_details, name='premium-details'),
    path('details/comp', views.company_details, name='company-details'),
    path('settings', views.settings, name='settings'),
    path('settings/prem', views.settings_prem, name='settings-prem'),
    path('settings/comp', views.settings_comp, name='settings-comp'),
    path('create-posting', views.create_posting, name='create-posting'),
    path('edit-posting', views.edit_posting, name='edit-posting'),
    path('saved-jobs', views.saved_jobs, name='saved-jobs'),
    path('login', views.login, name='login'),
    path('top-fans', views.top_fans, name='top-fans'),
    path('sort', views.HomeView.as_view(), name='sort-by-company'),
    path('sort', views.HomeView.as_view(), name='sort-by-title'),
    path('sort', views.HomeView.as_view(), name='sort-by-sector'),
    path('sort', views.HomeView.as_view(), name='sort-by-deadline'),
    path('sort', views.HomeView.as_view(), name='sort-by-location'),
]
