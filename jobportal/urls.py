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
    path('premium/saved-jobs', views.SavedJobs.as_view(), name='saved-jobs'),
    path('login', views.login, name='login'),
    path('logging-in', views.Login.as_view(), name='logging-in'),
    path('regular/sort', views.HomeView.as_view(), name='sort-by'),
    path('premium/sort', views.HomeView.as_view(), name='sort-by-premium'),
    path('premium/saved-jobs/sort', views.SavedJobs.as_view(), name='sort-by-saved-jobs')
]
