from django.contrib import admin
from .models import (
    Structure, UBO, ValidationRule,
    JurisdictionAlert, Successor, StructureOwnership
)




@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    list_display = [
        'nome', 'tax_classification', 'jurisdicao',
        'custo_base', 'custo_manutencao', 'ativo'
    ]
    list_filter = ['tax_classification', 'jurisdicao', 'ativo', 'created_at']
    search_fields = ['nome', 'descricao']
    fieldsets = [
        ('Basic Information', {
            'fields': ['nome', 'tax_classification', 'descricao']
        }),
        ('Jurisdiction', {
            'fields': ['jurisdicao', 'estado_us', 'estado_br']
        }),
        ('Costs', {
            'fields': ['custo_base', 'custo_manutencao']
        }),
        ('Scores', {
            'fields': ['privacy_score', 'banking_relation_score']
        }),
        ('Templates', {
            'fields': ['templates'],
            'classes': ['collapse']
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
    filter_horizontal = ['estruturas_aplicaveis']
    ordering = ['-prioridade', 'next_deadline']
    fieldsets = [
        ('Basic Information', {
            'fields': ['titulo', 'descricao', 'jurisdicao', 'tipo_alerta']
        }),
        ('Applicability', {
            'fields': ['estruturas_aplicaveis']
        }),
        ('Service Connection', {
            'fields': ['service_connection'],
            'classes': ['collapse']
        }),
        ('Templates and Links', {
            'fields': ['template_url', 'compliance_url'],
            'classes': ['collapse']
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
            ],
            'classes': ['collapse']
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


@admin.register(StructureOwnership)
class StructureOwnershipAdmin(admin.ModelAdmin):
    list_display = ['parent', 'child', 'percentage', 'created_at']
    list_filter = ['parent', 'child', 'created_at']
    search_fields = ['parent__nome', 'child__nome']
    ordering = ['parent__nome', 'child__nome']



