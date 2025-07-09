from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import models
from django.forms import TextInput, Textarea

from .models import Entity, Structure, EntityOwnership, MasterEntity, ValidationRule
from .admin_actions import get_structure_admin_actions, get_entity_admin_actions, get_ownership_admin_actions
from .views import structure_wizard_view


class EntityOwnershipInline(admin.TabularInline):
    """Improved inline for EntityOwnership with better UX"""
    model = EntityOwnership
    extra = 0
    min_num = 0
    
    fields = [
        'owner_display', 'owned_entity', 'percentage', 'shares', 
        'corporate_name', 'hash_number', 'share_value_usd', 'share_value_eur',
        'validation_status'
    ]
    readonly_fields = ['owner_display', 'validation_status']
    
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 40})},
        models.DecimalField: {'widget': TextInput(attrs={'size': '10'})},
    }
    
    def owner_display(self, obj):
        """Display owner information with icon"""
        if obj.owner_ubo:
            return format_html('👤 {}', obj.owner_ubo.name)
        elif obj.owner_entity:
            return format_html('🏢 {}', obj.owner_entity.name)
        return '❓ Unknown'
    owner_display.short_description = 'Owner'
    
    def validation_status(self, obj):
        """Show validation status with visual indicator"""
        if not obj.percentage:
            return format_html('<span style="color: #dc3545;">❌ No percentage</span>')
        
        # Get total percentage for this entity
        total_percentage = EntityOwnership.objects.filter(
            owned_entity=obj.owned_entity,
            structure=obj.structure
        ).aggregate(
            total=models.Sum('percentage')
        )['total'] or 0
        
        if total_percentage == 100:
            return format_html('<span style="color: #28a745;">✅ Valid</span>')
        elif total_percentage > 100:
            return format_html('<span style="color: #dc3545;">❌ Over-owned</span>')
        else:
            return format_html('<span style="color: #ffc107;">⚠️ Under-owned</span>')
    validation_status.short_description = 'Status'
    
    class Media:
        css = {
            'all': ('admin/css/structure_admin_improved.css',)
        }
        js = ('admin/js/structure_admin_improved.js',)


