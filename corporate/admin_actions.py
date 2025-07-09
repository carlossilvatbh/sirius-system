"""
Custom Django Admin Actions for SIRIUS Corporate Structures
"""

from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db import transaction
from django.core.exceptions import ValidationError
import json
import csv
from io import StringIO
from datetime import datetime

from .models import Structure, Entity, EntityOwnership
from parties.models import Party


class StructureAdminActions:
    """Custom actions for Structure admin"""
    
    @admin.action(description="🔍 Validate selected structures")
    def validate_structures(self, request, queryset):
        """Validate ownership completeness for selected structures"""
        results = []
        
        for structure in queryset:
            validation_result = self._validate_structure(structure)
            results.append({
                'structure': structure,
                'result': validation_result
            })
        
        # Prepare context for results template
        context = {
            'title': 'Structure Validation Results',
            'results': results,
            'total_structures': queryset.count(),
            'valid_structures': sum(1 for r in results if r['result']['is_valid']),
            'invalid_structures': sum(1 for r in results if not r['result']['is_valid'])
        }
        
        return render(request, 'admin/corporate/structure_validation_results.html', context)
    
    @admin.action(description="📊 Generate ownership report")
    def generate_ownership_report(self, request, queryset):
        """Generate detailed ownership report for selected structures"""
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="ownership_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        
        # Write header
        writer.writerow([
            'Structure Name',
            'Structure Status',
            'Entity Name',
            'Entity Type',
            'Owner Name',
            'Owner Type',
            'Ownership Percentage',
            'Shares',
            'Corporate Name',
            'Hash Number',
            'Share Value USD',
            'Share Value EUR',
            'Total Value USD',
            'Total Value EUR',
            'Validation Status'
        ])
        
        # Write data
        for structure in queryset:
            ownerships = EntityOwnership.objects.filter(structure=structure).select_related(
                'owned_entity', 'owner_ubo', 'owner_entity'
            )
            
            if not ownerships.exists():
                # Structure with no ownerships
                writer.writerow([
                    structure.name,
                    structure.get_status_display(),
                    'No entities',
                    '',
                    'No owners',
                    '',
                    '0',
                    '0',
                    '',
                    '',
                    '0.00',
                    '0.00',
                    '0.00',
                    '0.00',
                    'Invalid - No ownerships'
                ])
            else:
                for ownership in ownerships:
                    owner_name = ownership.owner_ubo.name if ownership.owner_ubo else (
                        ownership.owner_entity.name if ownership.owner_entity else 'Unknown'
                    )
                    owner_type = 'UBO' if ownership.owner_ubo else 'Entity'
                    
                    total_value_usd = (ownership.shares or 0) * (ownership.share_value_usd or 0)
                    total_value_eur = (ownership.shares or 0) * (ownership.share_value_eur or 0)
                    
                    validation = self._validate_entity_ownership(ownership.owned_entity, structure)
                    validation_status = 'Valid' if validation['is_complete'] else f"Invalid - {validation['total_percentage']:.1f}%"
                    
                    writer.writerow([
                        structure.name,
                        structure.get_status_display(),
                        ownership.owned_entity.name,
                        ownership.owned_entity.entity_type,
                        owner_name,
                        owner_type,
                        f"{ownership.percentage:.2f}" if ownership.percentage else '0.00',
                        ownership.shares or '0',
                        ownership.corporate_name or '',
                        ownership.hash_number or '',
                        f"{ownership.share_value_usd:.2f}" if ownership.share_value_usd else '0.00',
                        f"{ownership.share_value_eur:.2f}" if ownership.share_value_eur else '0.00',
                        f"{total_value_usd:.2f}",
                        f"{total_value_eur:.2f}",
                        validation_status
                    ])
        
        return response
    
    @admin.action(description="✅ Auto-approve valid structures")
    def auto_approve_structures(self, request, queryset):
        """Auto-approve structures that pass validation"""
        approved_count = 0
        skipped_count = 0
        
        with transaction.atomic():
            for structure in queryset:
                validation_result = self._validate_structure(structure)
                
                if validation_result['is_valid'] and structure.status != 'approved':
                    structure.status = 'approved'
                    structure.save()
                    approved_count += 1
                else:
                    skipped_count += 1
        
        if approved_count > 0:
            messages.success(
                request,
                f"Successfully approved {approved_count} structure(s). "
                f"{skipped_count} structure(s) skipped (invalid or already approved)."
            )
        else:
            messages.warning(
                request,
                f"No structures were approved. {skipped_count} structure(s) skipped."
            )
    
    @admin.action(description="🔄 Auto-balance ownership")
    def auto_balance_ownership(self, request, queryset):
        """Auto-balance ownership percentages for selected structures"""
        balanced_count = 0
        
        with transaction.atomic():
            for structure in queryset:
                if self._auto_balance_structure_ownership(structure):
                    balanced_count += 1
        
        if balanced_count > 0:
            messages.success(
                request,
                f"Successfully auto-balanced ownership for {balanced_count} structure(s)."
            )
        else:
            messages.warning(
                request,
                "No structures required ownership balancing."
            )
    
    @admin.action(description="📋 Clone selected structures")
    def clone_structures(self, request, queryset):
        """Clone selected structures with all their ownerships"""
        cloned_count = 0
        
        with transaction.atomic():
            for structure in queryset:
                cloned_structure = self._clone_structure(structure)
                if cloned_structure:
                    cloned_count += 1
        
        if cloned_count > 0:
            messages.success(
                request,
                f"Successfully cloned {cloned_count} structure(s)."
            )
        else:
            messages.error(
                request,
                "Failed to clone structures."
            )
    
    @admin.action(description="🗑️ Archive old structures")
    def archive_structures(self, request, queryset):
        """Archive selected structures (soft delete)"""
        archived_count = 0
        
        with transaction.atomic():
            for structure in queryset:
                if structure.status not in ['approved', 'sent_for_approval']:
                    structure.status = 'archived'
                    structure.save()
                    archived_count += 1
        
        if archived_count > 0:
            messages.success(
                request,
                f"Successfully archived {archived_count} structure(s)."
            )
        else:
            messages.warning(
                request,
                "No structures were archived. Only drafting/rejected structures can be archived."
            )
    
    def _validate_structure(self, structure):
        """Validate a single structure"""
        errors = []
        warnings = []
        info = []
        
        # Get all ownerships for this structure
        ownerships = EntityOwnership.objects.filter(structure=structure)
        
        if not ownerships.exists():
            errors.append("No ownership relationships defined")
            return {
                'is_valid': False,
                'errors': errors,
                'warnings': warnings,
                'info': info
            }
        
        # Group by entity and validate totals
        entity_totals = {}
        for ownership in ownerships:
            entity_id = ownership.owned_entity_id
            if entity_id not in entity_totals:
                entity_totals[entity_id] = {
                    'entity': ownership.owned_entity,
                    'total_percentage': 0,
                    'ownerships': []
                }
            entity_totals[entity_id]['total_percentage'] += ownership.percentage or 0
            entity_totals[entity_id]['ownerships'].append(ownership)
        
        # Validate each entity
        for entity_data in entity_totals.values():
            entity = entity_data['entity']
            total = entity_data['total_percentage']
            
            if total > 100:
                errors.append(f"Entity '{entity.name}' is over-owned ({total:.1f}%)")
            elif total < 100:
                warnings.append(f"Entity '{entity.name}' is under-owned ({total:.1f}%)")
            else:
                info.append(f"Entity '{entity.name}' has complete ownership (100%)")
        
        # Check for missing required fields
        for ownership in ownerships:
            if not ownership.corporate_name:
                warnings.append(f"Missing corporate name for {ownership.owned_entity.name}")
            if not ownership.hash_number:
                warnings.append(f"Missing hash number for {ownership.owned_entity.name}")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'info': info,
            'entity_count': len(entity_totals),
            'ownership_count': ownerships.count()
        }
    
    def _validate_entity_ownership(self, entity, structure):
        """Validate ownership for a specific entity"""
        ownerships = EntityOwnership.objects.filter(
            structure=structure,
            owned_entity=entity
        )
        
        total_percentage = sum(o.percentage or 0 for o in ownerships)
        
        return {
            'is_complete': total_percentage == 100,
            'total_percentage': total_percentage,
            'ownership_count': ownerships.count()
        }
    
    def _auto_balance_structure_ownership(self, structure):
        """Auto-balance ownership for a structure"""
        ownerships = EntityOwnership.objects.filter(structure=structure)
        
        if not ownerships.exists():
            return False
        
        # Group by entity
        entity_groups = {}
        for ownership in ownerships:
            entity_id = ownership.owned_entity_id
            if entity_id not in entity_groups:
                entity_groups[entity_id] = []
            entity_groups[entity_id].append(ownership)
        
        # Balance each entity group
        balanced = False
        for group in entity_groups.values():
            if len(group) > 1:  # Only balance if multiple ownerships
                equal_percentage = 100.0 / len(group)
                for ownership in group:
                    ownership.percentage = round(equal_percentage, 2)
                    ownership.save()
                balanced = True
        
        return balanced
    
    def _clone_structure(self, structure):
        """Clone a structure with all its ownerships"""
        try:
            # Create new structure
            cloned_structure = Structure.objects.create(
                name=f"{structure.name} (Copy)",
                description=f"Copy of {structure.name}",
                status='drafting'
            )
            
            # Clone all ownerships
            ownerships = EntityOwnership.objects.filter(structure=structure)
            for ownership in ownerships:
                EntityOwnership.objects.create(
                    structure=cloned_structure,
                    owned_entity=ownership.owned_entity,
                    owner_ubo=ownership.owner_ubo,
                    owner_entity=ownership.owner_entity,
                    percentage=ownership.percentage,
                    shares=ownership.shares,
                    corporate_name=ownership.corporate_name,
                    hash_number=ownership.hash_number,
                    share_value_usd=ownership.share_value_usd,
                    share_value_eur=ownership.share_value_eur
                )
            
            return cloned_structure
            
        except Exception as e:
            return None


