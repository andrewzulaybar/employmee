from django.urls import path

from jobportal import views

urlpatterns = [
    path('', views.login, name='login'),
    path('regular', views.HomeView.as_view(), name='home'),
    path('premium', views.HomeView.as_view(), name='premium-home'),
    path('company', views.HomeView.as_view(), name='company-home'),
    path('regular/settings', views.Settings.as_view(), name='settings'),
    path('premium/settings', views.Settings.as_view(), name='premium-settings'),
    path('company/settings', views.Settings.as_view(), name='company-settings'),
    path('regular/details/<int:pk>', views.Detail.as_view(), name='details'),
    path('premium/details/<int:pk>', views.Detail.as_view(), name='premium-details'),
    path('company/details/<int:pk>', views.Detail.as_view(), name='company-details'),
    path('company/create-posting', views.CreatePosting.as_view(), name='create-posting'),
    path('company/edit-posting', views.EditPosting.as_view(), name='edit-posting'),
    path('premium/saved-jobs', views.SavedJobs.as_view(), name='saved-jobs'),
    path('logging-in', views.Login.as_view(), name='logging-in'),
    path('regular/sort', views.HomeView.as_view(), name='sort-by'),
    path('premium/sort', views.HomeView.as_view(), name='sort-by-premium'),
    path('premium/saved-jobs/sort', views.SavedJobs.as_view(), name='sort-by-saved-jobs'),
    path('company/top-fans', views.TopFans.as_view(), name='top-fans'),
    path('regular/filter', views.HomeView.as_view(), name='filter-by'),
    path('premium/filter', views.HomeView.as_view(), name='filter-by-premium'),
    path('save-job', views.SaveJob.as_view(), name='save-job'),
    path('unsave-job', views.UnSaveJob.as_view(), name='unsave-job'),
    path('branch', views.Settings.as_view(), name='branch')
]