@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    """Improved Structure admin with enhanced UX"""
    
    list_display = [
        'name_with_icon', 'status_badge', 'entities_count', 
        'completion_percentage', 'created_at', 'action_buttons'
    ]
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    
    fieldsets = (
        ('📋 Basic Information', {
            'fields': ('name', 'description', 'status'),
            'classes': ('wide',)
        }),
        ('📊 Ownership Structure', {
            'fields': ('ownership_summary',),
            'classes': ('wide', 'collapse'),
            'description': 'Visual representation of the ownership structure'
        }),
        ('📈 Validation & Metrics', {
            'fields': ('validation_summary', 'tax_impacts_summary'),
            'classes': ('wide', 'collapse'),
            'description': 'Validation results and calculated metrics'
        }),
    )
    
    readonly_fields = ['ownership_summary', 'validation_summary', 'tax_impacts_summary']
    
    inlines = [EntityOwnershipInline]
    
    actions = get_structure_admin_actions()
    
    def get_urls(self):
        """Add custom URLs for wizard and other features"""
        urls = super().get_urls()
        custom_urls = [
            path(
                'wizard/',
                self.admin_site.admin_view(structure_wizard_view),
                name='corporate_structure_wizard'
            ),
        ]
        return custom_urls + urls
    
    def name_with_icon(self, obj):
        """Display name with appropriate icon"""
        status_icons = {
            'drafting': '📝',
            'sent_for_approval': '📤',
            'approved': '✅',
            'rejected': '❌'
        }
        icon = status_icons.get(obj.status, '📋')
        return format_html('{} {}', icon, obj.name)
    name_with_icon.short_description = 'Structure Name'
    name_with_icon.admin_order_field = 'name'
    
    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'drafting': '#6c757d',
            'sent_for_approval': '#ffc107',
            'approved': '#28a745',
            'rejected': '#dc3545'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def entities_count(self, obj):
        """Count of entities in this structure"""
        count = EntityOwnership.objects.filter(structure=obj).values('owned_entity').distinct().count()
        return format_html('🏢 {}', count)
    entities_count.short_description = 'Entities'
    
    def completion_percentage(self, obj):
        """Show completion percentage with progress bar"""
        ownerships = EntityOwnership.objects.filter(structure=obj)
        if not ownerships.exists():
            return format_html('<span style="color: #dc3545;">0%</span>')
        
        # Calculate completion
        entity_totals = {}
        for ownership in ownerships:
            entity_id = ownership.owned_entity_id
            if entity_id not in entity_totals:
                entity_totals[entity_id] = 0
            entity_totals[entity_id] += ownership.percentage or 0
        
        complete_entities = sum(1 for total in entity_totals.values() if total == 100)
        total_entities = len(entity_totals)
        
        if total_entities == 0:
            percentage = 0
        else:
            percentage = (complete_entities / total_entities) * 100
        
        color = '#28a745' if percentage == 100 else '#ffc107' if percentage > 0 else '#dc3545'
        
        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">'
            '<div style="width: 60px; height: 8px; background: #e9ecef; border-radius: 4px; overflow: hidden;">'
            '<div style="width: {}%; height: 100%; background: {}; transition: width 0.3s ease;"></div>'
            '</div>'
            '<span style="color: {}; font-weight: bold;">{:.0f}%</span>'
            '</div>',
            percentage, color, color, percentage
        )
    completion_percentage.short_description = 'Completion'
    
    def action_buttons(self, obj):
        """Action buttons for quick operations"""
        buttons = []
        
        # Wizard button
        wizard_url = reverse('admin:corporate_structure_wizard')
        buttons.append(
            f'<a href="{wizard_url}?structure_id={obj.id}" '
            f'style="background: #667eea; color: white; padding: 4px 8px; '
            f'border-radius: 4px; text-decoration: none; font-size: 11px; margin-right: 4px;">'
            f'🧙‍♂️ Wizard</a>'
        )
        
        # Validate button
        buttons.append(
            f'<a href="#" onclick="validateStructure({obj.id})" '
            f'style="background: #28a745; color: white; padding: 4px 8px; '
            f'border-radius: 4px; text-decoration: none; font-size: 11px; margin-right: 4px;">'
            f'✅ Validate</a>'
        )
        
        return format_html(''.join(buttons))
    action_buttons.short_description = 'Actions'
    
    def ownership_summary(self, obj):
        """Visual ownership summary"""
        ownerships = EntityOwnership.objects.filter(structure=obj).select_related(
            'owned_entity', 'owner_ubo', 'owner_entity'
        )
        
        if not ownerships.exists():
            return format_html(
                '<div style="text-align: center; padding: 20px; color: #666;">'
                '📋 No ownership relationships defined<br>'
                '<small>Use the wizard to create ownership structure</small>'
                '</div>'
            )
        
        # Group by entity
        entity_groups = {}
        for ownership in ownerships:
            entity_id = ownership.owned_entity_id
            if entity_id not in entity_groups:
                entity_groups[entity_id] = {
                    'entity': ownership.owned_entity,
                    'ownerships': [],
                    'total_percentage': 0
                }
            entity_groups[entity_id]['ownerships'].append(ownership)
            entity_groups[entity_id]['total_percentage'] += ownership.percentage or 0
        
        html_parts = ['<div style="max-height: 400px; overflow-y: auto;">']
        
        for group in entity_groups.values():
            entity = group['entity']
            total = group['total_percentage']
            
            # Entity header
            status_color = '#28a745' if total == 100 else '#ffc107' if total < 100 else '#dc3545'
            html_parts.append(
                f'<div style="border: 1px solid #e9ecef; border-radius: 8px; '
                f'margin-bottom: 15px; padding: 15px; background: #f8f9fa;">'
                f'<div style="display: flex; justify-content: space-between; align-items: center; '
                f'margin-bottom: 10px; padding-bottom: 8px; border-bottom: 1px solid #dee2e6;">'
                f'<strong>🏢 {entity.name}</strong>'
                f'<span style="background: {status_color}; color: white; padding: 2px 8px; '
                f'border-radius: 10px; font-size: 11px; font-weight: bold;">{total:.1f}%</span>'
                f'</div>'
            )
            
            # Ownership bars
            for ownership in group['ownerships']:
                owner_name = ownership.owner_ubo.name if ownership.owner_ubo else (
                    ownership.owner_entity.name if ownership.owner_entity else 'Unknown'
                )
                owner_icon = '👤' if ownership.owner_ubo else '🏢'
                percentage = ownership.percentage or 0
                
                html_parts.append(
                    f'<div style="display: flex; align-items: center; margin-bottom: 5px;">'
                    f'<div style="min-width: 120px; font-size: 12px;">{owner_icon} {owner_name}</div>'
                    f'<div style="flex: 1; height: 16px; background: #e9ecef; border-radius: 8px; '
                    f'margin: 0 10px; position: relative; overflow: hidden;">'
                    f'<div style="width: {min(percentage, 100)}%; height: 100%; background: {status_color}; '
                    f'border-radius: 8px; transition: width 0.3s ease;"></div>'
                    f'<div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); '
                    f'color: white; font-size: 10px; font-weight: bold; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">'
                    f'{percentage:.1f}%</div>'
                    f'</div>'
                    f'<div style="min-width: 50px; text-align: right; font-size: 12px; font-weight: bold;">'
                    f'{percentage:.1f}%</div>'
                    f'</div>'
                )
            
            html_parts.append('</div>')
        
        html_parts.append('</div>')
        
        return format_html(''.join(html_parts))
    ownership_summary.short_description = 'Ownership Structure'
    
    def validation_summary(self, obj):
        """Validation summary with metrics"""
        ownerships = EntityOwnership.objects.filter(structure=obj)
        
        if not ownerships.exists():
            return format_html(
                '<div style="color: #dc3545;">❌ No ownerships to validate</div>'
            )
        
        # Calculate validation metrics
        entity_totals = {}
        for ownership in ownerships:
            entity_id = ownership.owned_entity_id
            if entity_id not in entity_totals:
                entity_totals[entity_id] = {'entity': ownership.owned_entity, 'total': 0}
            entity_totals[entity_id]['total'] += ownership.percentage or 0
        
        complete = sum(1 for data in entity_totals.values() if data['total'] == 100)
        incomplete = sum(1 for data in entity_totals.values() if data['total'] < 100)
        over = sum(1 for data in entity_totals.values() if data['total'] > 100)
        total = len(entity_totals)
        
        return format_html(
            '<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; '
            'text-align: center; font-size: 12px;">'
            '<div><div style="font-size: 18px; font-weight: bold; color: #333;">{}</div>'
            '<div style="color: #666;">Total</div></div>'
            '<div><div style="font-size: 18px; font-weight: bold; color: #28a745;">{}</div>'
            '<div style="color: #666;">Complete</div></div>'
            '<div><div style="font-size: 18px; font-weight: bold; color: #ffc107;">{}</div>'
            '<div style="color: #666;">Incomplete</div></div>'
            '<div><div style="font-size: 18px; font-weight: bold; color: #dc3545;">{}</div>'
            '<div style="color: #666;">Over-owned</div></div>'
            '</div>',
            total, complete, incomplete, over
        )
    validation_summary.short_description = 'Validation Summary'
    
    def tax_impacts_summary(self, obj):
        """Tax impacts summary"""
        # This would calculate tax impacts based on the structure
        return format_html(
            '<div style="color: #666; font-style: italic;">Tax impact calculation not implemented yet</div>'
        )
    tax_impacts_summary.short_description = 'Tax Impacts'
    
    class Media:
        css = {
            'all': (
                'admin/css/structure_admin_improved.css',
                'admin/css/ownership_matrix.css',
                'admin/css/structure_wizard.css',
            )
        }
        js = (
            'admin/js/structure_admin_improved.js',
            'admin/js/structure_wizard.js',
        )


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    """Improved Entity admin"""
    
    list_display = [
        'name_with_icon', 'entity_type', 'jurisdiction', 
        'ownership_status', 'structures_count', 'total_shares'
    ]
    list_filter = ['entity_type', 'jurisdiction', 'created_at']
    search_fields = ['name', 'entity_type', 'jurisdiction']
    ordering = ['name']
    
    fieldsets = (
        ('🏢 Entity Information', {
            'fields': ('name', 'entity_type', 'jurisdiction'),
            'classes': ('wide',)
        }),
        ('📊 Share Information', {
            'fields': ('total_shares', 'share_currency'),
            'classes': ('wide',)
        }),
        ('📈 Ownership Summary', {
            'fields': ('ownership_breakdown',),
            'classes': ('wide', 'collapse'),
            'description': 'Current ownership breakdown for this entity'
        }),
    )
    
    readonly_fields = ['ownership_breakdown']
    
    actions = get_entity_admin_actions()
    
    def name_with_icon(self, obj):
        """Display name with entity type icon"""
        type_icons = {
            'Corporation': '🏢',
            'LLC': '🏛️',
            'Partnership': '🤝',
            'Trust': '🛡️',
            'Foundation': '🏛️'
        }
        icon = type_icons.get(obj.entity_type, '🏢')
        return format_html('{} {}', icon, obj.name)
    name_with_icon.short_description = 'Entity Name'
    name_with_icon.admin_order_field = 'name'
    
    def ownership_status(self, obj):
        """Show ownership completion status"""
        total_percentage = EntityOwnership.objects.filter(
            owned_entity=obj
        ).aggregate(total=models.Sum('percentage'))['total'] or 0
        
        if total_percentage == 100:
            return format_html('<span style="color: #28a745;">✅ Complete</span>')
        elif total_percentage > 100:
            return format_html('<span style="color: #dc3545;">❌ Over-owned</span>')
        elif total_percentage > 0:
            return format_html('<span style="color: #ffc107;">⚠️ Partial</span>')
        else:
            return format_html('<span style="color: #6c757d;">➖ None</span>')
    ownership_status.short_description = 'Ownership'
    
    def structures_count(self, obj):
        """Count of structures this entity belongs to"""
        count = EntityOwnership.objects.filter(owned_entity=obj).values('structure').distinct().count()
        return format_html('🏗️ {}', count)
    structures_count.short_description = 'Structures'
    
    def ownership_breakdown(self, obj):
        """Detailed ownership breakdown"""
        ownerships = EntityOwnership.objects.filter(owned_entity=obj).select_related(
            'owner_ubo', 'owner_entity', 'structure'
        )
        
        if not ownerships.exists():
            return format_html(
                '<div style="text-align: center; padding: 20px; color: #666;">'
                '📋 No ownership relationships<br>'
                '<small>This entity is not owned by anyone yet</small>'
                '</div>'
            )
        
        total_percentage = sum(o.percentage or 0 for o in ownerships)
        
        html_parts = [
            f'<div style="margin-bottom: 15px; padding: 10px; background: #f8f9fa; '
            f'border-radius: 6px; text-align: center;">'
            f'<strong>Total Ownership: {total_percentage:.1f}%</strong>'
            f'</div>'
        ]
        
        for ownership in ownerships:
            owner_name = ownership.owner_ubo.name if ownership.owner_ubo else (
                ownership.owner_entity.name if ownership.owner_entity else 'Unknown'
            )
            owner_icon = '👤' if ownership.owner_ubo else '🏢'
            percentage = ownership.percentage or 0
            
            html_parts.append(
                f'<div style="display: flex; justify-content: space-between; align-items: center; '
                f'padding: 8px; margin-bottom: 5px; background: white; border-radius: 4px; '
                f'border: 1px solid #e9ecef;">'
                f'<div>{owner_icon} {owner_name}</div>'
                f'<div style="font-weight: bold;">{percentage:.1f}%</div>'
                f'</div>'
            )
        
        return format_html(''.join(html_parts))
    ownership_breakdown.short_description = 'Ownership Breakdown'


