# Corporate Admin Configuration
# This file imports the improved admin interface for the SIRIUS system

# Temporarily disable improved admin due to ValidationRule inline issue
# try:
#     # Import the improved admin - this provides enhanced UX features
#     from .admin_improved import *
#     print("✅ Admin melhorado carregado com sucesso!")
# except ImportError as e:
#     print(f"⚠️ Admin melhorado não encontrado: {e}")

# Use basic admin for now
from django.contrib import admin
from .models import Entity, Structure, EntityOwnership, ValidationRule, StructureNode, NodeOwnership

# Basic admin registration with some improvements
@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ['name', 'entity_type', 'jurisdiction', 'active']
    list_filter = ['entity_type', 'jurisdiction', 'active']
    search_fields = ['name']
    
    class Media:
        css = {
            'all': ('admin/css/structure_admin_improved.css',)
        }
        js = ('admin/js/structure_admin_improved.js',)

@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description']
    
    class Media:
        css = {
            'all': ('admin/css/structure_admin_improved.css',)
        }
        js = ('admin/js/structure_admin_improved.js',)

@admin.register(EntityOwnership)
class EntityOwnershipAdmin(admin.ModelAdmin):
    list_display = ['structure', 'owned_entity', 'ownership_percentage']
    list_filter = ['structure', 'owned_entity']
    search_fields = ['structure__name', 'owned_entity__name']

@admin.register(ValidationRule)
class ValidationRuleAdmin(admin.ModelAdmin):
    list_display = ['description', 'relationship_type', 'severity', 'active']
    list_filter = ['relationship_type', 'severity', 'active']
    search_fields = ['description', 'tax_impacts']

@admin.register(StructureNode)
class StructureNodeAdmin(admin.ModelAdmin):
    list_display = ['custom_name', 'entity_template', 'structure', 'level', 'is_active']
    list_filter = ['structure', 'entity_template', 'level', 'is_active']
    search_fields = ['custom_name', 'entity_template__name', 'structure__name']
    ordering = ['structure', 'level', 'custom_name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('structure', 'entity_template', 'custom_name')
        }),
        ('Instance Configuration', {
            'fields': ('total_shares', 'corporate_name', 'hash_number')
        }),
        ('Hierarchy', {
            'fields': ('parent_node', 'level')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(NodeOwnership)
class NodeOwnershipAdmin(admin.ModelAdmin):
    list_display = ['get_owner_name', 'owned_node', 'ownership_percentage', 'structure']
    list_filter = ['structure', 'owned_node__entity_template']
    search_fields = ['owned_node__custom_name', 'owner_party__name', 'owner_node__custom_name']
    
    def get_owner_name(self, obj):
        if obj.owner_party:
            return f"🧑 {obj.owner_party.name}"
        elif obj.owner_node:
            return f"🏢 {obj.owner_node.custom_name}"
        return "Unknown"
    get_owner_name.short_description = "Owner"
    
    fieldsets = (
        ('Ownership Relationship', {
            'fields': ('structure', 'owner_party', 'owner_node', 'owned_node')
        }),
        ('Ownership Details', {
            'fields': ('ownership_percentage', 'owned_shares', 'share_value_usd')
        }),
    )

print("📋 Admin básico carregado com CSS/JS melhorado")
