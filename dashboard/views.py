from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from sales.models import StructureRequest, StructureApproval
from corporate.models import Structure, Entity, EntityOwnership
from parties.models import Party


@method_decorator([login_required, staff_member_required], name='dispatch')
class DashboardView(TemplateView):
    """
    Main dashboard view with overview of all structure requests and approvals
    """
    template_name = 'admin/dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Quick statistics
        context['stats'] = self.get_quick_stats()
        
        # Pending requests (Sales → Corporate)
        context['pending_requests'] = self.get_pending_requests()
        
        # Structures in progress (Corporate working)
        context['structures_in_progress'] = self.get_structures_in_progress()
        
        # Pending approvals (Corporate → Sales)
        context['pending_approvals'] = self.get_pending_approvals()
        
        # Recent activity
        context['recent_activity'] = self.get_recent_activity()
        
        # Performance metrics
        context['performance_metrics'] = self.get_performance_metrics()
        
        return context
    
    def get_quick_stats(self):
        """Get quick statistics for dashboard cards"""
        return {
            'pending_requests': StructureRequest.objects.filter(status='SUBMITTED').count(),
            'in_review': StructureRequest.objects.filter(status='IN_REVIEW').count(),
            'in_progress': StructureRequest.objects.filter(status='IN_PROGRESS').count(),
            'pending_approval': Structure.objects.filter(status='SENT_FOR_APPROVAL').count(),
            'completed_this_month': StructureRequest.objects.filter(
                status='COMPLETED',
                updated_at__gte=timezone.now() - timedelta(days=30)
            ).count(),
            'total_structures': Structure.objects.count(),
            'total_entities': Entity.objects.filter(active=True).count(),
            'total_parties': Party.objects.count(),
        }
    
    def get_pending_requests(self):
        """Get pending structure requests from Sales"""
        return StructureRequest.objects.filter(
            status__in=['SUBMITTED', 'IN_REVIEW']
        ).select_related(
            'point_of_contact_party',
            'point_of_contact_partner'
        ).prefetch_related(
            'requesting_parties'
        ).order_by('-submitted_at')[:10]
    
    def get_structures_in_progress(self):
        """Get structures currently being developed by Corporate"""
        return Structure.objects.filter(
            status='DRAFTING'
        ).prefetch_related(
            'entity_ownerships__owned_entity',
            'entity_ownerships__owner_ubo',
            'entity_ownerships__owner_entity'
        ).annotate(
            entities_count=Count('entity_ownerships')
        ).order_by('-created_at')[:10]
    
    def get_pending_approvals(self):
        """Get structures waiting for Sales approval"""
        return Structure.objects.filter(
            status='SENT_FOR_APPROVAL'
        ).prefetch_related(
            'entity_ownerships__owned_entity'
        ).annotate(
            entities_count=Count('entity_ownerships')
        ).order_by('-updated_at')[:10]
    
    def get_recent_activity(self):
        """Get recent activity across the system"""
        activities = []
        
        # Recent requests
        recent_requests = StructureRequest.objects.filter(
            submitted_at__gte=timezone.now() - timedelta(days=7)
        ).order_by('-submitted_at')[:5]
        
        for request in recent_requests:
            activities.append({
                'type': 'request_submitted',
                'title': f'New structure request #{request.pk}',
                'description': request.description[:100] + '...' if len(request.description) > 100 else request.description,
                'timestamp': request.submitted_at,
                'url': f'/admin/sales/structurerequest/{request.pk}/change/',
                'icon': 'fas fa-plus-circle',
                'color': 'primary'
            })
        
        # Recent structures
        recent_structures = Structure.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).order_by('-created_at')[:5]
        
        for structure in recent_structures:
            activities.append({
                'type': 'structure_created',
                'title': f'Structure created: {structure.name}',
                'description': structure.description[:100] + '...' if len(structure.description) > 100 else structure.description,
                'timestamp': structure.created_at,
                'url': f'/admin/corporate/structure/{structure.pk}/change/',
                'icon': 'fas fa-sitemap',
                'color': 'success'
            })
        
        # Recent approvals
        recent_approvals = StructureApproval.objects.filter(
            action_date__gte=timezone.now() - timedelta(days=7)
        ).select_related('structure').order_by('-action_date')[:5]
        
        for approval in recent_approvals:
            activities.append({
                'type': 'structure_approved',
                'title': f'Structure {approval.get_action_display().lower()}: {approval.structure.name}',
                'description': f'Action: {approval.get_action_display()}',
                'timestamp': approval.action_date,
                'url': f'/admin/sales/structureapproval/{approval.pk}/change/',
                'icon': 'fas fa-check-circle',
                'color': 'info'
            })
        
        # Sort all activities by timestamp
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return activities[:15]
    
    def get_performance_metrics(self):
        """Get performance metrics for the dashboard"""
        now = timezone.now()
        last_30_days = now - timedelta(days=30)
        
        # Completion rate
        total_requests = StructureRequest.objects.filter(submitted_at__gte=last_30_days).count()
        completed_requests = StructureRequest.objects.filter(
            status='COMPLETED',
            updated_at__gte=last_30_days
        ).count()
        completion_rate = (completed_requests / total_requests * 100) if total_requests > 0 else 0
        
        # Average processing time
        completed_with_times = StructureRequest.objects.filter(
            status='COMPLETED',
            updated_at__gte=last_30_days
        )
        
        total_processing_time = 0
        count = 0
        for request in completed_with_times:
            processing_time = (request.updated_at - request.submitted_at).days
            total_processing_time += processing_time
            count += 1
        
        avg_processing_time = total_processing_time / count if count > 0 else 0
        
        # Approval rate
        total_sent_for_approval = Structure.objects.filter(
            updated_at__gte=last_30_days,
            status__in=['SENT_FOR_APPROVAL', 'APPROVED']
        ).count()
        
        approved_structures = StructureApproval.objects.filter(
            action_date__gte=last_30_days,
            action__in=['APPROVED', 'APPROVED_WITH_PRICE_CHANGE']
        ).count()
        
        approval_rate = (approved_structures / total_sent_for_approval * 100) if total_sent_for_approval > 0 else 0
        
        return {
            'completion_rate': round(completion_rate, 1),
            'avg_processing_time': round(avg_processing_time, 1),
            'approval_rate': round(approval_rate, 1),
            'total_requests_30d': total_requests,
            'completed_requests_30d': completed_requests,
            'approved_structures_30d': approved_structures,
        }