@admin.register(EntityOwnership)
class EntityOwnershipAdmin(admin.ModelAdmin):
    """Improved EntityOwnership admin"""
    
    list_display = [
        'ownership_display', 'percentage_bar', 'shares_display', 
        'corporate_name', 'structure_link', 'validation_status'
    ]
    list_filter = ['structure', 'owned_entity__entity_type', 'created_at']
    search_fields = [
        'owned_entity__name', 'owner_ubo__name', 'owner_entity__name',
        'corporate_name', 'hash_number'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('👥 Ownership Relationship', {
            'fields': ('structure', 'owned_entity', 'owner_ubo', 'owner_entity'),
            'classes': ('wide',)
        }),
        ('📊 Ownership Details', {
            'fields': ('percentage', 'shares', 'corporate_name', 'hash_number'),
            'classes': ('wide',)
        }),
        ('💰 Share Values', {
            'fields': ('share_value_usd', 'share_value_eur'),
            'classes': ('wide',)
        }),
    )
    
    actions = get_ownership_admin_actions()
    
    def ownership_display(self, obj):
        """Display ownership relationship"""
        owner_name = obj.owner_ubo.name if obj.owner_ubo else (
            obj.owner_entity.name if obj.owner_entity else 'Unknown'
        )
        owner_icon = '👤' if obj.owner_ubo else '🏢'
        
        return format_html(
            '{} {} → 🏢 {}',
            owner_icon, owner_name, obj.owned_entity.name
        )
    ownership_display.short_description = 'Ownership'
    
    def percentage_bar(self, obj):
        """Visual percentage bar"""
        percentage = obj.percentage or 0
        color = '#28a745' if percentage == 100 else '#ffc107' if percentage > 0 else '#dc3545'
        
        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">'
            '<div style="width: 80px; height: 12px; background: #e9ecef; border-radius: 6px; overflow: hidden;">'
            '<div style="width: {}%; height: 100%; background: {}; transition: width 0.3s ease;"></div>'
            '</div>'
            '<span style="font-weight: bold; color: {};">{:.1f}%</span>'
            '</div>',
            min(percentage, 100), color, color, percentage
        )
    percentage_bar.short_description = 'Percentage'
    percentage_bar.admin_order_field = 'percentage'
    
    def shares_display(self, obj):
        """Display shares with formatting"""
        if obj.shares:
            return format_html('📊 {:,}', obj.shares)
        return '➖'
    shares_display.short_description = 'Shares'
    shares_display.admin_order_field = 'shares'
    
    def structure_link(self, obj):
        """Link to structure"""
        url = reverse('admin:corporate_structure_change', args=[obj.structure.id])
        return format_html('<a href="{}" style="color: #667eea;">🏗️ {}</a>', url, obj.structure.name)
    structure_link.short_description = 'Structure'
    
    def validation_status(self, obj):
        """Validation status for this ownership"""
        if not obj.percentage:
            return format_html('<span style="color: #dc3545;">❌ No %</span>')
        
        # Check entity total
        total_percentage = EntityOwnership.objects.filter(
            owned_entity=obj.owned_entity,
            structure=obj.structure
        ).aggregate(total=models.Sum('percentage'))['total'] or 0
        
        if total_percentage == 100:
            return format_html('<span style="color: #28a745;">✅ Valid</span>')
        elif total_percentage > 100:
            return format_html('<span style="color: #dc3545;">❌ Over</span>')
        else:
            return format_html('<span style="color: #ffc107;">⚠️ Under</span>')
    validation_status.short_description = 'Status'


@admin.register(MasterEntity)
class MasterEntityAdmin(admin.ModelAdmin):
    """Admin for MasterEntity"""
    list_display = ['entity', 'is_root', 'created_at']
    list_filter = ['is_root', 'created_at']
    search_fields = ['entity__name']


@admin.register(ValidationRule)
class ValidationRuleAdmin(admin.ModelAdmin):
    """Admin for ValidationRule"""
    list_display = ['name', 'rule_type', 'is_active', 'severity']
    list_filter = ['rule_type', 'is_active', 'severity']
    search_fields = ['name', 'description']

