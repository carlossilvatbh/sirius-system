from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.db import transaction
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
import json

from .models import Structure, Entity, EntityOwnership, ValidationRule
from parties.models import Party


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to require admin access"""
    def test_func(self):
        return self.request.user.is_staff


@method_decorator(staff_member_required, name='dispatch')
class StructureWizardView(AdminRequiredMixin, TemplateView):
    """Main wizard view for creating/editing structures"""
    template_name = 'admin/corporate/structure_wizard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get structure if editing
        structure_id = self.kwargs.get('structure_id')
        structure = None
        if structure_id:
            structure = get_object_or_404(Structure, pk=structure_id)
        
        # Get all available entities and parties
        entities = Entity.objects.filter(active=True).order_by('name')
        parties = Party.objects.all().order_by('name')
        
        # Get existing ownerships if editing
        ownerships = []
        if structure:
            ownerships = list(structure.entity_ownerships.select_related(
                'owner_ubo', 'owner_entity', 'owned_entity'
            ).all())
        
        context.update({
            'structure': structure,
            'entities': entities,
            'parties': parties,
            'ownerships': ownerships,
            'is_editing': bool(structure_id),
            'wizard_steps': [
                {'id': 1, 'name': 'Basic Info', 'icon': '📋'},
                {'id': 2, 'name': 'Entities & UBOs', 'icon': '🏢'},
                {'id': 3, 'name': 'Ownership Builder', 'icon': '🔗'},
                {'id': 4, 'name': 'Validation & Preview', 'icon': '✅'},
                {'id': 5, 'name': 'Save & Generate', 'icon': '💾'},
            ]
        })
        
        return context


@staff_member_required
@require_http_methods(["POST"])
def save_structure_step(request):
    """AJAX endpoint to save structure step data"""
    try:
        data = json.loads(request.body)
        step = data.get('step')
        structure_id = data.get('structure_id')
        
        if step == 1:
            # Save basic info
            return save_basic_info(request, data, structure_id)
        elif step == 2:
            # Save entities and UBOs selection
            return save_entities_ubos(request, data, structure_id)
        elif step == 3:
            # Save ownership relationships
            return save_ownership_relationships(request, data, structure_id)
        elif step == 4:
            # Validate and preview
            return validate_and_preview(request, data, structure_id)
        elif step == 5:
            # Final save and generate
            return final_save_and_generate(request, data, structure_id)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid step'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def save_basic_info(request, data, structure_id):
    """Save basic structure information"""
    try:
        with transaction.atomic():
            if structure_id:
                structure = get_object_or_404(Structure, pk=structure_id)
            else:
                structure = Structure()
            
            structure.name = data.get('name', '').strip()
            structure.description = data.get('description', '').strip()
            structure.status = data.get('status', 'drafting')
            
            # Validate required fields
            if not structure.name:
                return JsonResponse({
                    'success': False, 
                    'error': 'Structure name is required'
                })
            
            structure.save()
            
            return JsonResponse({
                'success': True,
                'structure_id': structure.id,
                'message': 'Basic information saved successfully'
            })
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def save_entities_ubos(request, data, structure_id):
    """Save selected entities and UBOs"""
    try:
        structure = get_object_or_404(Structure, pk=structure_id)
        
        selected_entities = data.get('selected_entities', [])
        selected_ubos = data.get('selected_ubos', [])
        
        # Store selections in session for next step
        request.session[f'structure_{structure_id}_entities'] = selected_entities
        request.session[f'structure_{structure_id}_ubos'] = selected_ubos
        
        return JsonResponse({
            'success': True,
            'message': f'Selected {len(selected_entities)} entities and {len(selected_ubos)} UBOs'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def save_ownership_relationships(request, data, structure_id):
    """Save ownership relationships"""
    try:
        with transaction.atomic():
            structure = get_object_or_404(Structure, pk=structure_id)
            
            # Clear existing ownerships
            structure.entity_ownerships.all().delete()
            
            ownerships = data.get('ownerships', [])
            
            for ownership_data in ownerships:
                ownership = EntityOwnership()
                ownership.structure = structure
                
                # Set owned entity
                owned_entity_id = ownership_data.get('owned_entity_id')
                if owned_entity_id:
                    ownership.owned_entity = Entity.objects.get(pk=owned_entity_id)
                
                # Set owner (UBO or Entity)
                owner_ubo_id = ownership_data.get('owner_ubo_id')
                owner_entity_id = ownership_data.get('owner_entity_id')
                
                if owner_ubo_id:
                    ownership.owner_ubo = Party.objects.get(pk=owner_ubo_id)
                elif owner_entity_id:
                    ownership.owner_entity = Entity.objects.get(pk=owner_entity_id)
                
                # Set ownership details
                ownership.ownership_percentage = ownership_data.get('percentage', 0)
                ownership.owned_shares = ownership_data.get('shares')
                ownership.corporate_name = ownership_data.get('corporate_name', '')
                ownership.hash_number = ownership_data.get('hash_number', '')
                
                # Set share values
                ownership.share_value_usd = ownership_data.get('share_value_usd')
                ownership.share_value_eur = ownership_data.get('share_value_eur')
                
                ownership.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Saved {len(ownerships)} ownership relationships'
            })
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def validate_and_preview(request, data, structure_id):
    """Validate structure and generate preview"""
    try:
        structure = get_object_or_404(Structure, pk=structure_id)
        
        # Perform validation
        validation_results = {
            'errors': [],
            'warnings': [],
            'info': []
        }
        
        # Check ownership completeness
        total_ownership = structure.get_total_ownership_by_entity()
        
        for entity, percentage in total_ownership.items():
            if percentage > 100:
                validation_results['errors'].append(
                    f'{entity.name}: Over-allocated ({percentage}%)'
                )
            elif percentage < 100 and percentage > 0:
                validation_results['warnings'].append(
                    f'{entity.name}: Under-allocated ({percentage}%)'
                )
            elif percentage == 100:
                validation_results['info'].append(
                    f'{entity.name}: Complete ownership (100%)'
                )
        
        # Check for missing corporate names
        missing_corporate_names = structure.entity_ownerships.filter(
            corporate_name__isnull=True
        ).count()
        
        if missing_corporate_names:
            validation_results['warnings'].append(
                f'{missing_corporate_names} ownerships missing corporate names'
            )
        
        # Generate structure preview
        preview_data = generate_structure_preview(structure)
        
        return JsonResponse({
            'success': True,
            'validation': validation_results,
            'preview': preview_data,
            'can_save': len(validation_results['errors']) == 0
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def final_save_and_generate(request, data, structure_id):
    """Final save and generate documentation"""
    try:
        with transaction.atomic():
            structure = get_object_or_404(Structure, pk=structure_id)
            
            # Update status if approved
            if data.get('approve', False):
                structure.status = 'approved'
                structure.save()
            
            # Generate documentation
            documentation = generate_structure_documentation(structure)
            
            # Clean up session data
            session_keys = [
                f'structure_{structure_id}_entities',
                f'structure_{structure_id}_ubos'
            ]
            for key in session_keys:
                if key in request.session:
                    del request.session[key]
            
            return JsonResponse({
                'success': True,
                'message': 'Structure saved successfully',
                'documentation': documentation,
                'redirect_url': reverse('admin:corporate_structure_change', args=[structure.id])
            })
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def generate_structure_preview(structure):
    """Generate structure preview data"""
    preview = {
        'name': structure.name,
        'description': structure.description,
        'status': structure.get_status_display(),
        'entities': [],
        'ownerships': [],
        'summary': {}
    }
    
    # Get entities
    entities = {}
    for ownership in structure.entity_ownerships.select_related('owned_entity'):
        entity = ownership.owned_entity
        if entity.id not in entities:
            entities[entity.id] = {
                'id': entity.id,
                'name': entity.name,
                'type': entity.entity_type,
                'jurisdiction': entity.jurisdiction,
                'total_ownership': 0,
                'owners': []
            }
    
    # Get ownerships
    for ownership in structure.entity_ownerships.select_related('owner_ubo', 'owner_entity', 'owned_entity'):
        owner_name = ''
        owner_type = ''
        
        if ownership.owner_ubo:
            owner_name = ownership.owner_ubo.name
            owner_type = 'UBO'
        elif ownership.owner_entity:
            owner_name = ownership.owner_entity.name
            owner_type = 'Entity'
        
        ownership_data = {
            'owner_name': owner_name,
            'owner_type': owner_type,
            'owned_entity': ownership.owned_entity.name,
            'percentage': ownership.ownership_percentage,
            'shares': ownership.owned_shares,
            'corporate_name': ownership.corporate_name,
            'hash_number': ownership.hash_number
        }
        
        preview['ownerships'].append(ownership_data)
        
        # Update entity ownership total
        entity_id = ownership.owned_entity.id
        if entity_id in entities:
            entities[entity_id]['total_ownership'] += ownership.ownership_percentage or 0
            entities[entity_id]['owners'].append({
                'name': owner_name,
                'type': owner_type,
                'percentage': ownership.ownership_percentage
            })
    
    preview['entities'] = list(entities.values())
    
    # Generate summary
    preview['summary'] = {
        'total_entities': len(entities),
        'total_ownerships': len(preview['ownerships']),
        'complete_entities': sum(1 for e in entities.values() if e['total_ownership'] == 100),
        'incomplete_entities': sum(1 for e in entities.values() if 0 < e['total_ownership'] < 100),
        'over_allocated_entities': sum(1 for e in entities.values() if e['total_ownership'] > 100)
    }
    
    return preview


def generate_structure_documentation(structure):
    """Generate structure documentation"""
    doc = {
        'structure_name': structure.name,
        'created_date': structure.created_at.strftime('%Y-%m-%d %H:%M'),
        'status': structure.get_status_display(),
        'entities_summary': [],
        'ownership_matrix': [],
        'validation_summary': {}
    }
    
    # Generate entities summary
    entities = {}
    for ownership in structure.entity_ownerships.select_related('owned_entity'):
        entity = ownership.owned_entity
        if entity.id not in entities:
            entities[entity.id] = {
                'name': entity.name,
                'type': entity.entity_type,
                'jurisdiction': entity.jurisdiction,
                'total_shares': entity.total_shares,
                'ownership_percentage': 0
            }
        entities[entity.id]['ownership_percentage'] += ownership.ownership_percentage or 0
    
    doc['entities_summary'] = list(entities.values())
    
    # Generate ownership matrix
    for ownership in structure.entity_ownerships.select_related('owner_ubo', 'owner_entity', 'owned_entity'):
        owner_name = ownership.owner_ubo.name if ownership.owner_ubo else ownership.owner_entity.name
        
        doc['ownership_matrix'].append({
            'owner': owner_name,
            'owned_entity': ownership.owned_entity.name,
            'percentage': ownership.ownership_percentage,
            'shares': ownership.owned_shares,
            'corporate_name': ownership.corporate_name
        })
    
    # Generate validation summary
    total_ownership = structure.get_total_ownership_by_entity()
    validation_issues = []
    
    for entity, percentage in total_ownership.items():
        if percentage != 100:
            validation_issues.append(f'{entity.name}: {percentage}%')
    
    doc['validation_summary'] = {
        'total_entities': len(entities),
        'complete_entities': sum(1 for pct in total_ownership.values() if pct == 100),
        'issues': validation_issues
    }
    
    return doc


@staff_member_required
def get_structure_data(request, structure_id):
    """Get structure data for wizard"""
    try:
        structure = get_object_or_404(Structure, pk=structure_id)
        
        # Get ownerships
        ownerships = []
        for ownership in structure.entity_ownerships.select_related('owner_ubo', 'owner_entity', 'owned_entity'):
            ownership_data = {
                'id': ownership.id,
                'owned_entity_id': ownership.owned_entity.id,
                'owned_entity_name': ownership.owned_entity.name,
                'owner_ubo_id': ownership.owner_ubo.id if ownership.owner_ubo else None,
                'owner_ubo_name': ownership.owner_ubo.name if ownership.owner_ubo else None,
                'owner_entity_id': ownership.owner_entity.id if ownership.owner_entity else None,
                'owner_entity_name': ownership.owner_entity.name if ownership.owner_entity else None,
                'percentage': ownership.ownership_percentage,
                'shares': ownership.owned_shares,
                'corporate_name': ownership.corporate_name,
                'hash_number': ownership.hash_number,
                'share_value_usd': ownership.share_value_usd,
                'share_value_eur': ownership.share_value_eur
            }
            ownerships.append(ownership_data)
        
        return JsonResponse({
            'success': True,
            'structure': {
                'id': structure.id,
                'name': structure.name,
                'description': structure.description,
                'status': structure.status
            },
            'ownerships': ownerships
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@staff_member_required
def duplicate_structure(request, structure_id):
    """Duplicate an existing structure"""
    try:
        with transaction.atomic():
            original = get_object_or_404(Structure, pk=structure_id)
            
            # Create duplicate
            duplicate = Structure.objects.create(
                name=f"{original.name} (Copy)",
                description=f"Copy of {original.description}",
                status='drafting'
            )
            
            # Copy ownerships
            for ownership in original.entity_ownerships.all():
                EntityOwnership.objects.create(
                    structure=duplicate,
                    owner_ubo=ownership.owner_ubo,
                    owner_entity=ownership.owner_entity,
                    owned_entity=ownership.owned_entity,
                    ownership_percentage=ownership.ownership_percentage,
                    owned_shares=ownership.owned_shares,
                    corporate_name=ownership.corporate_name,
                    hash_number=f"{ownership.hash_number}_copy" if ownership.hash_number else None,
                    share_value_usd=ownership.share_value_usd,
                    share_value_eur=ownership.share_value_eur
                )
            
            messages.success(request, f'Structure "{original.name}" duplicated successfully')
            
            return redirect('admin:corporate_structure_change', duplicate.id)
            
    except Exception as e:
        messages.error(request, f'Error duplicating structure: {str(e)}')
        return redirect('admin:corporate_structure_changelist')


# Quick validation endpoint
@staff_member_required
@require_http_methods(["POST"])
def quick_validate_structure(request, structure_id):
    """Quick validation endpoint for AJAX calls"""
    try:
        structure = get_object_or_404(Structure, pk=structure_id)
        
        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'score': 0
        }
        
        # Check ownership completeness
        total_ownership = structure.get_total_ownership_by_entity()
        complete_entities = 0
        total_entities = len(total_ownership)
        
        for entity, percentage in total_ownership.items():
            if percentage > 100:
                validation_results['errors'].append(f'{entity.name}: Over-allocated ({percentage}%)')
                validation_results['valid'] = False
            elif percentage < 100 and percentage > 0:
                validation_results['warnings'].append(f'{entity.name}: Under-allocated ({percentage}%)')
            elif percentage == 100:
                complete_entities += 1
        
        # Calculate score
        if total_entities > 0:
            validation_results['score'] = int((complete_entities / total_entities) * 100)
        
        return JsonResponse(validation_results)
        
    except Exception as e:
        return JsonResponse({'valid': False, 'error': str(e)})


# Ownership matrix view
@staff_member_required
def ownership_matrix_view(request, structure_id):
    """View for ownership matrix visualization"""
    structure = get_object_or_404(Structure, pk=structure_id)
    
    # Build matrix data
    matrix_data = build_ownership_matrix(structure)
    
    context = {
        'structure': structure,
        'matrix_data': matrix_data,
        'title': f'Ownership Matrix - {structure.name}'
    }
    
    return render(request, 'admin/corporate/ownership_matrix.html', context)


def build_ownership_matrix(structure):
    """Build ownership matrix data for visualization"""
    entities = {}
    owners = {}
    matrix = {}
    
    # Collect all entities and owners
    for ownership in structure.entity_ownerships.select_related('owner_ubo', 'owner_entity', 'owned_entity'):
        # Add owned entity
        entity_id = f"entity_{ownership.owned_entity.id}"
        entities[entity_id] = {
            'id': entity_id,
            'name': ownership.owned_entity.name,
            'type': 'entity'
        }
        
        # Add owner
        if ownership.owner_ubo:
            owner_id = f"ubo_{ownership.owner_ubo.id}"
            owners[owner_id] = {
                'id': owner_id,
                'name': ownership.owner_ubo.name,
                'type': 'ubo'
            }
        elif ownership.owner_entity:
            owner_id = f"entity_{ownership.owner_entity.id}"
            owners[owner_id] = {
                'id': owner_id,
                'name': ownership.owner_entity.name,
                'type': 'entity'
            }
            # Also add to entities if not already there
            entities[owner_id] = owners[owner_id]
        
        # Add to matrix
        if owner_id not in matrix:
            matrix[owner_id] = {}
        
        matrix[owner_id][entity_id] = {
            'percentage': ownership.ownership_percentage,
            'shares': ownership.owned_shares,
            'corporate_name': ownership.corporate_name
        }
    
    return {
        'entities': entities,
        'owners': owners,
        'matrix': matrix
    }

