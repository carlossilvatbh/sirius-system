from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from datetime import timedelta


class Entity(models.Model):
    """
    Represents a legal entity (formerly LegalStructure/Structure)
    Removed: description field (no longer needed)
    Modified: costs management moved to FINANCIAL_DEPARTMENT app
    Enhanced: template management in Implementation subsection
    """

    ENTITY_TYPES = [
        ("TRUST", "Trust"),
        ("FOREIGN_TRUST", "Foreign Trust"),
        ("FUND", "Fund"),
        ("IBC", "International Business Company"),
        ("LLC_DISREGARDED", "LLC Disregarded Entity"),
        ("LLC_PARTNERSHIP", "LLC Partnership"),
        ("LLC_AS_CORP", "LLC as a Corp"),
        ("CORP", "Corp"),
        ("WYOMING_FOUNDATION", "Wyoming Statutory Foundation"),
    ]

    TAX_CLASSIFICATION_CHOICES = [
        ("TRUST", "Trust"),
        ("FOREIGN_TRUST", "Foreign Trust"),
        ("FUND", "Fund"),
        ("US_CORP", "US Corp"),
        ("OFFSHORE_CORP", "Offshore Corp"),
        ("LLC_DISREGARDED_ENTITY", "LLC Disregarded Entity"),
        ("LLC_PARTNERSHIP", "LLC Partnership"),
        ("VIRTUAL_ASSET", "Virtual Asset"),
    ]

    JURISDICTIONS = [
        ("US", "United States"),
        ("BS", "Bahamas"),
        ("BR", "Brazil"),
        ("BZ", "Belize"),
        ("VG", "British Virgin Islands"),
        ("KY", "Cayman Islands"),
        ("PA", "Panama"),
    ]

    US_STATES = [
        ("AL", "Alabama"),
        ("AK", "Alaska"),
        ("AZ", "Arizona"),
        ("AR", "Arkansas"),
        ("CA", "California"),
        ("CO", "Colorado"),
        ("CT", "Connecticut"),
        ("DE", "Delaware"),
        ("FL", "Florida"),
        ("GA", "Georgia"),
        ("HI", "Hawaii"),
        ("ID", "Idaho"),
        ("IL", "Illinois"),
        ("IN", "Indiana"),
        ("IA", "Iowa"),
        ("KS", "Kansas"),
        ("KY", "Kentucky"),
        ("LA", "Louisiana"),
        ("ME", "Maine"),
        ("MD", "Maryland"),
        ("MA", "Massachusetts"),
        ("MI", "Michigan"),
        ("MN", "Minnesota"),
        ("MS", "Mississippi"),
        ("MO", "Missouri"),
        ("MT", "Montana"),
        ("NE", "Nebraska"),
        ("NV", "Nevada"),
        ("NH", "New Hampshire"),
        ("NJ", "New Jersey"),
        ("NM", "New Mexico"),
        ("NY", "New York"),
        ("NC", "North Carolina"),
        ("ND", "North Dakota"),
        ("OH", "Ohio"),
        ("OK", "Oklahoma"),
        ("OR", "Oregon"),
        ("PA", "Pennsylvania"),
        ("RI", "Rhode Island"),
        ("SC", "South Carolina"),
        ("SD", "South Dakota"),
        ("TN", "Tennessee"),
        ("TX", "Texas"),
        ("UT", "Utah"),
        ("VT", "Vermont"),
        ("VA", "Virginia"),
        ("WA", "Washington"),
        ("WV", "West Virginia"),
        ("WI", "Wisconsin"),
        ("WY", "Wyoming"),
        ("DC", "District of Columbia"),
    ]

    BR_STATES = [
        ("AC", "Acre"),
        ("AL", "Alagoas"),
        ("AP", "Amapá"),
        ("AM", "Amazonas"),
        ("BA", "Bahia"),
        ("CE", "Ceará"),
        ("DF", "Distrito Federal"),
        ("ES", "Espírito Santo"),
        ("GO", "Goiás"),
        ("MA", "Maranhão"),
        ("MT", "Mato Grosso"),
        ("MS", "Mato Grosso do Sul"),
        ("MG", "Minas Gerais"),
        ("PA", "Pará"),
        ("PB", "Paraíba"),
        ("PR", "Paraná"),
        ("PE", "Pernambuco"),
        ("PI", "Piauí"),
        ("RJ", "Rio de Janeiro"),
        ("RN", "Rio Grande do Norte"),
        ("RS", "Rio Grande do Sul"),
        ("RO", "Rondônia"),
        ("RR", "Roraima"),
        ("SC", "Santa Catarina"),
        ("SP", "São Paulo"),
        ("SE", "Sergipe"),
        ("TO", "Tocantins"),
    ]

    # Basic Information
    name = models.CharField(max_length=100, help_text="Entity name")
    entity_type = models.CharField(
        max_length=50,
        choices=ENTITY_TYPES,
        help_text="Type of legal entity",
        default="CORP",
    )

    # Tax classification
    tax_classification = models.CharField(
        max_length=50,
        choices=TAX_CLASSIFICATION_CHOICES,
        blank=True,
        help_text="Tax classification for this entity",
    )

    # Template Management (moved to Implementation subsection)
    implementation_templates = models.TextField(
        blank=True,
        help_text="Implementation templates (text format, not JSON)"
    )

    # Shares Information
    total_shares = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Total number of shares for this entity"
    )

    # Jurisdiction Information
    jurisdiction = models.CharField(
        max_length=10,
        choices=JURISDICTIONS,
        default="US",
        help_text="Primary jurisdiction",
    )
    us_state = models.CharField(
        max_length=10,
        choices=US_STATES,
        blank=True,
        null=True,
        help_text="US State (only if jurisdiction is United States)",
    )
    br_state = models.CharField(
        max_length=10,
        choices=BR_STATES,
        blank=True,
        null=True,
        help_text="Brazilian State (only if jurisdiction is Brazil)",
    )

    # Implementation Details
    implementation_time = models.IntegerField(
        help_text="Implementation time in days",
        validators=[MinValueValidator(1), MaxValueValidator(365)],
        default=30,
    )
    complexity = models.IntegerField(
        choices=[(i, f"Level {i}") for i in range(1, 6)],
        help_text="Complexity level from 1 (simple) to 5 (very complex)",
        default=3,
    )

    # Tax Impact Information
    tax_impact_usa = models.TextField(
        help_text="Detailed tax implications in the United States",
        default="To be determined",
    )
    tax_impact_brazil = models.TextField(
        help_text="Detailed tax implications in Brazil",
        default="To be determined",
    )
    tax_impact_others = models.TextField(
        blank=True, help_text="Tax implications in other jurisdictions"
    )

    # Privacy and Asset Protection
    confidentiality_level = models.IntegerField(
        choices=[(i, f"Level {i}") for i in range(1, 6)],
        help_text="Confidentiality level from 1 (low) to 5 (very high)",
        default=3,
    )
    asset_protection = models.IntegerField(
        choices=[(i, f"Level {i}") for i in range(1, 6)],
        help_text="Asset protection level from 1 (low) to 5 (very high)",
        default=3,
    )
    privacy_impact = models.TextField(
        help_text="Detailed privacy implications and protections",
        default="Standard privacy protections apply",
    )

    # Privacy Score (0-3) replaces privacy_score (0-100)
    privacy_score = models.IntegerField(
        choices=[(i, f"Level {i}") for i in range(0, 4)],
        help_text="Privacy score from 0 (lowest) to 3 (highest)",
        default=1,
    )

    # Banking Relation Score (1-3)
    banking_relation_score = models.IntegerField(
        choices=[(i, f"Level {i}") for i in range(1, 4)],
        help_text="Banking relationship difficulty from 1 (easy) to 3 (difficult)",
        default=2,
    )
    compliance_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Compliance score from 0 to 100",
        blank=True,
        null=True,
    )

    # Operational Information
    banking_facility = models.IntegerField(
        choices=[(i, f"Level {i}") for i in range(1, 6)],
        help_text="Banking facility level from 1 (difficult) to 5 (very easy)",
        default=3,
    )
    required_documentation = models.TextField(
        help_text="Required documentation for setup",
        default="Standard documentation required",
    )

    # Document URLs
    documents_url = models.URLField(
        blank=True, help_text="URL for entity documents and templates"
    )

    # Compliance and Reporting
    required_forms_usa = models.TextField(
        blank=True, help_text="Required US forms and reporting obligations"
    )
    required_forms_brazil = models.TextField(
        blank=True,
        help_text="Required Brazilian forms and reporting obligations",
    )

    # Status and Metadata
    active = models.BooleanField(
        default=True, help_text="Whether entity is active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Entity"
        verbose_name_plural = "Entities"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["jurisdiction"]),
            models.Index(fields=["active"]),
            models.Index(fields=["entity_type"]),
            models.Index(fields=["complexity"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_entity_type_display()})"

    def save(self, *args, **kwargs):
        """Auto-calculate privacy score from confidentiality_level if not set"""
        if self.confidentiality_level and not self.privacy_score:
            self.privacy_score = min(3, (self.confidentiality_level - 1))
        super().save(*args, **kwargs)

    def clean(self):
        """Validate jurisdiction and state combinations"""
        super().clean()

        # Validate US state is only set when jurisdiction is US
        if self.us_state and self.jurisdiction != "US":
            raise ValidationError(
                {"us_state": "US State can only be set when jurisdiction is US"}
            )

        # Validate BR state is only set when jurisdiction is BR
        if self.br_state and self.jurisdiction != "BR":
            raise ValidationError(
                {"br_state": "Brazilian State can only be set when jurisdiction is Brazil"}
            )

    def get_complexity_display_text(self):
        """Get human-readable complexity description"""
        complexity_map = {
            1: "Very Simple",
            2: "Simple",
            3: "Moderate",
            4: "Complex",
            5: "Very Complex",
        }
        return complexity_map.get(self.complexity, "Unknown")

    def get_full_jurisdiction_display(self):
        """Get full jurisdiction including state if applicable"""
        jurisdiction = self.get_jurisdiction_display()

        if self.jurisdiction == "US" and self.us_state:
            state = dict(self.US_STATES).get(self.us_state, self.us_state)
            return f"{state}, {jurisdiction}"
        elif self.jurisdiction == "BR" and self.br_state:
            state = dict(self.BR_STATES).get(self.br_state, self.br_state)
            return f"{state}, {jurisdiction}"

        return jurisdiction

    def get_tax_classification_display(self):
        """Return tax classification display name"""
        if self.tax_classification:
            return dict(self.TAX_CLASSIFICATION_CHOICES).get(
                self.tax_classification, self.tax_classification
            )
        return "Not set"

    def get_templates_list(self):
        """Return formatted list of templates"""
        if not self.implementation_templates:
            return []
        return [
            f"{template.get('name', 'Unknown')} ({template.get('url', 'No URL')})"
            for template in self.implementation_templates
        ]

    def get_privacy_score_display(self):
        """Get privacy score display"""
        score_map = {
            0: "Lowest Privacy",
            1: "Low Privacy",
            2: "Medium Privacy",
            3: "High Privacy",
        }
        return score_map.get(self.privacy_score, "Unknown")

    def get_banking_relation_display(self):
        """Get banking relation difficulty display"""
        score_map = {
            1: "Easy Banking",
            2: "Moderate Banking",
            3: "Difficult Banking",
        }
        return score_map.get(self.banking_relation_score, "Unknown")

    def get_compliance_level_display(self):
        """Get compliance level as percentage"""
        if self.compliance_score:
            return f"{self.compliance_score}%"
        return "Not set"


