from django.urls import path

from jobportal import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('company', views.company_home, name='company-home'),
    path('details/<int:pk>/', views.Detail.as_view(), name='details'),
    path('details/comp', views.company_details, name='company-details'),
    path('settings', views.Settings.as_view(), name='settings'),
    path('settings/comp', views.settings_comp, name='settings-comp'),
    path('create-posting', views.create_posting, name='create-posting'),
    path('saved-jobs', views.SavedJobs.as_view(), name='saved-jobs'),
    path('login', views.login, name='login'),
    path('logging-in', views.Login.as_view(), name='logging-in'),
    path('sort', views.HomeView.as_view(), name='sort-by-company'),
    path('sort', views.HomeView.as_view(), name='sort-by-title'),
    path('sort', views.HomeView.as_view(), name='sort-by-sector'),
    path('sort', views.HomeView.as_view(), name='sort-by-deadline'),
    path('sort', views.HomeView.as_view(), name='sort-by-location'),
]
