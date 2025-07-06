from django.contrib import admin
from django.utils.html import format_html
from .models import Estrutura, RegraValidacao, AlertaJurisdicao, UBO, Successor, Product, ProductHierarchy, PersonalizedProduct, Service, ServiceActivity


@admin.register(Estrutura)
class EstruturaAdmin(admin.ModelAdmin):
    """
    Admin interface for managing legal structures.
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
            'fields': ('facilidade_banking', 'url_documentos'),
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

    def get_full_jurisdiction_display(self, obj):
        return obj.get_full_jurisdiction_display()
    get_full_jurisdiction_display.short_description = "Jurisdiction"
    get_full_jurisdiction_display.admin_order_field = 'jurisdicao'


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


class ProductHierarchyInline(admin.TabularInline):
    """Inline para gerenciar hierarquia de estruturas dentro de um produto"""
    model = ProductHierarchy
    extra = 1
    fields = [
        'structure',
        'parent_structure',
        'ownership_percentage',
        'hierarchy_level',
        'notes'
    ]
    autocomplete_fields = ['structure', 'parent_structure']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for managing commercial products.
    """
    list_display = [
        'commercial_name',
        'nome',
        'complexidade_template',
        'custo_display',
        'uso_count',
        'ativo'
    ]
    list_filter = [
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
    inlines = [ProductHierarchyInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': (
                'nome',
                'commercial_name',
                'complexidade_template',
                'descricao'
            )
        }),
        ('Configuração Comercial', {
            'fields': (
                'master_agreement_url',
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


@admin.register(ProductHierarchy)
class ProductHierarchyAdmin(admin.ModelAdmin):
    """Admin interface for managing product hierarchies"""
    list_display = [
        'product',
        'structure',
        'parent_structure',
        'hierarchy_level',
        'ownership_percentage'
    ]
    list_filter = [
        'hierarchy_level',
        'product',
        'created_at'
    ]
    search_fields = [
        'product__commercial_name',
        'structure__nome',
        'parent_structure__nome'
    ]
    autocomplete_fields = ['product', 'structure', 'parent_structure']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Hierarchy Definition', {
            'fields': (
                'product',
                'structure',
                'parent_structure',
                'hierarchy_level'
            )
        }),
        ('Ownership Details', {
            'fields': (
                'ownership_percentage',
                'notes'
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'product',
            'structure',
            'parent_structure'
        )


@admin.register(PersonalizedProduct)
class PersonalizedProductAdmin(admin.ModelAdmin):
    """
    Admin interface for managing personalized products.
    """
    list_display = [
        'nome',
        'base_display',
        'status',
        'version_number',
        'ubos_count',
        'custo_display',
        'ativo'
    ]
    list_filter = [
        'status',
        'ativo',
        'version_number',
        'created_at',
    ]
    search_fields = [
        'nome',
        'descricao',
        'base_product__commercial_name',
        'base_product__nome',
        'base_structure__nome',
        'ubos__nome_completo'
    ]
    readonly_fields = ['version_number', 'created_at', 'updated_at']
    autocomplete_fields = ['base_product', 'base_structure', 'parent_version']
    filter_horizontal = ('ubos',)  # Widget for multiple selection of UBOs
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': (
                'nome',
                'descricao',
                'status'
            )
        }),
        ('Base do Produto', {
            'fields': (
                'base_product',
                'base_structure'
            ),
            'description': 'Selecione apenas um: Product ou Structure'
        }),
        ('UBOs Associados', {
            'fields': (
                'ubos',
            ),
            'description': 'UBOs proprietários deste produto personalizado'
        }),
        ('Versionamento', {
            'fields': (
                'version_number',
                'parent_version'
            ),
            'classes': ('collapse',)
        }),
        ('Personalização', {
            'fields': (
                'configuracao_personalizada',
                'custo_personalizado',
                'observacoes'
            ),
            'classes': ('collapse',)
        }),
        ('Status e Metadados', {
            'fields': (
                'ativo',
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def base_display(self, obj):
        """Exibe o objeto base (Product ou Structure)"""
        base_obj = obj.get_base_object()
        base_type = obj.get_base_type()
        
        if base_obj:
            color = 'blue' if base_type == 'Product' else 'green'
            return format_html(
                '<span style="color: {}; font-weight: bold;">[{}]</span> {}',
                color,
                base_type,
                str(base_obj)
            )
        return '-'
    base_display.short_description = "Base"
    
    def ubos_count(self, obj):
        """Exibe número de UBOs associados"""
        count = obj.get_ubos_ativos().count()
        color = 'green' if count > 0 else 'gray'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            count
        )
    ubos_count.short_description = "UBOs"
    
    def custo_display(self, obj):
        """Exibe custo com formatação"""
        custo = obj.get_custo_total()
        tipo = "Custom" if obj.custo_personalizado else "Auto"
        color = 'purple' if obj.custo_personalizado else 'blue'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">${:,.2f}</span> <small>({})</small>',
            color,
            custo,
            tipo
        )
    custo_display.short_description = "Custo Total"
    
    def get_queryset(self, request):
        """Otimiza consultas com select_related e prefetch_related"""
        return super().get_queryset(request).select_related(
            'base_product',
            'base_structure',
            'parent_version'
        ).prefetch_related(
            'ubos'
        )
    
    actions = ['create_new_version_action', 'ativar_products', 'desativar_products']
    
    def create_new_version_action(self, request, queryset):
        """Action para criar nova versão dos produtos selecionados"""
        count = 0
        for pp in queryset:
            if pp.status == 'ACTIVE':
                new_version = pp.create_new_version("Nova versão criada via admin action")
                count += 1
        
        self.message_user(
            request,
            f"Criadas {count} nova(s) versão(ões). Apenas produtos ACTIVE foram versionados."
        )
    create_new_version_action.short_description = "Criar nova versão (apenas ACTIVE)"
    
    def ativar_products(self, request, queryset):
        """Action para ativar produtos"""
        updated = queryset.update(ativo=True)
        self.message_user(
            request,
            f"{updated} produto(s) personalizado(s) ativado(s) com sucesso."
        )
    ativar_products.short_description = "Ativar produtos selecionados"
    
    def desativar_products(self, request, queryset):
        """Action para desativar produtos"""
        updated = queryset.update(ativo=False)
        self.message_user(
            request,
            f"{updated} produto(s) personalizado(s) desativado(s) com sucesso."
        )
    desativar_products.short_description = "Desativar produtos selecionados"


class ServiceActivityInline(admin.TabularInline):
    """Inline for managing ServiceActivity within Service admin"""
    model = ServiceActivity
    extra = 0
    fields = [
        'activity_title', 'start_date', 'due_date', 'status', 
        'priority', 'responsible_person', 'estimated_hours'
    ]
    readonly_fields = ['created_at']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin configuration for Service model"""
    
    list_display = [
        'service_name', 'service_type', 'get_association_display', 
        'cost', 'estimated_duration', 'status', 'ativo'
    ]
    list_filter = [
        'service_type', 'status', 'ativo', 'created_at',
        ('associated_product', admin.RelatedOnlyFieldListFilter),
        ('associated_structure', admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = [
        'service_name', 'description', 'associated_product__nome',
        'associated_structure__nome'
    ]
    autocomplete_fields = ['associated_product', 'associated_structure']
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'service_name', 'description', 'service_type', 'status'
            )
        }),
        ('Cost and Duration', {
            'fields': (
                'cost', 'estimated_duration'
            )
        }),
        ('Associations', {
            'fields': (
                'associated_product', 'associated_structure'
            ),
            'description': 'Associate this service with a Product OR Structure (not both)'
        }),
        ('Configuration', {
            'fields': (
                'requirements', 'deliverables'
            ),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': (
                'ativo',
            )
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ServiceActivityInline]
    
    actions = ['activate_services', 'deactivate_services', 'create_personalized_services']
    
    def get_association_display(self, obj):
        """Display the association type and object"""
        association_type = obj.get_association_type()
        if association_type == "Product":
            return format_html(
                '<span style="color: #007bff;">📦 {}</span>',
                obj.associated_product.nome
            )
        elif association_type == "Structure":
            return format_html(
                '<span style="color: #28a745;">🏢 {}</span>',
                obj.associated_structure.nome
            )
        else:
            return format_html(
                '<span style="color: #6c757d;">🔧 Standalone</span>'
            )
    get_association_display.short_description = 'Association'
    
    def activate_services(self, request, queryset):
        """Activate selected services"""
        updated = queryset.update(status='ACTIVE', ativo=True)
        self.message_user(
            request,
            f'{updated} services were successfully activated.'
        )
    activate_services.short_description = "Activate selected services"
    
    def deactivate_services(self, request, queryset):
        """Deactivate selected services"""
        updated = queryset.update(status='INACTIVE', ativo=False)
        self.message_user(
            request,
            f'{updated} services were successfully deactivated.'
        )
    deactivate_services.short_description = "Deactivate selected services"
    
    def create_personalized_services(self, request, queryset):
        """Create PersonalizedProducts from selected services"""
        created_count = 0
        for service in queryset:
            if service.is_available_for_association():
                service.create_personalized_service()
                created_count += 1
        
        self.message_user(
            request,
            f'{created_count} PersonalizedProducts were created from services.'
        )
    create_personalized_services.short_description = "Create PersonalizedProducts from services"


@admin.register(ServiceActivity)
class ServiceActivityAdmin(admin.ModelAdmin):
    """Admin configuration for ServiceActivity model"""
    
    list_display = [
        'activity_title', 'service', 'start_date', 'due_date', 
        'get_status_display', 'get_priority_display', 'responsible_person',
        'get_progress_display'
    ]
    list_filter = [
        'status', 'priority', 'start_date', 'due_date', 'ativo',
        ('service', admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = [
        'activity_title', 'activity_description', 'responsible_person',
        'service__service_name'
    ]
    autocomplete_fields = ['service']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Activity Information', {
            'fields': (
                'service', 'activity_title', 'activity_description'
            )
        }),
        ('Timeline', {
            'fields': (
                'start_date', 'due_date', 'completion_date'
            )
        }),
        ('Status and Priority', {
            'fields': (
                'status', 'priority'
            )
        }),
        ('Responsibility and Effort', {
            'fields': (
                'responsible_person', 'estimated_hours', 'actual_hours'
            )
        }),
        ('Notes', {
            'fields': (
                'notes',
            ),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': (
                'ativo',
            )
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['mark_completed', 'mark_in_progress', 'mark_on_hold']
    
    def get_status_display(self, obj):
        """Display status with color coding"""
        color = obj.get_status_color()
        return format_html(
            '<span style="color: {}; font-weight: bold;">●</span> {}',
            color, obj.get_status_display()
        )
    get_status_display.short_description = 'Status'
    
    def get_priority_display(self, obj):
        """Display priority with color coding"""
        color = obj.get_priority_color()
        return format_html(
            '<span style="color: {}; font-weight: bold;">●</span> {}',
            color, obj.get_priority_display()
        )
    get_priority_display.short_description = 'Priority'
    
    def get_progress_display(self, obj):
        """Display progress percentage"""
        progress = obj.get_progress_percentage()
        if progress == 100:
            color = '#28a745'  # Green
        elif progress >= 50:
            color = '#ffc107'  # Yellow
        else:
            color = '#6c757d'  # Gray
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}%</span>',
            color, progress
        )
    get_progress_display.short_description = 'Progress'
    
    def mark_completed(self, request, queryset):
        """Mark selected activities as completed"""
        from django.utils import timezone
        updated = queryset.update(
            status='COMPLETED',
            completion_date=timezone.now().date()
        )
        self.message_user(
            request,
            f'{updated} activities were marked as completed.'
        )
    mark_completed.short_description = "Mark as completed"
    
    def mark_in_progress(self, request, queryset):
        """Mark selected activities as in progress"""
        updated = queryset.update(status='IN_PROGRESS')
        self.message_user(
            request,
            f'{updated} activities were marked as in progress.'
        )
    mark_in_progress.short_description = "Mark as in progress"
    
    def mark_on_hold(self, request, queryset):
        """Mark selected activities as on hold"""
        updated = queryset.update(status='ON_HOLD')
        self.message_user(
            request,
            f'{updated} activities were marked as on hold.'
        )
    mark_on_hold.short_description = "Mark as on hold"


# Update AlertaJurisdicaoAdmin with new fields
@admin.register(AlertaJurisdicao)
class AlertaJurisdicaoAdmin(admin.ModelAdmin):
    """Enhanced admin configuration for AlertaJurisdicao model"""
    
    list_display = [
        'titulo', 'jurisdicao', 'tipo_alerta', 'get_deadline_display',
        'get_status_display', 'prioridade', 'ativo'
    ]
    list_filter = [
        'jurisdicao', 'tipo_alerta', 'deadline_type', 'prioridade', 
        'ativo', 'next_deadline', 'recurrence_pattern',
        ('service_connection', admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = [
        'titulo', 'descricao', 'estruturas_aplicaveis__nome',
        'ubos_aplicaveis__nome_completo'
    ]
    autocomplete_fields = ['estruturas_aplicaveis', 'ubos_aplicaveis', 'service_connection']
    date_hierarchy = 'next_deadline'
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'titulo', 'descricao', 'jurisdicao', 'tipo_alerta', 'prioridade'
            )
        }),
        ('Applicability', {
            'fields': (
                'estruturas_aplicaveis', 'ubos_aplicaveis'
            )
        }),
        ('Deadline Configuration', {
            'fields': (
                'deadline_type', 'single_deadline', 'recurrence_pattern',
                'advance_notice_days', 'auto_calculate_next'
            )
        }),
        ('Calculated Deadlines', {
            'fields': (
                'next_deadline', 'last_completed'
            ),
            'classes': ('collapse',)
        }),
        ('Templates and Links', {
            'fields': (
                'template_url', 'compliance_url'
            ),
            'classes': ('collapse',)
        }),
        ('Service Integration', {
            'fields': (
                'service_connection',
            ),
            'classes': ('collapse',)
        }),
        ('Advanced Configuration', {
            'fields': (
                'custom_recurrence_config',
            ),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': (
                'ativo',
            )
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    actions = [
        'mark_completed', 'update_next_deadlines', 'create_service_activities',
        'activate_alerts', 'deactivate_alerts'
    ]
    
    def get_deadline_display(self, obj):
        """Display next deadline with formatting"""
        if not obj.next_deadline:
            return format_html('<span style="color: #6c757d;">No deadline</span>')
        
        days_until = obj.days_until_deadline()
        if obj.is_overdue():
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">⚠️ {} (Overdue)</span>',
                obj.next_deadline.strftime('%Y-%m-%d')
            )
        elif obj.needs_advance_notice():
            return format_html(
                '<span style="color: #ffc107; font-weight: bold;">⏰ {} ({} days)</span>',
                obj.next_deadline.strftime('%Y-%m-%d'), days_until
            )
        else:
            return format_html(
                '<span style="color: #28a745;">📅 {}</span>',
                obj.next_deadline.strftime('%Y-%m-%d')
            )
    get_deadline_display.short_description = 'Next Deadline'
    
    def get_status_display(self, obj):
        """Display status with color coding"""
        status = obj.get_status_display()
        color = obj.get_status_color()
        return format_html(
            '<span style="color: {}; font-weight: bold;">●</span> {}',
            color, status
        )
    get_status_display.short_description = 'Status'
    
    def mark_completed(self, request, queryset):
        """Mark selected alerts as completed"""
        from django.utils import timezone
        updated_count = 0
        for alert in queryset:
            alert.mark_completed()
            updated_count += 1
        
        self.message_user(
            request,
            f'{updated_count} alerts were marked as completed and next deadlines updated.'
        )
    mark_completed.short_description = "Mark as completed"
    
    def update_next_deadlines(self, request, queryset):
        """Update next deadlines for selected alerts"""
        updated_count = 0
        for alert in queryset:
            alert.update_next_deadline()
            updated_count += 1
        
        self.message_user(
            request,
            f'Next deadlines updated for {updated_count} alerts.'
        )
    update_next_deadlines.short_description = "Update next deadlines"
    
    def create_service_activities(self, request, queryset):
        """Create service activities for alerts with service connections"""
        created_count = 0
        for alert in queryset.filter(service_connection__isnull=False):
            activity = alert.create_service_activity()
            if activity:
                created_count += 1
        
        self.message_user(
            request,
            f'{created_count} service activities were created from alerts.'
        )
    create_service_activities.short_description = "Create service activities"
    
    def activate_alerts(self, request, queryset):
        """Activate selected alerts"""
        updated = queryset.update(ativo=True)
        self.message_user(
            request,
            f'{updated} alerts were successfully activated.'
        )
    activate_alerts.short_description = "Activate selected alerts"
    
    def deactivate_alerts(self, request, queryset):
        """Deactivate selected alerts"""
        updated = queryset.update(ativo=False)
        self.message_user(
            request,
            f'{updated} alerts were successfully deactivated.'
        )
    deactivate_alerts.short_description = "Deactivate selected alerts"