class EntityAdminActions:
    """Custom actions for Entity admin"""
    
    @admin.action(description="📊 Generate entity report")
    def generate_entity_report(self, request, queryset):
        """Generate detailed report for selected entities"""
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="entity_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        
        # Write header
        writer.writerow([
            'Entity Name',
            'Entity Type',
            'Jurisdiction',
            'Total Shares',
            'Structures Count',
            'Total Ownership Percentage',
            'Owners Count',
            'UBO Owners',
            'Entity Owners',
            'Average Share Value USD',
            'Average Share Value EUR',
            'Status'
        ])
        
        # Write data
        for entity in queryset:
            ownerships = EntityOwnership.objects.filter(owned_entity=entity)
            
            total_percentage = sum(o.percentage or 0 for o in ownerships)
            structures_count = ownerships.values('structure').distinct().count()
            owners_count = ownerships.count()
            ubo_owners = ownerships.filter(owner_ubo__isnull=False).count()
            entity_owners = ownerships.filter(owner_entity__isnull=False).count()
            
            # Calculate average share values
            share_values_usd = [o.share_value_usd for o in ownerships if o.share_value_usd]
            share_values_eur = [o.share_value_eur for o in ownerships if o.share_value_eur]
            
            avg_share_value_usd = sum(share_values_usd) / len(share_values_usd) if share_values_usd else 0
            avg_share_value_eur = sum(share_values_eur) / len(share_values_eur) if share_values_eur else 0
            
            status = 'Complete' if total_percentage == 100 else f'Incomplete ({total_percentage:.1f}%)'
            
            writer.writerow([
                entity.name,
                entity.entity_type,
                entity.jurisdiction,
                entity.total_shares or 0,
                structures_count,
                f"{total_percentage:.2f}",
                owners_count,
                ubo_owners,
                entity_owners,
                f"{avg_share_value_usd:.2f}",
                f"{avg_share_value_eur:.2f}",
                status
            ])
        
        return response
    
    @admin.action(description="🔄 Update share calculations")
    def update_share_calculations(self, request, queryset):
        """Update share calculations for selected entities"""
        updated_count = 0
        
        with transaction.atomic():
            for entity in queryset:
                ownerships = EntityOwnership.objects.filter(owned_entity=entity)
                
                for ownership in ownerships:
                    if ownership.percentage and entity.total_shares:
                        # Calculate shares from percentage
                        calculated_shares = int((ownership.percentage / 100) * entity.total_shares)
                        if ownership.shares != calculated_shares:
                            ownership.shares = calculated_shares
                            ownership.save()
                            updated_count += 1
        
        if updated_count > 0:
            messages.success(
                request,
                f"Updated share calculations for {updated_count} ownership(s)."
            )
        else:
            messages.info(
                request,
                "No share calculations needed updating."
            )


