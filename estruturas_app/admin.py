from django.contrib import admin
from django.utils.html import format_html
from .models import Estrutura, RegraValidacao, Template, ConfiguracaoSalva, AlertaJurisdicao, UBO, Successor, Product


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




@admin.register(UBO)
class UBOAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Ultimate Beneficial Owners.
    """
    list_display = [
        'nome_completo',
        'nacionalidade_display',
        'tin',
        'data_nascimento',
        'products_count',
        'ativo'
    ]
    list_filter = [
        'nacionalidade',
        'ativo',
        'created_at'
    ]
    search_fields = [
        'nome_completo',
        'tin',
        'email'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome_completo', 'data_nascimento', 'nacionalidade')
        }),
        ('Informações Fiscais', {
            'fields': ('tin', 'endereco_residencia_fiscal')
        }),
        ('Contato', {
            'fields': ('telefone', 'email'),
            'classes': ('collapse',)
        }),
        ('Observações', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
        ('Status e Metadados', {
            'fields': ('ativo', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def nacionalidade_display(self, obj):
        return obj.get_nacionalidade_display()
    nacionalidade_display.short_description = "Nacionalidade"
    nacionalidade_display.admin_order_field = 'nacionalidade'
    
    def products_count(self, obj):
        count = len(obj.get_products_associados())
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if count > 0 else 'gray',
            count
        )
    products_count.short_description = "Products"



@admin.register(Successor)
class SuccessorAdmin(admin.ModelAdmin):
    """
    Admin interface for managing succession between UBOs.
    """
    list_display = [
        'ubo_proprietario',
        'ubo_sucessor',
        'percentual_display',
        'data_efetivacao',
        'efetivado',
        'ativo'
    ]
    list_filter = [
        'efetivado',
        'ativo',
        'data_definicao'
    ]
    search_fields = [
        'ubo_proprietario__nome_completo',
        'ubo_sucessor__nome_completo'
    ]
    autocomplete_fields = ['ubo_proprietario', 'ubo_sucessor']
    readonly_fields = ['data_definicao', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Sucessão', {
            'fields': (
                'ubo_proprietario',
                'ubo_sucessor',
                'percentual'
            )
        }),
        ('Datas', {
            'fields': (
                'data_definicao',
                'data_efetivacao',
                'data_efetivacao_real'
            )
        }),
        ('Condições', {
            'fields': ('condicoes',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('ativo', 'efetivado', 'created_at', 'updated_at')
        }),
    )
    
    def percentual_display(self, obj):
        color = 'green' if obj.percentual == 100 else 'orange'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.2f}%</span>',
            color,
            obj.percentual
        )
    percentual_display.short_description = "Percentual"
    percentual_display.admin_order_field = 'percentual'
    
    def get_form(self, request, obj=None, **kwargs):
        """Customiza form para mostrar percentual disponível"""
        form = super().get_form(request, obj, **kwargs)
        
        if obj and obj.ubo_proprietario:
            # Calcula percentual disponível
            disponivel = obj.get_percentual_disponivel()
            form.base_fields['percentual'].help_text = f"Disponível: {disponivel:.2f}%"
        
        return form
    
    def save_model(self, request, obj, form, change):
        """Override para validar percentuais antes de salvar"""
        try:
            obj.full_clean()
            super().save_model(request, obj, form, change)
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f"Erro ao salvar: {str(e)}")
            raise


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for managing commercial products.
    """
    list_display = [
        'commercial_name',
        'nome',
        'categoria',
        'complexidade_template',
        'custo_display',
        'uso_count',
        'ativo'
    ]
    list_filter = [
        'categoria',
        'complexidade_template',
        'custo_automatico',
        'ativo',
        'created_at'
    ]
    search_fields = [
        'commercial_name',
        'nome',
        'descricao',
        'publico_alvo'
    ]
    readonly_fields = ['uso_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': (
                'nome',
                'commercial_name',
                'categoria',
                'complexidade_template',
                'descricao'
            )
        }),
        ('Configuração Comercial', {
            'fields': (
                'master_agreement_url',
                'configuracao'
            )
        }),
        ('Custos', {
            'fields': (
                'custo_automatico',
                'custo_manual'
            ),
            'description': 'Configure se o custo será calculado automaticamente ou definido manualmente'
        }),
        ('Implementação', {
            'fields': (
                'tempo_total_implementacao',
                'publico_alvo',
                'casos_uso'
            )
        }),
        ('Status e Estatísticas', {
            'fields': (
                'ativo',
                'uso_count',
                'created_at',
                'updated_at'
            )
        }),
    )
    
    def custo_display(self, obj):
        """Exibe custo com formatação e indicação do tipo"""
        custo = obj.get_custo_total_primeiro_ano()
        tipo = "Auto" if obj.custo_automatico else "Manual"
        color = 'green' if obj.custo_automatico else 'blue'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">${:,.2f}</span> <small>({})</small>',
            color,
            custo,
            tipo
        )
    custo_display.short_description = "Custo Total"
    custo_display.admin_order_field = 'custo_manual'
    
    def get_form(self, request, obj=None, **kwargs):
        """Customiza form baseado no tipo de custo"""
        form = super().get_form(request, obj, **kwargs)
        
        # Ajusta help_text baseado no custo_automatico
        if obj and not obj.custo_automatico:
            form.base_fields['custo_manual'].help_text = "Custo definido manualmente (custo automático desabilitado)"
        elif obj and obj.custo_automatico:
            form.base_fields['custo_manual'].help_text = "Campo ignorado quando custo automático está habilitado"
        
        return form
    
    def save_model(self, request, obj, form, change):
        """Override para validar campos de custo"""
        if not obj.custo_automatico and not obj.custo_manual:
            from django.contrib import messages
            messages.warning(
                request, 
                "Atenção: Custo manual não definido. O produto terá custo zero."
            )
        
        super().save_model(request, obj, form, change)
    
    actions = ['incrementar_uso_action', 'ativar_products', 'desativar_products']
    
    def incrementar_uso_action(self, request, queryset):
        """Action para incrementar contador de uso"""
        count = 0
        for product in queryset:
            product.incrementar_uso()
            count += 1
        
        self.message_user(
            request,
            f"Contador de uso incrementado para {count} produto(s)."
        )
    incrementar_uso_action.short_description = "Incrementar contador de uso"
    
    def ativar_products(self, request, queryset):
        """Action para ativar produtos"""
        updated = queryset.update(ativo=True)
        self.message_user(
            request,
            f"{updated} produto(s) ativado(s) com sucesso."
        )
    ativar_products.short_description = "Ativar produtos selecionados"
    
    def desativar_products(self, request, queryset):
        """Action para desativar produtos"""
        updated = queryset.update(ativo=False)
        self.message_user(
            request,
            f"{updated} produto(s) desativado(s) com sucesso."
        )
    desativar_products.short_description = "Desativar produtos selecionados"

