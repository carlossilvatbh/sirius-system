from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='main'),
    path('quick-action/', views.quick_action_view, name='quick_action'),
    path('api/', views.dashboard_api_view, name='api'),
]

