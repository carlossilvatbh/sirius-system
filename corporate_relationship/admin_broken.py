from django.contrib import admin
from .models import (
    File, RelationshipStructure, 
    Service, ServiceActivity, WebhookLog
)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['structure', 'approved_by', 'approved_at', 'created_at']
    list_filter = ['approved_at', 'created_at']
    search_fields = ['structure__name', 'approved_by__name']
    readonly_fields = ['created_at', 'approved_at']

    fieldsets = [
        ('Structure Information', {
            'fields': ['structure']
        }),
        ('Approval', {
            'fields': ['approved_by', 'approved_at']
        }),
        ('Metadata', {
            'fields': ['created_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(RelationshipStructure)
class RelationshipStructureAdmin(admin.ModelAdmin):
    list_display = ['structure', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['structure__name']
    list_select_related = ['structure']
    readonly_fields = ['created_at']


class ServiceActivityInline(admin.TabularInline):
    model = ServiceActivity
    extra = 1
    fields = ['order', 'name', 'status']
    ordering = ['order']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'counterparty_name', 
        'service_price', 
        'regulator_fee',
        'total_cost_display',
        'executor'
    ]
    search_fields = ['name', 'counterparty_name', 'description']
    list_filter = [
        'executor', 
        'service_price_currency',
        'created_at'
    ]
    filter_horizontal = ['informed']
    inlines = [ServiceActivityInline]
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'description']
        }),
        ('Pricing', {
            'fields': ['service_price', 'regulator_fee']
        }),
        ('Responsibilities', {
            'fields': ['executor', 'counterparty_name']
        }),
        ('Relationships', {
            'fields': ['relationship_structure', 'informed']
        }),
        ('Metadata', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

    def total_cost_display(self, obj):
        return obj.get_total_cost()
    total_cost_display.short_description = 'Total Cost'


@admin.register(ServiceActivity)
class ServiceActivityAdmin(admin.ModelAdmin):
    list_display = ['service', 'order', 'name', 'status', 'updated_at']
    list_filter = ['status', 'service']
    search_fields = ['name', 'service__name']
    list_select_related = ['service']
    ordering = ['service', 'order']


@admin.register(WebhookLog)
class WebhookLogAdmin(admin.ModelAdmin):
    list_display = [
        'event_type', 
        'status', 
        'response_status_code',
        'attempt_count',
        'created_at',
        'last_attempt_at'
    ]
    list_filter = [
        'status', 
        'event_type', 
        'response_status_code',
        'created_at'
    ]
    search_fields = ['event_type', 'url', 'error_message']
    readonly_fields = [
        'created_at', 
        'last_attempt_at', 
        'response_status_code',
        'response_body'
    ]

    fieldsets = [
        ('Event Information', {
            'fields': ['event_type', 'payload', 'url']
        }),
        ('Status', {
            'fields': ['status', 'attempt_count']
        }),
        ('Response', {
            'fields': [
                'response_status_code', 
                'response_body', 
                'error_message'
            ],
            'classes': ['collapse']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'last_attempt_at'],
            'classes': ['collapse']
        }),
    ]

    def has_add_permission(self, request):
        # WebhookLog é apenas para leitura - criado automaticamente
        return False

