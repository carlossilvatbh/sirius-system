from django.contrib import admin
from django.utils.html import format_html
from .models import Estrutura, RegraValidacao, Template, ConfiguracaoSalva, AlertaJurisdicao


@admin.register(Estrutura)
class EstruturaAdmin(admin.ModelAdmin):
    """
    Admin interface for managing legal structures.
    """
    list_display = [
        'nome', 
        'tipo', 
        'custo_base_formatted', 
        'custo_manutencao_formatted',
        'tempo_implementacao',
        'complexidade_display',
        'nivel_confidencialidade',
        'ativo'
    ]
    list_filter = [
        'tipo', 
        'complexidade', 
        'nivel_confidencialidade', 
        'protecao_patrimonial',
        'ativo'
    ]
    search_fields = ['nome', 'descricao', 'tipo']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('nome', 'tipo', 'descricao', 'ativo')
        }),
        ('Cost Information', {
            'fields': ('custo_base', 'custo_manutencao'),
            'classes': ('collapse',)
        }),
        ('Implementation Details', {
            'fields': ('tempo_implementacao', 'complexidade', 'documentacao_necessaria'),
            'classes': ('collapse',)
        }),
        ('Tax Implications', {
            'fields': (
                'impacto_tributario_eua', 
                'impacto_tributario_brasil', 
                'impacto_tributario_outros',
                'formularios_obrigatorios_eua',
                'formularios_obrigatorios_brasil'
            ),
            'classes': ('collapse',)
        }),
        ('Privacy & Asset Protection', {
            'fields': (
                'nivel_confidencialidade', 
                'protecao_patrimonial', 
                'impacto_privacidade'
            ),
            'classes': ('collapse',)
        }),
        ('Operational Information', {
            'fields': ('facilidade_banking',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def custo_base_formatted(self, obj):
        return f"${obj.custo_base:,.2f}"
    custo_base_formatted.short_description = "Base Cost"
    custo_base_formatted.admin_order_field = 'custo_base'
    
    def custo_manutencao_formatted(self, obj):
        return f"${obj.custo_manutencao:,.2f}"
    custo_manutencao_formatted.short_description = "Maintenance Cost"
    custo_manutencao_formatted.admin_order_field = 'custo_manutencao'
    
    def complexidade_display(self, obj):
        colors = {1: 'green', 2: 'lightgreen', 3: 'orange', 4: 'red', 5: 'darkred'}
        color = colors.get(obj.complexidade, 'gray')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_complexity_display_text()
        )
    complexidade_display.short_description = "Complexity"
    complexidade_display.admin_order_field = 'complexidade'


@admin.register(RegraValidacao)
class RegraValidacaoAdmin(admin.ModelAdmin):
    """
    Admin interface for managing validation rules between structures.
    """
    list_display = [
        'estrutura_a', 
        'estrutura_b', 
        'tipo_relacionamento', 
        'severidade',
        'jurisdicao_aplicavel',
        'ativo'
    ]
    list_filter = [
        'tipo_relacionamento', 
        'severidade',
        'jurisdicao_aplicavel',
        'ativo'
    ]
    search_fields = [
        'estrutura_a__nome', 
        'estrutura_b__nome', 
        'descricao'
    ]
    autocomplete_fields = ['estrutura_a', 'estrutura_b']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Rule Definition', {
            'fields': (
                'estrutura_a', 
                'estrutura_b', 
                'tipo_relacionamento', 
                'severidade'
            )
        }),
        ('Details', {
            'fields': ('descricao', 'jurisdicao_aplicavel', 'condicoes')
        }),
        ('Status', {
            'fields': ('ativo', 'created_at')
        }),
    )


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    """
    Admin interface for managing configuration templates.
    """
    list_display = [
        'nome', 
        'categoria', 
        'complexidade_template',
        'custo_total_formatted',
        'tempo_total_implementacao',
        'uso_count',
        'ativo'
    ]
    list_filter = [
        'categoria', 
        'complexidade_template',
        'ativo'
    ]
    search_fields = ['nome', 'descricao', 'publico_alvo']
    readonly_fields = ['created_at', 'updated_at', 'uso_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'nome', 
                'categoria', 
                'complexidade_template', 
                'descricao'
            )
        }),
        ('Target & Use Cases', {
            'fields': ('publico_alvo', 'casos_uso'),
            'classes': ('collapse',)
        }),
        ('Configuration', {
            'fields': ('configuracao',),
            'classes': ('collapse',)
        }),
        ('Cost & Time', {
            'fields': ('custo_total', 'tempo_total_implementacao')
        }),
        ('Statistics & Status', {
            'fields': ('uso_count', 'ativo', 'created_at', 'updated_at')
        }),
    )
    
    def custo_total_formatted(self, obj):
        return f"${obj.custo_total:,.2f}"
    custo_total_formatted.short_description = "Total Cost"
    custo_total_formatted.admin_order_field = 'custo_total'


@admin.register(ConfiguracaoSalva)
class ConfiguracaoSalvaAdmin(admin.ModelAdmin):
    """
    Admin interface for managing saved configurations.
    """
    list_display = [
        'nome', 
        'custo_estimado_formatted',
        'tempo_estimado',
        'created_at',
        'updated_at'
    ]
    search_fields = ['nome', 'descricao']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('nome', 'descricao')
        }),
        ('Configuration', {
            'fields': ('configuracao',),
            'classes': ('collapse',)
        }),
        ('Estimates', {
            'fields': ('custo_estimado', 'tempo_estimado')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def custo_estimado_formatted(self, obj):
        if obj.custo_estimado:
            return f"${obj.custo_estimado:,.2f}"
        return "-"
    custo_estimado_formatted.short_description = "Estimated Cost"
    custo_estimado_formatted.admin_order_field = 'custo_estimado'


@admin.register(AlertaJurisdicao)
class AlertaJurisdicaoAdmin(admin.ModelAdmin):
    """
    Admin interface for managing jurisdiction-specific alerts.
    """
    list_display = [
        'titulo',
        'jurisdicao',
        'tipo_alerta',
        'prioridade_display',
        'ativo'
    ]
    list_filter = [
        'jurisdicao',
        'tipo_alerta',
        'prioridade',
        'ativo'
    ]
    search_fields = ['titulo', 'descricao']
    filter_horizontal = ['estruturas_aplicaveis']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Alert Information', {
            'fields': ('titulo', 'descricao', 'jurisdicao', 'tipo_alerta')
        }),
        ('Applicability', {
            'fields': ('estruturas_aplicaveis',)
        }),
        ('Priority & Status', {
            'fields': ('prioridade', 'ativo')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def prioridade_display(self, obj):
        colors = {1: 'green', 2: 'lightgreen', 3: 'orange', 4: 'red', 5: 'darkred'}
        color = colors.get(obj.prioridade, 'gray')
        return format_html(
            '<span style="color: {};">Priority {}</span>',
            color,
            obj.prioridade
        )
    prioridade_display.short_description = "Priority"
    prioridade_display.admin_order_field = 'prioridade'


# Customize admin site header and title
admin.site.site_header = "SIRIUS Administration"
admin.site.site_title = "SIRIUS Admin"
admin.site.index_title = "Strategic Intelligence Relationship & Interactive Universal System"

