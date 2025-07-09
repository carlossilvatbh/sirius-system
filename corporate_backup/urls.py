from django.urls import path
from . import views

app_name = 'corporate'

urlpatterns = [
    path('', views.canvas_modern, name='canvas_modern'),
]
