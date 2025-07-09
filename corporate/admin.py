from django.contrib import admin
from .models import (
    Entity, Structure, EntityOwnership, ValidationRule
)


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'entity_type', 'jurisdiction', 'total_shares', 'active'
    ]
    list_filter = ['entity_type', 'jurisdiction', 'active', 'created_at']
    search_fields = ['name', 'tax_classification']
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'entity_type', 'tax_classification']
        }),
        ('Jurisdiction', {
            'fields': ['jurisdiction', 'us_state', 'br_state']
        }),
        ('Shares', {
            'fields': ['total_shares']
        }),
        ('Implementation', {
            'fields': ['implementation_templates', 'implementation_time', 'complexity']
        }),
        ('Tax Information', {
            'fields': ['tax_impact_usa', 'tax_impact_brazil', 'tax_impact_others'],
            'classes': ['collapse']
        }),
        ('Privacy & Protection', {
            'fields': ['confidentiality_level', 'asset_protection', 'privacy_impact', 'privacy_score'],
            'classes': ['collapse']
        }),
        ('Banking & Compliance', {
            'fields': ['banking_relation_score', 'compliance_score', 'banking_facility'],
            'classes': ['collapse']
        }),
        ('Documentation', {
            'fields': ['required_documentation', 'documents_url', 'required_forms_usa', 'required_forms_brazil'],
            'classes': ['collapse']
        }),
        ('Status', {
            'fields': ['active']
        }),
    ]
    ordering = ['name']


@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'status', 'get_entities_count', 'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description']
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'description', 'status']
        }),
        ('Calculated Fields', {
            'fields': ['tax_impacts', 'severity_levels'],
            'classes': ['collapse'],
            'description': 'These fields are automatically calculated from validation rules'
        }),
    ]
    ordering = ['-created_at']
    
    # Add custom CSS and JS for status colors
    class Media:
        css = {
            'all': ('admin/css/structure_status_colors.css',)
        }
        js = ('admin/js/structure_status_colors.js',)

    def get_entities_count(self, obj):
        return obj.entity_ownerships.count()
    get_entities_count.short_description = 'Entities'


@admin.register(EntityOwnership)
class EntityOwnershipAdmin(admin.ModelAdmin):
    list_display = [
        'structure', 'get_owner_name', 'owned_entity', 'ownership_percentage', 'owned_shares'
    ]
    list_filter = ['structure', 'owned_entity', 'created_at']
    search_fields = ['structure__name', 'owned_entity__name', 'corporate_name']
    fieldsets = [
        ('Basic Information', {
            'fields': ['structure', 'owned_entity']
        }),
        ('Owner', {
            'fields': ['owner_ubo', 'owner_entity'],
            'description': 'Select either UBO or Entity as owner (not both)'
        }),
        ('Corporate Identity', {
            'fields': ['corporate_name', 'hash_number'],
            'description': 'At least one of these fields must be filled'
        }),
        ('Ownership', {
            'fields': ['owned_shares', 'ownership_percentage'],
            'description': 'Fill either shares or percentage - the other will be calculated automatically'
        }),
        ('Share Valuation', {
            'fields': ['share_value_usd', 'share_value_eur', 'total_value_usd', 'total_value_eur'],
            'classes': ['collapse'],
            'description': 'Total values are calculated automatically'
        }),
    ]
    ordering = ['structure', 'owned_entity']

    def get_owner_name(self, obj):
        if obj.owner_ubo:
            return str(obj.owner_ubo)
        elif obj.owner_entity:
            return str(obj.owner_entity)
        return "No owner"
    get_owner_name.short_description = 'Owner'


@admin.register(ValidationRule)
class ValidationRuleAdmin(admin.ModelAdmin):
    list_display = [
        'parent_entity', 'related_entity', 'relationship_type', 'severity'
    ]
    list_filter = ['relationship_type', 'severity', 'created_at']
    search_fields = ['parent_entity__name', 'related_entity__name', 'description']
    fieldsets = [
        ('Entities', {
            'fields': ['parent_entity', 'related_entity']
        }),
        ('Relationship', {
            'fields': ['relationship_type', 'severity', 'description']
        }),
        ('Tax Information', {
            'fields': ['tax_impacts'],
            'description': 'Detailed tax implications of this entity combination'
        }),
    ]
    ordering = ['parent_entity', 'related_entity']

