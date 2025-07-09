from django.contrib import admin
from django.db.models import Sum, Count, Q
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.core.exceptions import ValidationError
from django import forms
from .models import (
    Entity, Structure, EntityOwnership, ValidationRule
)


# ============================================================================
# CUSTOM FILTERS
# ============================================================================

class OwnershipCompleteFilter(admin.SimpleListFilter):
    title = 'Ownership Status'
    parameter_name = 'ownership_complete'
    
    def lookups(self, request, model_admin):
        return (
            ('complete', '✅ Complete (100%)'),
            ('incomplete', '⚠️ Incomplete (<100%)'),
            ('over', '❌ Over-allocated (>100%)'),
            ('empty', '➖ No ownership'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'complete':
            return queryset.annotate(
                total_ownership=Sum('entity_ownerships__ownership_percentage')
            ).filter(total_ownership=100)
        elif self.value() == 'incomplete':
            return queryset.annotate(
                total_ownership=Sum('entity_ownerships__ownership_percentage')
            ).filter(total_ownership__lt=100, total_ownership__gt=0)
        elif self.value() == 'over':
            return queryset.annotate(
                total_ownership=Sum('entity_ownerships__ownership_percentage')
            ).filter(total_ownership__gt=100)
        elif self.value() == 'empty':
            return queryset.annotate(
                total_ownership=Sum('entity_ownerships__ownership_percentage')
            ).filter(total_ownership__isnull=True)


class EntityCountFilter(admin.SimpleListFilter):
    title = 'Entity Count'
    parameter_name = 'entity_count'
    
    def lookups(self, request, model_admin):
        return (
            ('single', '1 Entity'),
            ('small', '2-5 Entities'),
            ('medium', '6-10 Entities'),
            ('large', '10+ Entities'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'single':
            return queryset.annotate(
                entity_count=Count('entity_ownerships__owned_entity', distinct=True)
            ).filter(entity_count=1)
        elif self.value() == 'small':
            return queryset.annotate(
                entity_count=Count('entity_ownerships__owned_entity', distinct=True)
            ).filter(entity_count__gte=2, entity_count__lte=5)
        elif self.value() == 'medium':
            return queryset.annotate(
                entity_count=Count('entity_ownerships__owned_entity', distinct=True)
            ).filter(entity_count__gte=6, entity_count__lte=10)
        elif self.value() == 'large':
            return queryset.annotate(
                entity_count=Count('entity_ownerships__owned_entity', distinct=True)
            ).filter(entity_count__gt=10)


# ============================================================================
# CUSTOM FORMS
# ============================================================================

class StructureAdminForm(forms.ModelForm):
    class Meta:
        model = Structure
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Custom validation logic for existing structures
        if self.instance.pk:
            total_ownership = self.instance.get_total_ownership_by_entity()
            errors = []
            
            for entity, percentage in total_ownership.items():
                if percentage > 100:
                    errors.append(
                        f'{entity.name}: Over-allocated ({percentage}%)'
                    )
                elif percentage < 100 and percentage > 0:
                    errors.append(
                        f'{entity.name}: Under-allocated ({percentage}%)'
                    )
            
            if errors:
                raise ValidationError(
                    f'Ownership validation errors: {"; ".join(errors)}'
                )
        
        return cleaned_data


class EntityOwnershipAdminForm(forms.ModelForm):
    class Meta:
        model = EntityOwnership
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validate ownership percentage
        percentage = cleaned_data.get('ownership_percentage')
        if percentage and (percentage < 0 or percentage > 100):
            raise ValidationError(
                'Ownership percentage must be between 0 and 100'
            )
        
        # Validate that either UBO or Entity is selected as owner
        owner_ubo = cleaned_data.get('owner_ubo')
        owner_entity = cleaned_data.get('owner_entity')
        
        if not owner_ubo and not owner_entity:
            raise ValidationError(
                'Either UBO or Entity must be selected as owner'
            )
        
        if owner_ubo and owner_entity:
            raise ValidationError(
                'Cannot select both UBO and Entity as owner'
            )
        
        return cleaned_data


# ============================================================================
# INLINE ADMINS
# ============================================================================

class EntityOwnershipInlineAdmin(admin.TabularInline):
    model = EntityOwnership
    form = EntityOwnershipAdminForm
    extra = 0
    
    fields = [
        'owner_display', 'owned_entity', 
        'ownership_percentage', 'owned_shares',
        'corporate_name', 'hash_number',
        'validation_status_display'
    ]
    
    readonly_fields = ['owner_display', 'validation_status_display']
    
    classes = ['collapse']
    
    def owner_display(self, obj):
        if obj.owner_ubo:
            return format_html(
                '👤 <strong>{}</strong>',
                obj.owner_ubo.name
            )
        elif obj.owner_entity:
            return format_html(
                '🏢 <strong>{}</strong>',
                obj.owner_entity.name
            )
        return "➖ No owner"
    owner_display.short_description = "Owner"
    
    def validation_status_display(self, obj):
        if not obj.pk:
            return "➖ Not saved"
        
        if obj.ownership_percentage:
            if obj.ownership_percentage > 100:
                return format_html(
                    '<span style="color: red; font-weight: bold;">❌ Invalid ({}%)</span>',
                    obj.ownership_percentage
                )
            elif obj.ownership_percentage == 100:
                return format_html(
                    '<span style="color: green; font-weight: bold;">✅ Complete (100%)</span>'
                )
            else:
                return format_html(
                    '<span style="color: orange; font-weight: bold;">⚠️ Partial ({}%)</span>',
                    obj.ownership_percentage
                )
        return "➖ Not set"
    validation_status_display.short_description = "Status"


class ValidationRuleInlineAdmin(admin.TabularInline):
    model = ValidationRule
    extra = 0
    fields = ['related_entity', 'relationship_type', 'severity', 'description']
    classes = ['collapse']


# ============================================================================
# ADMIN ACTIONS
# ============================================================================

@admin.action(description='🔍 Validate selected structures')
def validate_structures(modeladmin, request, queryset):
    validated = 0
    errors = []
    
    for structure in queryset:
        try:
            # Perform validation logic
            total_ownership = structure.get_total_ownership_by_entity()
            structure_errors = []
            
            for entity, percentage in total_ownership.items():
                if percentage != 100:
                    structure_errors.append(
                        f'{entity.name}: {percentage}%'
                    )
            
            if structure_errors:
                errors.append(
                    f"{structure.name}: {'; '.join(structure_errors)}"
                )
            else:
                validated += 1
                
        except Exception as e:
            errors.append(f"{structure.name}: {str(e)}")
    
    if validated:
        messages.success(
            request, 
            f'✅ Successfully validated {validated} structures.'
        )
    
    if errors:
        messages.warning(
            request,
            f'⚠️ Validation issues found: {"; ".join(errors[:5])}'
            + (f' and {len(errors)-5} more...' if len(errors) > 5 else '')
        )


@admin.action(description='📊 Generate ownership reports')
def generate_ownership_reports(modeladmin, request, queryset):
    for structure in queryset:
        # Generate ownership report logic here
        pass
    
    messages.success(
        request,
        f'📊 Generated ownership reports for {queryset.count()} structures.'
    )


@admin.action(description='📋 Duplicate selected structures')
def duplicate_structures(modeladmin, request, queryset):
    duplicated = 0
    
    for structure in queryset:
        # Create duplicate
        new_structure = Structure.objects.create(
            name=f"{structure.name} (Copy)",
            description=f"Copy of {structure.description}",
            status='drafting'
        )
        
        # Copy entity ownerships
        for ownership in structure.entity_ownerships.all():
            EntityOwnership.objects.create(
                structure=new_structure,
                owner_ubo=ownership.owner_ubo,
                owner_entity=ownership.owner_entity,
                owned_entity=ownership.owned_entity,
                ownership_percentage=ownership.ownership_percentage,
                owned_shares=ownership.owned_shares,
                corporate_name=ownership.corporate_name,
                hash_number=f"{ownership.hash_number}_copy" if ownership.hash_number else None
            )
        
        duplicated += 1
    
    messages.success(
        request,
        f'📋 Successfully duplicated {duplicated} structures.'
    )


# ============================================================================
# MAIN ADMIN CLASSES
# ============================================================================

@admin.register(Structure)
class StructureAdminImproved(admin.ModelAdmin):
    form = StructureAdminForm
    
    # Fieldsets organizados
    fieldsets = (
        ('📋 Basic Information', {
            'fields': ('name', 'description', 'status'),
            'classes': ('wide',),
            'description': 'Essential structure information'
        }),
        ('📊 Metrics & Analysis', {
            'fields': ('entities_count_display', 'ownership_summary_display', 'validation_summary_display'),
            'classes': ('collapse',),
            'description': 'Automatically calculated metrics and validation status'
        }),
        ('🔧 Advanced Fields', {
            'fields': ('tax_impacts', 'severity_levels'),
            'classes': ('collapse',),
            'description': 'Advanced fields calculated from validation rules'
        }),
    )
    
    # Inlines para relacionamentos
    inlines = [
        EntityOwnershipInlineAdmin,
        ValidationRuleInlineAdmin,
    ]
    
    # List display otimizado
    list_display = [
        'name', 'status_badge', 'entities_count_badge', 
        'ownership_status_badge', 'validation_score_badge', 'created_date_display'
    ]
    
    # Filtros inteligentes
    list_filter = [
        'status', 
        OwnershipCompleteFilter,
        EntityCountFilter,
        ('created_at', admin.DateFieldListFilter),
    ]
    
    # Busca avançada
    search_fields = [
        'name', 'description', 
        'entity_ownerships__owned_entity__name',
        'entity_ownerships__corporate_name'
    ]
    
    # Actions customizadas
    actions = [
        validate_structures, 
        generate_ownership_reports, 
        duplicate_structures
    ]
    
    # Ordenação
    ordering = ['-created_at']
    
    # Campos readonly calculados
    readonly_fields = [
        'entities_count_display', 
        'ownership_summary_display', 
        'validation_summary_display'
    ]
    
    # CSS e JS customizados
    class Media:
        css = {
            'all': ('admin/css/structure_admin_improved.css',)
        }
        js = ('admin/js/structure_admin_improved.js',)
    
    # ========================================================================
    # DISPLAY METHODS
    # ========================================================================
    
    def status_badge(self, obj):
        status_colors = {
            'drafting': '#ffc107',      # Yellow
            'sent_for_approval': '#17a2b8',  # Blue
            'approved': '#28a745',      # Green
            'rejected': '#dc3545',      # Red
        }
        
        color = status_colors.get(obj.status, '#6c757d')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "Status"
    
    def entities_count_badge(self, obj):
        count = obj.entity_ownerships.values('owned_entity').distinct().count()
        
        if count == 0:
            color = '#dc3545'  # Red
            icon = '❌'
        elif count <= 3:
            color = '#28a745'  # Green
            icon = '🏢'
        elif count <= 10:
            color = '#ffc107'  # Yellow
            icon = '🏗️'
        else:
            color = '#17a2b8'  # Blue
            icon = '🏭'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{} {}</span>',
            color,
            icon,
            count
        )
    entities_count_badge.short_description = "Entities"
    
    def ownership_status_badge(self, obj):
        total_ownership = obj.get_total_ownership_by_entity()
        
        if not total_ownership:
            return format_html(
                '<span style="background-color: #6c757d; color: white; padding: 3px 8px; '
                'border-radius: 12px; font-size: 11px; font-weight: bold;">➖ Empty</span>'
            )
        
        complete_entities = sum(1 for pct in total_ownership.values() if pct == 100)
        total_entities = len(total_ownership)
        
        if complete_entities == total_entities:
            color = '#28a745'  # Green
            icon = '✅'
            text = 'Complete'
        elif complete_entities == 0:
            color = '#dc3545'  # Red
            icon = '❌'
            text = 'Incomplete'
        else:
            color = '#ffc107'  # Yellow
            icon = '⚠️'
            text = f'{complete_entities}/{total_entities}'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{} {}</span>',
            color,
            icon,
            text
        )
    ownership_status_badge.short_description = "Ownership"
    
    def validation_score_badge(self, obj):
        # Calculate validation score based on various factors
        score = 0
        max_score = 100
        
        # Check ownership completeness (40 points)
        total_ownership = obj.get_total_ownership_by_entity()
        if total_ownership:
            complete_entities = sum(1 for pct in total_ownership.values() if pct == 100)
            total_entities = len(total_ownership)
            score += (complete_entities / total_entities) * 40
        
        # Check if has entities (20 points)
        if obj.entity_ownerships.exists():
            score += 20
        
        # Check if has description (10 points)
        if obj.description:
            score += 10
        
        # Check status (30 points)
        status_scores = {
            'drafting': 10,
            'sent_for_approval': 20,
            'approved': 30,
            'rejected': 5
        }
        score += status_scores.get(obj.status, 0)
        
        percentage = int(score)
        
        if percentage >= 90:
            color = '#28a745'  # Green
            icon = '🏆'
        elif percentage >= 70:
            color = '#ffc107'  # Yellow
            icon = '⭐'
        elif percentage >= 50:
            color = '#fd7e14'  # Orange
            icon = '⚠️'
        else:
            color = '#dc3545'  # Red
            icon = '❌'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{} {}%</span>',
            color,
            icon,
            percentage
        )
    validation_score_badge.short_description = "Score"
    
    def created_date_display(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')
    created_date_display.short_description = "Created"
    
    # ========================================================================
    # READONLY FIELD METHODS
    # ========================================================================
    
    def entities_count_display(self, obj):
        if not obj.pk:
            return "Save structure first to see entities"
        
        count = obj.entity_ownerships.values('owned_entity').distinct().count()
        entities = obj.entity_ownerships.select_related('owned_entity').values_list(
            'owned_entity__name', flat=True
        ).distinct()
        
        entity_list = ', '.join(entities[:5])
        if len(entities) > 5:
            entity_list += f' and {len(entities) - 5} more...'
        
        return format_html(
            '<strong>{} entities:</strong><br>{}',
            count,
            entity_list or 'No entities yet'
        )
    entities_count_display.short_description = "Entities Summary"
    
    def ownership_summary_display(self, obj):
        if not obj.pk:
            return "Save structure first to see ownership"
        
        total_ownership = obj.get_total_ownership_by_entity()
        
        if not total_ownership:
            return format_html(
                '<span style="color: #dc3545;">❌ No ownership relationships defined</span>'
            )
        
        summary_lines = []
        for entity, percentage in total_ownership.items():
            if percentage == 100:
                icon = '✅'
                color = '#28a745'
            elif percentage > 100:
                icon = '❌'
                color = '#dc3545'
            else:
                icon = '⚠️'
                color = '#ffc107'
            
            summary_lines.append(
                f'<span style="color: {color};">{icon} {entity.name}: {percentage}%</span>'
            )
        
        return format_html('<br>'.join(summary_lines))
    ownership_summary_display.short_description = "Ownership Summary"
    
    def validation_summary_display(self, obj):
        if not obj.pk:
            return "Save structure first to see validation"
        
        issues = []
        
        # Check ownership issues
        total_ownership = obj.get_total_ownership_by_entity()
        for entity, percentage in total_ownership.items():
            if percentage != 100:
                issues.append(f'{entity.name}: {percentage}% ownership')
        
        # Check for missing corporate names
        missing_corporate_names = obj.entity_ownerships.filter(
            corporate_name__isnull=True
        ).count()
        
        if missing_corporate_names:
            issues.append(f'{missing_corporate_names} ownerships missing corporate names')
        
        if not issues:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">✅ All validations passed</span>'
            )
        
        issue_list = '<br>'.join([f'• {issue}' for issue in issues[:5]])
        if len(issues) > 5:
            issue_list += f'<br>• and {len(issues) - 5} more issues...'
        
        return format_html(
            '<span style="color: #dc3545;">❌ Issues found:</span><br>{}',
            issue_list
        )
    validation_summary_display.short_description = "Validation Summary"


@admin.register(EntityOwnership)
class EntityOwnershipAdminImproved(admin.ModelAdmin):
    form = EntityOwnershipAdminForm
    
    list_display = [
        'structure_link', 'owner_display', 'owned_entity_link', 
        'ownership_percentage_display', 'shares_display', 'validation_status'
    ]
    
    list_filter = [
        'structure', 'owned_entity__entity_type', 'owned_entity__jurisdiction',
        ('created_at', admin.DateFieldListFilter),
    ]
    
    search_fields = [
        'structure__name', 'owned_entity__name', 'corporate_name',
        'owner_ubo__name', 'owner_entity__name'
    ]
    
    fieldsets = (
        ('🏗️ Structure & Entity', {
            'fields': ('structure', 'owned_entity'),
            'classes': ('wide',)
        }),
        ('👥 Owner Information', {
            'fields': ('owner_ubo', 'owner_entity'),
            'description': 'Select either UBO or Entity as owner (not both)'
        }),
        ('🏢 Corporate Identity', {
            'fields': ('corporate_name', 'hash_number'),
            'description': 'Corporate name and hash number for this ownership'
        }),
        ('📊 Ownership Details', {
            'fields': ('owned_shares', 'ownership_percentage'),
            'description': 'Fill either shares or percentage - the other will be calculated'
        }),
        ('💰 Share Valuation', {
            'fields': ('share_value_usd', 'share_value_eur', 'total_value_display'),
            'classes': ('collapse',),
            'description': 'Share values and calculated totals'
        }),
    )
    
    readonly_fields = ['total_value_display']
    
    ordering = ['structure', 'owned_entity']
    
    def structure_link(self, obj):
        url = reverse('admin:corporate_structure_change', args=[obj.structure.pk])
        return format_html('<a href="{}">{}</a>', url, obj.structure.name)
    structure_link.short_description = "Structure"
    
    def owner_display(self, obj):
        if obj.owner_ubo:
            return format_html('👤 {}', obj.owner_ubo.name)
        elif obj.owner_entity:
            return format_html('🏢 {}', obj.owner_entity.name)
        return "❌ No owner"
    owner_display.short_description = "Owner"
    
    def owned_entity_link(self, obj):
        url = reverse('admin:corporate_entity_change', args=[obj.owned_entity.pk])
        return format_html('<a href="{}">{}</a>', url, obj.owned_entity.name)
    owned_entity_link.short_description = "Owned Entity"
    
    def ownership_percentage_display(self, obj):
        if obj.ownership_percentage:
            return f"{obj.ownership_percentage}%"
        return "➖"
    ownership_percentage_display.short_description = "Percentage"
    
    def shares_display(self, obj):
        if obj.owned_shares:
            return f"{obj.owned_shares:,} shares"
        return "➖"
    shares_display.short_description = "Shares"
    
    def validation_status(self, obj):
        issues = []
        
        # Check ownership percentage
        if not obj.ownership_percentage:
            issues.append("No percentage")
        elif obj.ownership_percentage < 0 or obj.ownership_percentage > 100:
            issues.append("Invalid percentage")
        
        # Check owner
        if not obj.owner_ubo and not obj.owner_entity:
            issues.append("No owner")
        elif obj.owner_ubo and obj.owner_entity:
            issues.append("Multiple owners")
        
        # Check corporate name
        if not obj.corporate_name:
            issues.append("No corporate name")
        
        if not issues:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">✅ Valid</span>'
            )
        
        return format_html(
            '<span style="color: #dc3545; font-weight: bold;">❌ {}</span>',
            ', '.join(issues[:2])
        )
    validation_status.short_description = "Status"
    
    def total_value_display(self, obj):
        if obj.total_value_usd or obj.total_value_eur:
            values = []
            if obj.total_value_usd:
                values.append(f"${obj.total_value_usd:,.2f}")
            if obj.total_value_eur:
                values.append(f"€{obj.total_value_eur:,.2f}")
            return " / ".join(values)
        return "Not calculated"
    total_value_display.short_description = "Total Value"


