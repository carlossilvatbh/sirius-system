from django.urls import path
from . import views

app_name = 'dashboard_public'

urlpatterns = [
    path('', views.PublicDashboardView.as_view(), name='main'),
    path('api/', views.dashboard_api_view, name='api'),
]
