from django.contrib import admin
from .models import Product, ProductHierarchy, PersonalizedProduct


class ProductHierarchyInline(admin.TabularInline):
    model = ProductHierarchy
    extra = 1
    fields = ['structure', 'order', 'custom_cost', 'notes']
    ordering = ['order']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['nome', 'commercial_name', 'complexidade_template',
                    'uso_count', 'ativo']
    list_filter = ['complexidade_template', 'ativo', 'created_at']
    search_fields = ['nome', 'commercial_name', 'descricao']
    inlines = [ProductHierarchyInline]
    fieldsets = [
        ('Basic Information', {
            'fields': ['nome', 'commercial_name', 'complexidade_template',
                       'descricao']
        }),
        ('Commercial Details', {
            'fields': ['master_agreement_url', 'publico_alvo', 'casos_uso']
        }),
        ('Cost Configuration', {
            'fields': ['custo_automatico', 'custo_manual']
        }),
        ('Implementation', {
            'fields': ['tempo_total_implementacao']
        }),
        ('Status', {
            'fields': ['ativo']
        }),
    ]
    ordering = ['-uso_count', 'commercial_name']


@admin.register(ProductHierarchy)
class ProductHierarchyAdmin(admin.ModelAdmin):
    list_display = ['product', 'structure', 'order', 'custom_cost']
    list_filter = ['product', 'structure', 'created_at']
    search_fields = ['product__nome', 'structure__nome']
    ordering = ['product', 'order']


@admin.register(PersonalizedProduct)
class PersonalizedProductAdmin(admin.ModelAdmin):
    list_display = ['nome', 'get_base_type', 'status', 'version_number',
                    'ativo']
    list_filter = ['status', 'version_number', 'ativo', 'created_at']
    search_fields = ['nome', 'descricao', 'base_product__nome',
                     'base_structure__nome']
    fieldsets = [
        ('Basic Information', {
            'fields': ['nome', 'descricao', 'status']
        }),
        ('Base Configuration', {
            'fields': ['base_product', 'base_structure']
        }),
        ('Versioning', {
            'fields': ['version_number', 'parent_version']
        }),
        ('Customization', {
            'fields': ['configuracao_personalizada', 'custo_personalizado',
                       'observacoes']
        }),
        ('Status', {
            'fields': ['ativo']
        }),
    ]
    ordering = ['-version_number', '-created_at']
    
    def get_base_type(self, obj):
        return obj.get_base_type()
    get_base_type.short_description = 'Base Type'


