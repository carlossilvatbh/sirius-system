from django.urls import path
from . import views

app_name = 'estruturas_app'

urlpatterns = [
    # Main canvas interface
    path('', views.canvas_principal, name='canvas_principal'),
    
    # API endpoints for structures
    path('api/estruturas/', views.estruturas_json, name='estruturas_json'),
    path('api/estrutura/<int:estrutura_id>/', views.estrutura_detail, name='estrutura_detail'),
    
    # Validation endpoint
    path('api/validar/', views.validar_configuracao, name='validar_configuracao'),
    
    # Template management
    path('api/templates/', views.templates_json, name='templates_json'),
    path('api/template/<int:template_id>/', views.carregar_template, name='carregar_template'),
    path('api/salvar-template/', views.salvar_template, name='salvar_template'),
    
    # Configuration management
    path('api/salvar-configuracao/', views.salvar_configuracao, name='salvar_configuracao'),
    
    # Admin interface
    path('admin-estruturas/', views.admin_estruturas, name='admin_estruturas'),
]

