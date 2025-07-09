from django.contrib import admin
from .models import EntityPrice, IncorporationCost, ServicePrice, ServiceCost


class IncorporationCostInline(admin.TabularInline):
    model = IncorporationCost
    extra = 1
    fields = ['name', 'cost_type', 'value']


class ServiceCostInline(admin.TabularInline):
    model = ServiceCost
    extra = 1
    fields = ['name', 'cost_type', 'value']


@admin.register(EntityPrice)
class EntityPriceAdmin(admin.ModelAdmin):
    list_display = ['entity', 'base_currency', 'markup_type', 'markup_value', 'created_at']
    list_filter = ['base_currency', 'markup_type', 'created_at']
    search_fields = ['entity__name']
    inlines = [IncorporationCostInline]
    
    fieldsets = (
        ('Entity Information', {
            'fields': ('entity',)
        }),
        ('Pricing Configuration', {
            'fields': ('base_currency', 'markup_type', 'markup_value')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(IncorporationCost)
class IncorporationCostAdmin(admin.ModelAdmin):
    list_display = ['name', 'entity_price', 'cost_type', 'value', 'created_at']
    list_filter = ['cost_type', 'created_at']
    search_fields = ['name', 'entity_price__entity__name']
    
    fieldsets = (
        ('Cost Information', {
            'fields': ('entity_price', 'name', 'cost_type', 'value')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ServicePrice)
class ServicePriceAdmin(admin.ModelAdmin):
    list_display = ['service', 'base_currency', 'markup_type', 'markup_value', 'created_at']
    list_filter = ['base_currency', 'markup_type', 'created_at']
    search_fields = ['service__name']
    inlines = [ServiceCostInline]
    
    fieldsets = (
        ('Service Information', {
            'fields': ('service',)
        }),
        ('Pricing Configuration', {
            'fields': ('base_currency', 'markup_type', 'markup_value')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ServiceCost)
class ServiceCostAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_price', 'cost_type', 'value', 'created_at']
    list_filter = ['cost_type', 'created_at']
    search_fields = ['name', 'service_price__service__name']
    
    fieldsets = (
        ('Cost Information', {
            'fields': ('service_price', 'name', 'cost_type', 'value')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

