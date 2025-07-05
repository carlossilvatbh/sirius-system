from django.urls import path
from . import views

app_name = 'estruturas'

urlpatterns = [
    # Main views
    path('', views.canvas_principal, name='canvas_principal'),
    path('admin-estruturas/', views.admin_estruturas, name='admin_estruturas'),
    
    # API endpoints
    path('api/estruturas/', views.api_estruturas, name='api_estruturas'),
    path('api/templates/', views.api_templates, name='api_templates'),
    path('api/calcular-custos/', views.api_calcular_custos, name='api_calcular_custos'),
    path('api/validar-configuracao/', views.api_validar_configuracao, name='api_validar_configuracao'),
    path('api/regras-validacao/', views.api_regras_validacao, name='api_regras_validacao'),
    path('api/alertas-jurisdicao/', views.api_alertas_jurisdicao, name='api_alertas_jurisdicao'),
    path('api/salvar-configuracao/', views.api_salvar_configuracao, name='api_salvar_configuracao'),
    path('api/configuracoes-salvas/', views.api_configuracoes_salvas, name='api_configuracoes_salvas'),
    path('api/aplicar-template/', views.api_aplicar_template, name='api_aplicar_template'),
    path('api/generate-pdf/', views.api_generate_pdf, name='api_generate_pdf'),
]