class OwnershipAdminActions:
    """Custom actions for EntityOwnership admin"""
    
    @admin.action(description="🔍 Validate ownership percentages")
    def validate_ownership_percentages(self, request, queryset):
        """Validate that ownership percentages are correct"""
        issues = []
        
        # Group by entity
        entity_groups = {}
        for ownership in queryset:
            entity_id = ownership.owned_entity_id
            if entity_id not in entity_groups:
                entity_groups[entity_id] = {
                    'entity': ownership.owned_entity,
                    'ownerships': []
                }
            entity_groups[entity_id]['ownerships'].append(ownership)
        
        # Check each entity group
        for entity_data in entity_groups.values():
            entity = entity_data['entity']
            ownerships = entity_data['ownerships']
            
            total_percentage = sum(o.percentage or 0 for o in ownerships)
            
            if total_percentage != 100:
                issues.append({
                    'entity': entity,
                    'total_percentage': total_percentage,
                    'ownerships_count': len(ownerships),
                    'issue_type': 'over' if total_percentage > 100 else 'under'
                })
        
        # Prepare context for results
        context = {
            'title': 'Ownership Validation Results',
            'issues': issues,
            'total_entities': len(entity_groups),
            'valid_entities': len(entity_groups) - len(issues),
            'invalid_entities': len(issues)
        }
        
        return render(request, 'admin/corporate/ownership_validation_results.html', context)
    
    @admin.action(description="💰 Calculate total values")
    def calculate_total_values(self, request, queryset):
        """Calculate total values for selected ownerships"""
        updated_count = 0
        
        with transaction.atomic():
            for ownership in queryset:
                updated = False
                
                # Calculate USD total
                if ownership.shares and ownership.share_value_usd:
                    total_usd = ownership.shares * ownership.share_value_usd
                    # Store in a custom field if needed
                    updated = True
                
                # Calculate EUR total
                if ownership.shares and ownership.share_value_eur:
                    total_eur = ownership.shares * ownership.share_value_eur
                    # Store in a custom field if needed
                    updated = True
                
                if updated:
                    ownership.save()
                    updated_count += 1
        
        messages.success(
            request,
            f"Calculated total values for {updated_count} ownership(s)."
        )
    
    @admin.action(description="🔄 Sync shares with percentages")
    def sync_shares_with_percentages(self, request, queryset):
        """Synchronize shares with percentages based on entity total shares"""
        updated_count = 0
        
        with transaction.atomic():
            for ownership in queryset:
                entity = ownership.owned_entity
                
                if ownership.percentage and entity.total_shares:
                    calculated_shares = int((ownership.percentage / 100) * entity.total_shares)
                    
                    if ownership.shares != calculated_shares:
                        ownership.shares = calculated_shares
                        ownership.save()
                        updated_count += 1
        
        if updated_count > 0:
            messages.success(
                request,
                f"Synchronized shares for {updated_count} ownership(s)."
            )
        else:
            messages.info(
                request,
                "All shares are already synchronized with percentages."
            )


# Utility functions for admin integration
def get_structure_admin_actions():
    """Get all structure admin actions"""
    actions = StructureAdminActions()
    return [
        actions.validate_structures,
        actions.generate_ownership_report,
        actions.auto_approve_structures,
        actions.auto_balance_ownership,
        actions.clone_structures,
        actions.archive_structures
    ]

def get_entity_admin_actions():
    """Get all entity admin actions"""
    actions = EntityAdminActions()
    return [
        actions.generate_entity_report,
        actions.update_share_calculations
    ]

def get_ownership_admin_actions():
    """Get all ownership admin actions"""
    actions = OwnershipAdminActions()
    return [
        actions.validate_ownership_percentages,
        actions.calculate_total_values,
        actions.sync_shares_with_percentages
    ]

