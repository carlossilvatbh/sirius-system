from django.contrib import admin
from django.utils.html import format_html
from .models import Estrutura


@admin.register(Estrutura)
class EstruturaAdmin(admin.ModelAdmin):
    """
    Admin interface for managing legal structures.
    
    NOTE: This is kept for backward compatibility.
    New functionality should use corporate.Structure.
    """
    list_display = [
        'nome', 
        'tipo', 
        'get_full_jurisdiction_display',
        'custo_base_formatted', 
        'custo_manutencao_formatted',
        'tempo_implementacao',
        'complexidade_display',
        'nivel_confidencialidade',
        'ativo'
    ]
    list_filter = [
        'tipo',
        'jurisdicao',
        'estado_us',
        'estado_br',
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
        ('Jurisdiction', {
            'fields': ('jurisdicao', 'estado_us', 'estado_br'),
            'description': 'Select state only if jurisdiction is US or Brazil'
        }),
        ('Cost Information', {
            'fields': ('custo_base', 'custo_manutencao'),
            'classes': ('collapse',)
        }),
        ('Implementation Details', {
            'fields': ('tempo_implementacao', 'complexidade', 'documentacao_necessaria'),
            'classes': ('collapse',)
        }),
        ('Tax Impact', {
            'fields': ('impacto_tributario_eua', 'impacto_tributario_brasil', 'impacto_tributario_outros'),
            'classes': ('collapse',)
        }),
        ('Privacy and Protection', {
            'fields': ('nivel_confidencialidade', 'protecao_patrimonial', 'impacto_privacidade'),
            'classes': ('collapse',)
        }),
        ('Operational', {
            'fields': ('facilidade_banking', 'url_documentos'),
            'classes': ('collapse',)
        }),
        ('Compliance', {
            'fields': ('formularios_obrigatorios_eua', 'formularios_obrigatorios_brasil'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def custo_base_formatted(self, obj):
        """Format base cost for display"""
        return f"${obj.custo_base:,.2f}"
    custo_base_formatted.short_description = 'Base Cost'
    custo_base_formatted.admin_order_field = 'custo_base'
    
    def custo_manutencao_formatted(self, obj):
        """Format maintenance cost for display"""
        return f"${obj.custo_manutencao:,.2f}"
    custo_manutencao_formatted.short_description = 'Maintenance Cost'
    custo_manutencao_formatted.admin_order_field = 'custo_manutencao'
    
    def complexidade_display(self, obj):
        """Display complexity with color coding"""
        colors = {
            1: '#28a745',  # Green
            2: '#6c757d',  # Gray
            3: '#ffc107',  # Yellow
            4: '#fd7e14',  # Orange
            5: '#dc3545',  # Red
        }
        color = colors.get(obj.complexidade, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_complexity_display_text()
        )
    complexidade_display.short_description = 'Complexity'
    complexidade_display.admin_order_field = 'complexidade'