class Structure(models.Model):
    """
    Represents ownership hierarchies (corporate tree) among Entities and UBOs
    Purpose: Model complex corporate ownership structures
    """

    STATUS_CHOICES = [
        ('DRAFTING', 'Drafting'),
        ('SENT_FOR_APPROVAL', 'Sent for Approval'),
        ('APPROVED', 'Approved'),
    ]

    name = models.CharField(max_length=200, help_text="Structure name")
    description = models.TextField(help_text="Structure description")

    # Status Management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFTING')

    # Validation aggregated fields
    tax_impacts = models.TextField(
        blank=True,
        help_text="Aggregated tax impacts from validation rules"
    )
    severity_levels = models.TextField(
        blank=True,
        help_text="Aggregated severity levels from validation rules"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Structure"
        verbose_name_plural = "Structures"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        # Implement warning color for drafts in admin interface
        super().save(*args, **kwargs)
        
        if self.status == 'SENT_FOR_APPROVAL':
            # Trigger notification to approvers
            self.notify_approvers()

    def notify_approvers(self):
        """Implement notification system for approvers"""
        # TODO: Implement notification logic
        pass


class EntityOwnership(models.Model):
    """
    Manages ownership relationships within a Structure
    Handles both UBO → Entity and Entity → Entity ownership
    """

    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)

    # Owner can be either UBO or Entity
    owner_ubo = models.ForeignKey(
        'parties.Party', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE,
        help_text="UBO owner"
    )
    owner_entity = models.ForeignKey(
        Entity, 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name='owned_entities',
        help_text="Entity owner"
    )

    # Owned entity
    owned_entity = models.ForeignKey(
        Entity, 
        on_delete=models.CASCADE, 
        related_name='ownership_records'
    )

    # Share management
    total_shares = models.PositiveIntegerField(help_text="Total shares of the owned entity")
    owned_shares = models.PositiveIntegerField(help_text="Shares owned by this owner")
    ownership_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Ownership percentage (auto-calculated)"
    )

    # Share valuation (optional)
    share_value_usd = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.01)]
    )
    share_value_eur = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.01)]
    )

    # Corporate identification
    corporate_name = models.CharField(max_length=200, blank=True)
    hash_number = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Entity Ownership"
        verbose_name_plural = "Entity Ownerships"
        unique_together = ['structure', 'owner_ubo', 'owner_entity', 'owned_entity']
        indexes = [
            models.Index(fields=["structure"]),
            models.Index(fields=["owned_entity"]),
        ]

    def __str__(self):
        owner_name = ""
        if self.owner_ubo:
            owner_name = str(self.owner_ubo)
        elif self.owner_entity:
            owner_name = str(self.owner_entity)
        
        return f"{owner_name} owns {self.ownership_percentage}% of {self.owned_entity.name}"

    def clean(self):
        # Validate that exactly one owner type is specified
        if not (bool(self.owner_ubo) ^ bool(self.owner_entity)):
            raise ValidationError("Must specify exactly one owner (UBO or Entity)")

        # Validate share distribution totals 100%
        self.validate_share_distribution()

    def save(self, *args, **kwargs):
        # Auto-calculate percentage from shares
        if self.owned_shares and self.total_shares:
            self.ownership_percentage = (self.owned_shares / self.total_shares) * 100

        # Auto-calculate shares from percentage
        elif self.ownership_percentage and self.total_shares:
            self.owned_shares = int((self.ownership_percentage / 100) * self.total_shares)

        super().save(*args, **kwargs)

    def validate_share_distribution(self):
        """Ensure total ownership equals 100%"""
        total_ownership = EntityOwnership.objects.filter(
            structure=self.structure,
            owned_entity=self.owned_entity
        ).exclude(pk=self.pk).aggregate(
            total=models.Sum('ownership_percentage')
        )['total'] or 0

        if total_ownership + self.ownership_percentage > 100:
            raise ValidationError("Total ownership cannot exceed 100%")