@login_required
@staff_member_required
def quick_action_view(request):
    """Handle quick actions from dashboard"""
    if request.method == 'POST':
        action = request.POST.get('action')
        object_id = request.POST.get('object_id')
        
        if action == 'assign_request':
            request_obj = get_object_or_404(StructureRequest, pk=object_id)
            request_obj.status = 'IN_REVIEW'
            request_obj.save()
            messages.success(request, f'Request #{request_obj.pk} assigned for review.')
            
        elif action == 'start_progress':
            request_obj = get_object_or_404(StructureRequest, pk=object_id)
            request_obj.status = 'IN_PROGRESS'
            request_obj.save()
            messages.success(request, f'Request #{request_obj.pk} marked as in progress.')
            
        elif action == 'send_for_approval':
            structure = get_object_or_404(Structure, pk=object_id)
            structure.status = 'SENT_FOR_APPROVAL'
            structure.save()
            messages.success(request, f'Structure "{structure.name}" sent for approval.')
            
        elif action == 'complete_request':
            request_obj = get_object_or_404(StructureRequest, pk=object_id)
            request_obj.status = 'COMPLETED'
            request_obj.save()
            messages.success(request, f'Request #{request_obj.pk} marked as completed.')
    
    return redirect('admin:dashboard')


@login_required
@staff_member_required
def dashboard_api_view(request):
    """API endpoint for dashboard data updates"""
    if request.method == 'GET':
        data_type = request.GET.get('type')
        
        if data_type == 'stats':
            dashboard_view = DashboardView()
            stats = dashboard_view.get_quick_stats()
            return JsonResponse(stats)
            
        elif data_type == 'recent_activity':
            dashboard_view = DashboardView()
            activities = dashboard_view.get_recent_activity()
            return JsonResponse({'activities': activities})
            
        elif data_type == 'performance':
            dashboard_view = DashboardView()
            metrics = dashboard_view.get_performance_metrics()
            return JsonResponse(metrics)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


class PublicDashboardView(TemplateView):
    """
    Public dashboard view that doesn't require authentication
    Shows basic system statistics
    """
    template_name = 'admin/dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Basic public statistics
        context['stats'] = {
            'pending_requests': 0,  # Hide sensitive data for public view
            'in_progress': Structure.objects.filter(status='DRAFTING').count(),
            'pending_approvals': 0,  # Hide sensitive data for public view
            'completed': Structure.objects.filter(status='APPROVED').count(),
        }
        
        # Public structures (approved ones only)
        context['structures_in_progress'] = Structure.objects.filter(
            status__in=['APPROVED']
        ).order_by('-created_at')[:5]
        
        # Empty for public view (no sensitive data)
        context['pending_requests'] = []
        context['pending_approvals'] = []
        context['recent_activity'] = []
        context['performance_metrics'] = self.get_public_performance_metrics()
        
        return context
    
    def get_public_performance_metrics(self):
        """Get basic performance metrics for public view"""
        total_structures = Structure.objects.count()
        approved_structures = Structure.objects.filter(status='APPROVED').count()
        
        approval_rate = (approved_structures / total_structures * 100) if total_structures > 0 else 0
        
        return {
            'total_structures': total_structures,
            'approved_structures': approved_structures,
            'approval_rate': approval_rate,
            'entities_managed': Entity.objects.count(),
        }

