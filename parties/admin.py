from django.contrib import admin
from .models import Party, PartyRole, Passport, BeneficiaryRelation, DocumentAttachment


class PartyRoleInline(admin.TabularInline):
    model = PartyRole
    extra = 1
    fields = ['role_type', 'context', 'active']


class PassportInline(admin.TabularInline):
    model = Passport
    extra = 0
    fields = ['number', 'issuing_country', 'issued_at', 'expires_at', 'active']
    readonly_fields = ['created_at', 'updated_at']


class DocumentAttachmentInline(admin.TabularInline):
    model = DocumentAttachment
    extra = 0
    fields = ['document_type', 'url', 'description', 'active']


class BeneficiaryRelationInline(admin.TabularInline):
    model = BeneficiaryRelation
    fk_name = 'giver_party'
    extra = 0
    fields = ['beneficiary', 'percentage', 'conditions', 'effective_date', 'active']


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ['name', 'person_type', 'nationality', 'is_partner', 'active', 'created_at']
    list_filter = ['person_type', 'nationality', 'is_partner', 'active', 'created_at']
    search_fields = ['name', 'tax_identification_number', 'email']
    inlines = [PartyRoleInline, PassportInline, DocumentAttachmentInline, BeneficiaryRelationInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'person_type', 'is_partner')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code')
        }),
        ('Tax and Legal Information', {
            'fields': ('tax_identification_number', 'nationality', 'birth_date')
        }),
        ('Status', {
            'fields': ('active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PartyRole)
class PartyRoleAdmin(admin.ModelAdmin):
    list_display = ['party', 'role_type', 'context', 'active', 'created_at']
    list_filter = ['role_type', 'active', 'created_at']
    search_fields = ['party__name', 'context']
    
    fieldsets = (
        ('Role Information', {
            'fields': ('party', 'role_type', 'context', 'active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Passport)
class PassportAdmin(admin.ModelAdmin):
    list_display = ['party', 'number', 'issuing_country', 'expires_at', 'is_expiring_soon_display', 'active']
    list_filter = ['issuing_country', 'active', 'expires_at']
    search_fields = ['party__name', 'number']
    
    def is_expiring_soon_display(self, obj):
        return obj.is_expiring_soon()
    is_expiring_soon_display.boolean = True
    is_expiring_soon_display.short_description = 'Expiring Soon'
    
    fieldsets = (
        ('Passport Information', {
            'fields': ('party', 'number', 'issuing_country')
        }),
        ('Dates', {
            'fields': ('issued_at', 'expires_at')
        }),
        ('Status', {
            'fields': ('active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(BeneficiaryRelation)
class BeneficiaryRelationAdmin(admin.ModelAdmin):
    list_display = ['get_giver_display', 'beneficiary', 'percentage', 'effective_date', 'active']
    list_filter = ['active', 'effective_date', 'created_at']
    search_fields = ['giver_party__name', 'giver_entity__name', 'beneficiary__name']
    
    def get_giver_display(self, obj):
        if obj.giver_party:
            return f"Party: {obj.giver_party.name}"
        elif obj.giver_entity:
            return f"Entity: {obj.giver_entity.name}"
        return "No Giver"
    get_giver_display.short_description = 'Giver'
    
    fieldsets = (
        ('Giver Information', {
            'fields': ('giver_party', 'giver_entity'),
            'description': 'Select exactly one giver (Party or Entity)'
        }),
        ('Beneficiary Information', {
            'fields': ('beneficiary', 'percentage')
        }),
        ('Conditions', {
            'fields': ('conditions', 'effective_date')
        }),
        ('Status', {
            'fields': ('active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(DocumentAttachment)
class DocumentAttachmentAdmin(admin.ModelAdmin):
    list_display = ['party', 'document_type', 'description', 'active', 'uploaded_at']
    list_filter = ['document_type', 'active', 'uploaded_at']
    search_fields = ['party__name', 'description']
    
    fieldsets = (
        ('Document Information', {
            'fields': ('party', 'document_type', 'url', 'description')
        }),
        ('Status', {
            'fields': ('active',)
        }),
        ('Metadata', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['uploaded_at']

