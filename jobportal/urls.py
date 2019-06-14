from django.urls import path

from jobportal import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('premium', views.premium_home, name='premium-home'),
    path('company', views.company_home, name='company-home'),
    path('details/1', views.details, name='details'),
    path('sort', views.HomeView.as_view(), name='sort-by-company'),
    path('sort', views.HomeView.as_view(), name='sort-by-title'),
    path('sort', views.HomeView.as_view(), name='sort-by-sector'),
    path('sort', views.HomeView.as_view(), name='sort-by-deadline'),
    path('sort', views.HomeView.as_view(), name='sort-by-location'),
]
