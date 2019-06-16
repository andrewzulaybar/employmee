from django.urls import path

from jobportal import views

urlpatterns = [
    path('regular', views.HomeView.as_view(), name='home'),
    path('premium', views.HomeView.as_view(), name='premium-home'),
    path('company', views.HomeView.as_view(), name='company-home'),
    path('regular/settings', views.Settings.as_view(), name='settings'),
    path('premium/settings', views.Settings.as_view(), name='premium-settings'),
    path('company/settings', views.Settings.as_view(), name='company-settings'),
    path('regular/details/<int:pk>', views.Detail.as_view(), name='details'),
    path('premium/details/<int:pk>', views.Detail.as_view(), name='premium-details'),
    path('company/details/<int:pk>', views.Detail.as_view(), name='company-details'),
    path('create-posting', views.CreatePosting.as_view(), name='create-posting'),
    path('saved-jobs', views.SavedJobs.as_view(), name='saved-jobs'),
    path('login', views.login, name='login'),
    path('logging-in', views.Login.as_view(), name='logging-in'),
    path('sort', views.HomeView.as_view(), name='sort-by-company'),
    path('sort', views.HomeView.as_view(), name='sort-by-title'),
    path('sort', views.HomeView.as_view(), name='sort-by-sector'),
    path('sort', views.HomeView.as_view(), name='sort-by-deadline'),
    path('sort', views.HomeView.as_view(), name='sort-by-location'),
]
