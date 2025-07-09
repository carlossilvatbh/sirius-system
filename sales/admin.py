from django.contrib import admin
from .models import Partner, Contact, StructureRequest, StructureApproval


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1
    fields = ['name', 'role', 'phone', 'email']


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'partnership_status', 'partnership_start_date']
    list_filter = ['partnership_status', 'partnership_start_date']
    search_fields = ['company_name', 'party__name']
    inlines = [ContactInline]
    fieldsets = [
        ('Basic Information', {
            'fields': ['party', 'company_name', 'address']
        }),
        ('Partnership Details', {
            'fields': ['partnership_status']
        }),
    ]
    ordering = ['company_name']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'partner', 'email', 'phone']
    list_filter = ['role', 'partner']
    search_fields = ['name', 'email', 'partner__company_name']
    fieldsets = [
        ('Contact Information', {
            'fields': ['partner', 'name', 'role']
        }),
        ('Contact Details', {
            'fields': ['email', 'phone']
        }),
    ]
    ordering = ['partner', 'name']


@admin.register(StructureRequest)
class StructureRequestAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status', 'submitted_at', 'get_requesting_parties']
    list_filter = ['status', 'submitted_at']
    search_fields = ['description']
    filter_horizontal = ['requesting_parties']
    fieldsets = [
        ('Request Details', {
            'fields': ['description', 'requesting_parties']
        }),
        ('Point of Contact', {
            'fields': ['point_of_contact_party', 'point_of_contact_partner', 'point_of_contact_contact']
        }),
        ('Status', {
            'fields': ['status']
        }),
    ]
    ordering = ['-submitted_at']
    readonly_fields = ['submitted_at', 'updated_at']

    def get_requesting_parties(self, obj):
        return ", ".join([party.name for party in obj.requesting_parties.all()[:3]])
    get_requesting_parties.short_description = 'Requesting Parties'


@admin.register(StructureApproval)
class StructureApprovalAdmin(admin.ModelAdmin):
    list_display = ['structure', 'action', 'action_date', 'processed_by']
    list_filter = ['action', 'action_date']
    search_fields = ['structure__name']
    fieldsets = [
        ('Structure Information', {
            'fields': ['structure']
        }),
        ('Approval Action', {
            'fields': ['action']
        }),
        ('Action Details', {
            'fields': ['approver', 'final_price', 'correction_comment', 'rejector', 'rejection_reason']
        }),
        ('Processing Information', {
            'fields': ['processed_by']
        }),
    ]
    ordering = ['-action_date']
    readonly_fields = ['action_date']


# Note: Legacy models (Product, ProductHierarchy, PersonalizedProduct) are kept in models.py
# but not registered in admin to avoid confusion. They will be migrated in future phases.