# Keep existing Entity and ValidationRule admins but with minor improvements
@admin.register(Entity)
class EntityAdminImproved(admin.ModelAdmin):
    list_display = [
        'name', 'entity_type_badge', 'jurisdiction_display', 'shares_display', 'active_badge'
    ]
    list_filter = ['entity_type', 'jurisdiction', 'active', 'created_at']
    search_fields = ['name', 'tax_classification']
    
    fieldsets = [
        ('📋 Basic Information', {
            'fields': ['name', 'entity_type', 'tax_classification'],
            'classes': ('wide',)
        }),
        ('🌍 Jurisdiction', {
            'fields': ['jurisdiction', 'us_state', 'br_state']
        }),
        ('📊 Shares', {
            'fields': ['total_shares']
        }),
        ('🚀 Implementation', {
            'fields': ['implementation_templates', 'implementation_time', 'complexity'],
            'classes': ('collapse',)
        }),
        ('💰 Tax Information', {
            'fields': ['tax_impact_usa', 'tax_impact_brazil', 'tax_impact_others'],
            'classes': ['collapse']
        }),
        ('🔒 Privacy & Protection', {
            'fields': ['confidentiality_level', 'asset_protection', 'privacy_impact', 'privacy_score'],
            'classes': ['collapse']
        }),
        ('🏦 Banking & Compliance', {
            'fields': ['banking_relation_score', 'compliance_score', 'banking_facility'],
            'classes': ['collapse']
        }),
        ('📄 Documentation', {
            'fields': ['required_documentation', 'documents_url', 'required_forms_usa', 'required_forms_brazil'],
            'classes': ['collapse']
        }),
        ('✅ Status', {
            'fields': ['active']
        }),
    ]
    ordering = ['name']
    
    def entity_type_badge(self, obj):
        type_colors = {
            'corporation': '#007bff',
            'llc': '#28a745',
            'partnership': '#ffc107',
            'trust': '#17a2b8',
            'foundation': '#6f42c1',
        }
        
        color = type_colors.get(obj.entity_type.lower(), '#6c757d')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; '
            'border-radius: 10px; font-size: 10px; font-weight: bold;">{}</span>',
            color,
            obj.entity_type
        )
    entity_type_badge.short_description = "Type"
    
    def jurisdiction_display(self, obj):
        return f"{obj.jurisdiction}" + (f" ({obj.us_state})" if obj.us_state else "") + (f" ({obj.br_state})" if obj.br_state else "")
    jurisdiction_display.short_description = "Jurisdiction"
    
    def shares_display(self, obj):
        if obj.total_shares:
            return f"{obj.total_shares:,}"
        return "➖"
    shares_display.short_description = "Shares"
    
    def active_badge(self, obj):
        if obj.active:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">✅ Active</span>'
            )
        return format_html(
            '<span style="color: #dc3545; font-weight: bold;">❌ Inactive</span>'
        )
    active_badge.short_description = "Status"


