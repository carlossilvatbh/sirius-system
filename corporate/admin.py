from django.contrib import admin
from .models import (
    TaxClassification, Structure, UBO, ValidationRule, 
    JurisdictionAlert, Successor, Service, ServiceActivity
)


@admin.register(TaxClassification)
class TaxClassificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    list_filter = ['name', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    list_display = [
        'nome', 'get_tax_classifications_display', 'jurisdicao', 
        'custo_base', 'custo_manutencao', 'ativo'
    ]
    list_filter = ['tax_classifications', 'jurisdicao', 'ativo', 'created_at']
    search_fields = ['nome', 'descricao']
    filter_horizontal = ['tax_classifications']
    fieldsets = [
        ('Basic Information', {
            'fields': ['nome', 'tax_classifications', 'descricao']
        }),
        ('Jurisdiction', {
            'fields': ['jurisdicao', 'estado_us', 'estado_br']
        }),
        ('Costs', {
            'fields': ['custo_base', 'custo_manutencao']
        }),
        ('Scores', {
            'fields': ['privacidade_score', 'compliance_score']
        }),
        ('Implementation', {
            'fields': ['tempo_implementacao', 'documentos_necessarios']
        }),
        ('Status', {
            'fields': ['ativo']
        }),
    ]
    ordering = ['nome']


@admin.register(UBO)
class UBOAdmin(admin.ModelAdmin):
    list_display = [
        'nome', 'tipo_pessoa', 'email', 'telefone', 'pais', 'ativo'
    ]
    list_filter = ['tipo_pessoa', 'pais', 'ativo', 'created_at']
    search_fields = ['nome', 'email', 'documento_identidade']
    fieldsets = [
        ('Basic Information', {
            'fields': ['nome', 'tipo_pessoa']
        }),
        ('Contact Information', {
            'fields': ['email', 'telefone']
        }),
        ('Address Information', {
            'fields': ['endereco', 'cidade', 'estado', 'pais', 'cep']
        }),
        ('Identification', {
            'fields': ['documento_identidade', 'tipo_documento']
        }),
        ('Additional Information', {
            'fields': ['nacionalidade', 'data_nascimento']
        }),
        ('Status', {
            'fields': ['ativo']
        }),
    ]
    ordering = ['nome']


@admin.register(ValidationRule)
class ValidationRuleAdmin(admin.ModelAdmin):
    list_display = [
        'estrutura_a', 'estrutura_b', 'tipo_relacionamento', 
        'severidade', 'ativo'
    ]
    list_filter = [
        'tipo_relacionamento', 'severidade', 'ativo', 'created_at'
    ]
    search_fields = [
        'estrutura_a__nome', 'estrutura_b__nome', 'descricao'
    ]
    ordering = ['estrutura_a__nome', 'estrutura_b__nome']


@admin.register(JurisdictionAlert)
class JurisdictionAlertAdmin(admin.ModelAdmin):
    list_display = [
        'titulo', 'jurisdicao', 'tipo_alerta', 'deadline_type', 
        'next_deadline', 'prioridade', 'ativo'
    ]
    list_filter = [
        'jurisdicao', 'tipo_alerta', 'deadline_type', 
        'prioridade', 'ativo', 'created_at'
    ]
    search_fields = ['titulo', 'descricao']
    filter_horizontal = ['estruturas_aplicaveis', 'ubos_aplicaveis']
    ordering = ['-prioridade', 'next_deadline']
    fieldsets = [
        ('Basic Information', {
            'fields': ['titulo', 'descricao', 'jurisdicao', 'tipo_alerta']
        }),
        ('Applicability', {
            'fields': ['estruturas_aplicaveis', 'ubos_aplicaveis']
        }),
        ('Deadline Configuration', {
            'fields': [
                'deadline_type', 'single_deadline', 'recurrence_pattern',
                'next_deadline', 'last_completed'
            ]
        }),
        ('Advanced Settings', {
            'fields': [
                'advance_notice_days', 'auto_calculate_next',
                'custom_recurrence_config'
            ]
        }),
        ('Priority and Status', {
            'fields': ['prioridade', 'ativo']
        }),
    ]


@admin.register(Successor)
class SuccessorAdmin(admin.ModelAdmin):
    list_display = [
        'ubo_proprietario', 'ubo_sucessor', 'percentual', 
        'ativo', 'efetivado'
    ]
    list_filter = ['ativo', 'efetivado', 'created_at']
    search_fields = [
        'ubo_proprietario__nome', 'ubo_sucessor__nome'
    ]
    ordering = ['-percentual', 'data_definicao']


class ServiceActivityInline(admin.TabularInline):
    model = ServiceActivity
    extra = 1
    fields = [
        'activity_title', 'status', 'priority', 'start_date', 
        'due_date', 'responsible_person'
    ]
    ordering = ['-start_date']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'service_name', 'service_type', 'status', 
        'associated_structure', 'cost', 'ativo'
    ]
    list_filter = ['service_type', 'status', 'ativo', 'created_at']
    search_fields = ['service_name', 'description']
    inlines = [ServiceActivityInline]
    fieldsets = [
        ('Basic Information', {
            'fields': ['service_name', 'description', 'service_type']
        }),
        ('Cost and Duration', {
            'fields': ['cost', 'estimated_duration']
        }),
        ('Associations', {
            'fields': ['associated_structure']
        }),
        ('Configuration', {
            'fields': ['requirements', 'deliverables']
        }),
        ('Status', {
            'fields': ['status', 'ativo']
        }),
    ]
    ordering = ['service_name']


@admin.register(ServiceActivity)
class ServiceActivityAdmin(admin.ModelAdmin):
    list_display = [
        'activity_title', 'service', 'status', 'priority', 
        'start_date', 'due_date', 'responsible_person'
    ]
    list_filter = [
        'status', 'priority', 'service__service_type', 'ativo'
    ]
    search_fields = [
        'activity_title', 'activity_description', 
        'service__service_name', 'responsible_person'
    ]
    ordering = ['-start_date', 'priority']