class MasterEntity(models.Model):
    """
    Designates Master Entities (roots) of a Structure
    Only UBOs can own Master Entities
    """

    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Master Entity"
        verbose_name_plural = "Master Entities"
        unique_together = ['structure', 'entity']
        indexes = [
            models.Index(fields=["structure"]),
            models.Index(fields=["entity"]),
        ]

    def __str__(self):
        return f"{self.entity.name} (Master in {self.structure.name})"


class ValidationRule(models.Model):
    """
    Enhanced validation rules for entity combinations
    Removed: conditions field
    Renamed: structure_a → parent_entity, structure_b → related_entity
    Added: tax_impacts field
    """

    RELATIONSHIP_TYPES = [
        ("REQUIRED", "Required Combination"),
        ("RECOMMENDED", "Recommended Combination"),
        ("INCOMPATIBLE", "Incompatible Combination"),
        ("CONDITIONAL", "Conditional Combination"),
        ("SYNERGISTIC", "Synergistic Combination"),
    ]

    SEVERITY_CHOICES = [
        ("ERROR", "Error - Blocks configuration"),
        ("WARNING", "Warning - Potential issue"),
        ("INFO", "Information - Suggestion"),
    ]

    parent_entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name='parent_validation_rules'
    )
    related_entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name='related_validation_rules'
    )

    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    description = models.TextField()

    # New field for tax impact explanations
    tax_impacts = models.TextField(
        help_text="Detailed tax implications of this entity combination"
    )

    jurisdiction = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Validation Rule"
        verbose_name_plural = "Validation Rules"
        unique_together = ["parent_entity", "related_entity", "relationship_type"]
        indexes = [
            models.Index(fields=["parent_entity"]),
            models.Index(fields=["related_entity"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self):
        return f"{self.parent_entity.name} -> {self.related_entity.name} ({self.get_relationship_type_display()})"


# Keep existing models that don't need changes for now
# We'll update references in later phases

class UBO(models.Model):
    """
    Ultimate Beneficial Owner - represents the ultimate beneficial owners of structures
    This model will be migrated to parties.Party in Phase 3
    """

    TIPO_PESSOA = [
        ("FISICA", "Pessoa Física"),
        ("JURIDICA", "Pessoa Jurídica"),
    ]

    NACIONALIDADES = [
        ("BR", "Brasil"),
        ("US", "Estados Unidos"),
        ("BS", "Bahamas"),
        ("KN", "São Cristóvão e Nevis"),
        ("VG", "Ilhas Virgens Britânicas"),
        ("PA", "Panamá"),
        ("CH", "Suíça"),
        ("SG", "Singapura"),
        ("HK", "Hong Kong"),
        ("OTHER", "Outro"),
    ]

    # Basic Information (merged from both models)
    nome = models.CharField(max_length=200, help_text="Full name")
    nome_completo = models.CharField(
        max_length=200,
        blank=True,
        help_text="Nome completo do Ultimate Beneficial Owner",
    )
    tipo_pessoa = models.CharField(
        max_length=20,
        choices=TIPO_PESSOA,
        default="FISICA",
        help_text="Type of entity (individual or corporate)",
    )

    # Contact Information
    email = models.EmailField(blank=True, help_text="Email address")
    telefone = models.CharField(
        max_length=20, blank=True, help_text="Phone number"
    )

    # Address Information
    endereco = models.TextField(blank=True, help_text="Complete address")
    endereco_residencia_fiscal = models.TextField(
        blank=True, help_text="Endereço completo de residência fiscal"
    )
    cidade = models.CharField(max_length=100, blank=True, help_text="City")
    estado = models.CharField(
        max_length=100, blank=True, help_text="State/Province"
    )
    pais = models.CharField(max_length=100, blank=True, help_text="Country")
    cep = models.CharField(
        max_length=20, blank=True, help_text="ZIP/Postal Code"
    )

    # Identification
    documento_identidade = models.CharField(
        max_length=50, blank=True, help_text="Identity document number"
    )
    tipo_documento = models.CharField(
        max_length=50, blank=True, help_text="Type of identity document"
    )
    tin = models.CharField(
        max_length=50,
        blank=True,
        help_text="Tax Identification Number - número emitido pelo país de residência fiscal",
    )

    # Additional Information
    nacionalidade = models.CharField(
        max_length=10,
        choices=NACIONALIDADES,
        blank=True,
        help_text="Nationality",
    )
    data_nascimento = models.DateField(
        null=True, blank=True, help_text="Date of birth (for individuals)"
    )
    observacoes = models.TextField(
        blank=True, help_text="Observações adicionais sobre o UBO"
    )

    # Metadata
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "UBO (Ultimate Beneficial Owner)"
        verbose_name_plural = "UBOs (Ultimate Beneficial Owners)"
        ordering = ["nome"]
        indexes = [
            models.Index(fields=["tipo_pessoa"]),
            models.Index(fields=["tin"]),
            models.Index(fields=["nacionalidade"]),
            models.Index(fields=["ativo"]),
        ]

    def __str__(self):
        if self.tin:
            return f"{self.nome or self.nome_completo} ({self.tin})"
        return f"{self.nome or self.nome_completo} ({self.get_tipo_pessoa_display()})"

    def clean(self):
        """Validações customizadas"""
        super().clean()

        # Ensure at least one name field is filled
        if not self.nome and not self.nome_completo:
            raise ValidationError("At least one name field must be filled")

        # Sync nome and nome_completo if only one is filled
        if self.nome and not self.nome_completo:
            self.nome_completo = self.nome
        elif self.nome_completo and not self.nome:
            self.nome = self.nome_completo

        # Validação básica de TIN (pode ser expandida por país)
        if self.tin:
            import re

            if not re.match(r"^[A-Z0-9\-]{5,20}$", self.tin.upper()):
                raise ValidationError(
                    {
                        "tin": "TIN deve conter apenas letras, números e hífens (5-20 caracteres)"
                    }
                )

    def get_endereco_completo(self):
        """Retorna endereço completo formatado"""
        endereco_base = self.endereco or self.endereco_residencia_fiscal
        partes = [endereco_base, self.cidade, self.estado, self.pais, self.cep]
        return ", ".join([parte for parte in partes if parte])


class JurisdictionAlert(models.Model):
    """
    Model for jurisdiction-specific alerts and compliance requirements.
    Enhanced with deadline management, recurrence patterns, and service connections.
    """

    JURISDICOES = [
        ("US", "United States"),
        ("BR", "Brazil"),
        ("BS", "Bahamas"),
        ("WY", "Wyoming"),
        ("GLOBAL", "Global/Multiple"),
    ]

    TIPOS_ALERTA = [
        ("TAX", "Tax Obligation"),
        ("COMPLIANCE", "Compliance Requirement"),
        ("REPORTING", "Reporting Obligation"),
        ("DEADLINE", "Important Deadline"),
        ("REGULATORY", "Regulatory Change"),
        ("RENEWAL", "License/Registration Renewal"),
        ("FILING", "Required Filing"),
    ]

    DEADLINE_TYPES = [
        ("SINGLE", "Single Deadline"),
        ("RECURRING", "Recurring Deadline"),
    ]

    RECURRENCE_PATTERNS = [
        ("MONTHLY", "Monthly"),
        ("QUARTERLY", "Quarterly"),
        ("SEMIANUAL", "Semiannual"),
        ("ANNUAL", "Annual"),
        ("BIENNIAL", "Biennial"),
        ("CUSTOM", "Custom Pattern"),
    ]

    # Basic Information
    jurisdicao = models.CharField(
        max_length=10, choices=JURISDICOES, help_text="Applicable jurisdiction"
    )
    tipo_alerta = models.CharField(
        max_length=20, choices=TIPOS_ALERTA, help_text="Type of alert"
    )
    titulo = models.CharField(max_length=200, help_text="Alert title")
    descricao = models.TextField(help_text="Detailed alert description")

    # Applicability - Updated to use Entity instead of Structure
    estruturas_aplicaveis = models.ManyToManyField(
        Entity,
        blank=True,
        help_text="Entities to which this alert applies",
    )

    # Deadline Management
    deadline_type = models.CharField(
        max_length=20,
        choices=DEADLINE_TYPES,
        default="SINGLE",
        help_text="Type of deadline (single or recurring)",
    )
    single_deadline = models.DateField(
        null=True,
        blank=True,
        help_text="Single deadline date (for non-recurring alerts)",
    )
    recurrence_pattern = models.CharField(
        max_length=20,
        choices=RECURRENCE_PATTERNS,
        null=True,
        blank=True,
        help_text="Pattern for recurring deadlines",
    )
    next_deadline = models.DateField(
        null=True, blank=True, help_text="Next calculated deadline date"
    )
    last_completed = models.DateField(
        null=True,
        blank=True,
        help_text="Date when this alert was last completed",
    )

    # Templates and Links
    template_url = models.URLField(
        blank=True, help_text="URL to template or form for this alert"
    )
    compliance_url = models.URLField(
        blank=True, help_text="URL to compliance information or portal"
    )

    # Service Connection
    service_connection = models.ForeignKey(
        "corporate_relationship.Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Associated service for this alert",
    )

    # Advanced Configuration
    advance_notice_days = models.PositiveIntegerField(
        default=30, help_text="Days before deadline to trigger advance notice"
    )
    auto_calculate_next = models.BooleanField(
        default=True,
        help_text="Automatically calculate next deadline after completion",
    )
    custom_recurrence_config = models.JSONField(
        default=dict,
        blank=True,
        help_text="Custom configuration for complex recurrence patterns",
    )

    # Priority and Status
    prioridade = models.IntegerField(
        choices=[(i, f"Priority {i}") for i in range(1, 6)],
        default=3,
        help_text="Alert priority from 1 (low) to 5 (critical)",
    )
    ativo = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Jurisdiction Alert"
        verbose_name_plural = "Jurisdiction Alerts"
        ordering = ["-prioridade", "next_deadline", "jurisdicao"]
        indexes = [
            models.Index(fields=["jurisdicao", "tipo_alerta"]),
            models.Index(fields=["next_deadline"]),
            models.Index(fields=["deadline_type"]),
            models.Index(fields=["prioridade"]),
            models.Index(fields=["ativo"]),
        ]

    def __str__(self):
        return f"{self.get_jurisdicao_display()}: {self.titulo}"

    def clean(self):
        """Validate deadline configuration"""
        if self.deadline_type == "SINGLE":
            if not self.single_deadline:
                raise ValidationError(
                    "Single deadline date is required for single deadline type"
                )
            if self.recurrence_pattern:
                raise ValidationError(
                    "Recurrence pattern should not be set for single deadline type"
                )
        elif self.deadline_type == "RECURRING":
            if not self.recurrence_pattern:
                raise ValidationError(
                    "Recurrence pattern is required for recurring deadline type"
                )
            if self.single_deadline:
                raise ValidationError(
                    "Single deadline should not be set for recurring deadline type"
                )

    def calculate_next_deadline(self):
        """Calculate the next deadline based on recurrence pattern"""
        if self.deadline_type != "RECURRING" or not self.recurrence_pattern:
            return None

        from dateutil.relativedelta import relativedelta

        # Use last_completed as base, or current date if never completed
        base_date = self.last_completed or timezone.now().date()

        if self.recurrence_pattern == "MONTHLY":
            return base_date + relativedelta(months=1)
        elif self.recurrence_pattern == "QUARTERLY":
            return base_date + relativedelta(months=3)
        elif self.recurrence_pattern == "SEMIANUAL":
            return base_date + relativedelta(months=6)
        elif self.recurrence_pattern == "ANNUAL":
            return base_date + relativedelta(years=1)
        elif self.recurrence_pattern == "BIENNIAL":
            return base_date + relativedelta(years=2)
        elif self.recurrence_pattern == "CUSTOM":
            # Handle custom patterns from custom_recurrence_config
            config = self.custom_recurrence_config
            if "months" in config:
                return base_date + relativedelta(months=config["months"])
            elif "days" in config:
                return base_date + relativedelta(days=config["days"])

        return None

    def update_next_deadline(self):
        """Update the next_deadline field based on calculation"""
        if self.deadline_type == "SINGLE":
            self.next_deadline = self.single_deadline
        elif self.deadline_type == "RECURRING" and self.auto_calculate_next:
            self.next_deadline = self.calculate_next_deadline()

        self.save(update_fields=["next_deadline"])

    def mark_completed(self, completion_date=None):
        """Mark alert as completed and update next deadline"""
        completion_date = completion_date or timezone.now().date()
        self.last_completed = completion_date

        if self.deadline_type == "RECURRING" and self.auto_calculate_next:
            self.next_deadline = self.calculate_next_deadline()

        self.save(update_fields=["last_completed", "next_deadline"])

    def is_overdue(self):
        """Check if alert is overdue"""
        if not self.next_deadline:
            return False
        return timezone.now().date() > self.next_deadline

    def days_until_deadline(self):
        """Calculate days until next deadline"""
        if not self.next_deadline:
            return None
        delta = self.next_deadline - timezone.now().date()
        return delta.days

    def needs_advance_notice(self):
        """Check if advance notice should be triggered"""
        days_until = self.days_until_deadline()
        if days_until is None:
            return False
        return 0 <= days_until <= self.advance_notice_days

    def get_status_display(self):
        """Get human-readable status"""
        if self.is_overdue():
            return "Overdue"
        elif self.needs_advance_notice():
            return "Due Soon"
        elif self.next_deadline:
            return "Scheduled"
        else:
            return "No Deadline"

    def get_status_color(self):
        """Get color code for status display"""
        if self.is_overdue():
            return "#dc3545"  # Red
        elif self.needs_advance_notice():
            return "#ffc107"  # Yellow
        elif self.next_deadline:
            return "#28a745"  # Green
        else:
            return "#6c757d"  # Gray


class Successor(models.Model):
    """
    Modelo para gestão de sucessão entre UBOs
    This model will be migrated to parties.BeneficiaryRelation in Phase 3
    """

    # Relacionamentos
    ubo_proprietario = models.ForeignKey(
        UBO,
        on_delete=models.CASCADE,
        related_name="sucessores_definidos",
        help_text="UBO que está definindo a sucessão",
    )
    ubo_sucessor = models.ForeignKey(
        UBO,
        on_delete=models.CASCADE,
        related_name="sucessoes_recebidas",
        help_text="UBO que receberá a sucessão",
    )

    # Campos de sucessão
    percentual = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(100.00)],
        help_text="Percentual que o sucessor receberá (0.01 a 100.00)",
    )
    data_definicao = models.DateTimeField(
        auto_now_add=True, help_text="Data em que a sucessão foi definida"
    )
    data_efetivacao = models.DateField(
        null=True,
        blank=True,
        help_text="Data em que a sucessão deve ser efetivada (opcional)",
    )
    condicoes = models.TextField(
        blank=True, help_text="Condições específicas para a sucessão"
    )

    # Status
    ativo = models.BooleanField(default=True)
    efetivado = models.BooleanField(default=False)
    data_efetivacao_real = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Data real em que a sucessão foi efetivada",
    )

    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Successor"
        verbose_name_plural = "Successors"
        ordering = ["-data_definicao"]
        unique_together = ["ubo_proprietario", "ubo_sucessor"]
        indexes = [
            models.Index(fields=["ubo_proprietario", "ativo"]),
            models.Index(fields=["data_efetivacao"]),
        ]

    def __str__(self):
        return (
            f"{self.ubo_proprietario.nome} → {self.ubo_sucessor.nome} "
            f"({self.percentual}%)"
        )

    def clean(self):
        """Validações customizadas"""
        super().clean()

        # Validar que sucessor não é o mesmo que proprietário
        if self.ubo_proprietario == self.ubo_sucessor:
            raise ValidationError("UBO não pode ser sucessor de si mesmo")

        # Validar soma de percentuais para o mesmo proprietário
        if self.pk:
            outros_sucessores = Successor.objects.filter(
                ubo_proprietario=self.ubo_proprietario, ativo=True
            ).exclude(pk=self.pk)
        else:
            outros_sucessores = Successor.objects.filter(
                ubo_proprietario=self.ubo_proprietario, ativo=True
            )

        total_outros = sum(s.percentual for s in outros_sucessores)
        if total_outros + self.percentual > 100:
            raise ValidationError(
                {
                    "percentual": (
                        f"Soma dos percentuais excede 100%. "
                        f"Disponível: {100 - total_outros}%"
                    )
                }
            )


class StructureOwnership(models.Model):
    """
    Tabela de propriedade entre estruturas (N↔N não-simétrica).
    Mapeia participação societária de uma estrutura em outra.
    This model will be updated to use Entity instead of Structure in later phases
    """

    parent = models.ForeignKey(
        Entity,  # Updated to use Entity
        on_delete=models.CASCADE,
        related_name="owned_entities_legacy",
        help_text="Entity proprietária (parent)",
    )
    child = models.ForeignKey(
        Entity,  # Updated to use Entity
        on_delete=models.CASCADE,
        related_name="ownership_by_legacy",
        help_text="Entity possuída (child)",
    )
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(100.00)],
        help_text="Percentual de propriedade (0.01 a 100.00)",
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Structure Ownership (Legacy)"
        verbose_name_plural = "Structure Ownerships (Legacy)"
        unique_together = ["parent", "child"]
        ordering = ["-percentage"]

    def __str__(self):
        return (
            f"{self.parent.name} owns {self.percentage}% of "
            f"{self.child.name}"
        )

    def clean(self):
        """Validações customizadas"""
        super().clean()

        # Validar que parent não é o mesmo que child
        if self.parent == self.child:
            raise ValidationError("Entity cannot own itself")