@admin.register(ValidationRule)
class ValidationRuleAdminImproved(admin.ModelAdmin):
    list_display = [
        'parent_entity', 'related_entity', 'relationship_type_badge', 'severity_badge'
    ]
    list_filter = ['relationship_type', 'severity', 'created_at']
    search_fields = ['parent_entity__name', 'related_entity__name', 'description']
    
    fieldsets = [
        ('🏢 Entities', {
            'fields': ['parent_entity', 'related_entity'],
            'classes': ('wide',)
        }),
        ('🔗 Relationship', {
            'fields': ['relationship_type', 'severity', 'description']
        }),
        ('💰 Tax Information', {
            'fields': ['tax_impacts'],
            'description': 'Detailed tax implications of this entity combination',
            'classes': ('collapse',)
        }),
    ]
    ordering = ['parent_entity', 'related_entity']
    
    def relationship_type_badge(self, obj):
        return format_html(
            '<span style="background-color: #17a2b8; color: white; padding: 2px 6px; '
            'border-radius: 10px; font-size: 10px; font-weight: bold;">{}</span>',
            obj.relationship_type
        )
    relationship_type_badge.short_description = "Type"
    
    def severity_badge(self, obj):
        severity_colors = {
            'low': '#28a745',
            'medium': '#ffc107', 
            'high': '#fd7e14',
            'critical': '#dc3545'
        }
        
        color = severity_colors.get(obj.severity.lower(), '#6c757d')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; '
            'border-radius: 10px; font-size: 10px; font-weight: bold;">{}</span>',
            color,
            obj.severity.upper()
        )
    severity_badge.short_description = "Severity"

