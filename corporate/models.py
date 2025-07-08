from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Structure(models.Model):
    """
    Model representing legal structures available in the SIRIUS system.
    Each structure contains detailed information about costs, tax implications,
    privacy impacts, and operational requirements.

    This model combines the comprehensive features from Legal Structures
    (Estrutura) with enhanced corporate features for a complete solution.
    """

    TIPOS_ESTRUTURA = [
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

    # Nova classificação fiscal como campo de texto (substitui
    # TaxClassification)
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

    JURISDICOES = [
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
    nome = models.CharField(max_length=100, help_text="Structure name")
    tipo = models.CharField(
        max_length=50,
        choices=TIPOS_ESTRUTURA,
        help_text="Structure type",
        default="CORP",
    )

    # Nova classificação fiscal (substitui ManyToMany TaxClassification)
    tax_classification = models.CharField(
        max_length=50,
        choices=TAX_CLASSIFICATION_CHOICES,
        blank=True,
        help_text="Tax classification for this structure",
    )

    descricao = models.TextField(
        help_text="Detailed description of the structure"
    )

    # Templates (substitui campo implementation)
    templates = models.JSONField(
        default=list,
        help_text=(
            "List of templates: [{'name': 'Template Name', "
            "'url': 'http://...'}]"
        ),
    )

    # Jurisdiction Information
    jurisdicao = models.CharField(
        max_length=10,
        choices=JURISDICOES,
        default="US",
        help_text="Primary jurisdiction",
    )
    estado_us = models.CharField(
        max_length=10,
        choices=US_STATES,
        blank=True,
        null=True,
        help_text="US State (only if jurisdiction is United States)",
    )
    estado_br = models.CharField(
        max_length=10,
        choices=BR_STATES,
        blank=True,
        null=True,
        help_text="Brazilian State (only if jurisdiction is Brazil)",
    )

    # Cost Information
    custo_base = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Base setup cost in USD"
    )
    custo_manutencao = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Annual maintenance cost in USD",
    )

    # Implementation Details
    tempo_implementacao = models.IntegerField(
        help_text="Implementation time in days",
        validators=[MinValueValidator(1), MaxValueValidator(365)],
        default=30,
    )
    complexidade = models.IntegerField(
        choices=[(i, f"Level {i}") for i in range(1, 6)],
        help_text="Complexity level from 1 (simple) to 5 (very complex)",
        default=3,
    )

    # Tax Impact Information
    impacto_tributario_eua = models.TextField(
        help_text="Detailed tax implications in the United States",
        default="To be determined",
    )
    impacto_tributario_brasil = models.TextField(
        help_text="Detailed tax implications in Brazil",
        default="To be determined",
    )
    impacto_tributario_outros = models.TextField(
        blank=True, help_text="Tax implications in other jurisdictions"
    )

    # Privacy and Asset Protection
    nivel_confidencialidade = models.IntegerField(
        choices=[(i, f"Level {i}") for i in range(1, 6)],
        help_text="Confidentiality level from 1 (low) to 5 (very high)",
        default=3,
    )
    protecao_patrimonial = models.IntegerField(
        choices=[(i, f"Level {i}") for i in range(1, 6)],
        help_text="Asset protection level from 1 (low) to 5 (very high)",
        default=3,
    )
    impacto_privacidade = models.TextField(
        help_text="Detailed privacy implications and protections",
        default="Standard privacy protections apply",
    )

    # Novo: Privacy Score discreto (0-3) substitui privacidade_score (0-100)
    privacy_score = models.IntegerField(
        choices=[(i, f"Level {i}") for i in range(0, 4)],
        help_text="Privacy score from 0 (lowest) to 3 (highest)",
        default=1,
    )

    # Novo: Banking Relation Score (1-3)
    banking_relation_score = models.IntegerField(
        choices=[(i, f"Level {i}") for i in range(1, 4)],
        help_text=(
            "Banking relationship difficulty from 1 (easy) to 3 (difficult)"
        ),
        default=2,
    )
    compliance_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Compliance score from 0 to 100",
        blank=True,
        null=True,
    )

    # Operational Information
    facilidade_banking = models.IntegerField(
        choices=[(i, f"Level {i}") for i in range(1, 6)],
        help_text="Banking facility level from 1 (difficult) to 5 (very easy)",
        default=3,
    )
    documentacao_necessaria = models.TextField(
        help_text="Required documentation for setup",
        default="Standard documentation required",
    )
    documentos_necessarios = models.TextField(
        blank=True,
        help_text="Additional required documents for setup (legacy field)",
    )

    # Document URLs
    url_documentos = models.URLField(
        blank=True, help_text="URL for structure documents and templates"
    )

    # Compliance and Reporting
    formularios_obrigatorios_eua = models.TextField(
        blank=True, help_text="Required US forms and reporting obligations"
    )
    formularios_obrigatorios_brasil = models.TextField(
        blank=True,
        help_text="Required Brazilian forms and reporting obligations",
    )

    # Status and Metadata
    ativo = models.BooleanField(
        default=True, help_text="Whether structure is active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Legal Structure"
        verbose_name_plural = "Legal Structures"
        ordering = ["nome"]
        indexes = [
            models.Index(fields=["jurisdicao"]),
            models.Index(fields=["ativo"]),
            models.Index(fields=["tipo"]),
            models.Index(fields=["complexidade"]),
        ]

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

    def save(self, *args, **kwargs):
        """Auto-calculate privacy score from nivel_confidencialidade if not
        set"""
        if self.nivel_confidencialidade and not self.privacy_score:
            self.privacy_score = min(
                3, (self.nivel_confidencialidade - 1)
            )  # Convert 1-5 to 0-3
        super().save(*args, **kwargs)

    def clean(self):
        """Validate jurisdiction and state combinations"""
        super().clean()

        # Validate US state is only set when jurisdiction is US
        if self.estado_us and self.jurisdicao != "US":
            raise ValidationError(
                {
                    "estado_us": (
                        "US State can only be set when jurisdiction is US"
                    )
                }
            )

        # Validate BR state is only set when jurisdiction is BR
        if self.estado_br and self.jurisdicao != "BR":
            raise ValidationError(
                {
                    "estado_br": (
                        "Brazilian State can only be set when jurisdiction is "
                        "Brazil"
                    )
                }
            )

        # Consolidate documentation fields
        if self.documentos_necessarios and not self.documentacao_necessaria:
            self.documentacao_necessaria = self.documentos_necessarios

    def get_custo_total_primeiro_ano(self):
        """Calculate total first year cost including setup and maintenance"""
        return self.custo_base + self.custo_manutencao

    def get_complexity_display_text(self):
        """Get human-readable complexity description"""
        complexity_map = {
            1: "Very Simple",
            2: "Simple",
            3: "Moderate",
            4: "Complex",
            5: "Very Complex",
        }
        return complexity_map.get(self.complexidade, "Unknown")

    def get_full_jurisdiction_display(self):
        """Get full jurisdiction including state if applicable"""
        jurisdiction = self.get_jurisdicao_display()

        if self.jurisdicao == "US" and self.estado_us:
            state = dict(self.US_STATES).get(self.estado_us, self.estado_us)
            return f"{state}, {jurisdiction}"
        elif self.jurisdicao == "BR" and self.estado_br:
            state = dict(self.BR_STATES).get(self.estado_br, self.estado_br)
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
        if not self.templates:
            return []
        return [
            f"{template.get('name', 'Unknown')} ({template.get('url', 'No URL')})"
            for template in self.templates
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


class UBO(models.Model):
    """
    Ultimate Beneficial Owner - represents the ultimate beneficial owners of structures
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

    def get_products_associados(self):
        """Retorna todos os Products associados a este UBO"""
        from sales.models import PersonalizedProduct

        return PersonalizedProduct.objects.filter(ubos=self, ativo=True)

    def get_structures_associadas(self):
        """Retorna todas as Legal Structures associadas a este UBO"""
        structures = []
        for pp in self.get_products_associados():
            if pp.base_structure:
                structures.append(pp.base_structure)
            elif pp.base_product:
                # Get structures from product hierarchies
                for hierarchy in pp.base_product.producthierarchy_set.all():
                    structures.append(hierarchy.structure)
        return list(set(structures))  # Remove duplicates


class ValidationRule(models.Model):
    """
    Model representing validation rules between different legal structures.
    Defines compatibility, requirements, and restrictions between structures.
    """

    TIPOS_RELACIONAMENTO = [
        ("REQUIRED", "Required Combination"),
        ("RECOMMENDED", "Recommended Combination"),
        ("INCOMPATIBLE", "Incompatible Combination"),
        ("CONDITIONAL", "Conditional Combination"),
        ("SYNERGISTIC", "Synergistic Combination"),
    ]

    SEVERIDADE = [
        ("ERROR", "Error - Blocks configuration"),
        ("WARNING", "Warning - Potential issue"),
        ("INFO", "Information - Suggestion"),
    ]

    estrutura_a = models.ForeignKey(
        Structure,
        on_delete=models.CASCADE,
        related_name="regras_como_a",
        help_text="First structure in the relationship",
    )
    estrutura_b = models.ForeignKey(
        Structure,
        on_delete=models.CASCADE,
        related_name="regras_como_b",
        help_text="Second structure in the relationship",
    )
    tipo_relacionamento = models.CharField(
        max_length=20,
        choices=TIPOS_RELACIONAMENTO,
        help_text="Type of relationship between structures",
    )
    severidade = models.CharField(
        max_length=10,
        choices=SEVERIDADE,
        default="INFO",
        help_text="Severity level of the validation rule",
    )
    descricao = models.TextField(
        help_text="Detailed description of the validation rule"
    )
    condicoes = models.JSONField(
        blank=True,
        null=True,
        help_text="JSON object containing specific conditions for the rule",
    )
    jurisdicao_aplicavel = models.CharField(
        max_length=100,
        blank=True,
        help_text="Specific jurisdiction where this rule applies",
    )
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Validation Rule"
        verbose_name_plural = "Validation Rules"
        unique_together = ["estrutura_a", "estrutura_b", "tipo_relacionamento"]

    def __str__(self):
        return f"{self.estrutura_a.nome} -> {self.estrutura_b.nome} ({self.get_tipo_relacionamento_display()})"


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

    # Applicability
    estruturas_aplicaveis = models.ManyToManyField(
        Structure,
        blank=True,
        help_text="Structures to which this alert applies",
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

    def get_applicable_entities(self):
        """Get all entities (structures only) this alert applies to"""
        entities = []
        entities.extend(list(self.estruturas_aplicaveis.all()))
        # UBOs removed as per specification
        return entities

    def create_service_activity(
        self, activity_title=None, responsible_person=None
    ):
        """Create a ServiceActivity if this alert is connected to a service"""
        if not self.service_connection:
            return None

        # Import here to avoid circular import
        from corporate_relationship.models import ServiceActivity

        activity = ServiceActivity.objects.create(
            service=self.service_connection,
            activity_title=activity_title or f"Alert: {self.titulo}",
            activity_description=(
                f"Compliance activity for {self.titulo}. " f"{self.descricao}"
            ),
            start_date=timezone.now().date(),
            due_date=self.next_deadline,
            status="PLANNED",
            priority="HIGH" if self.prioridade >= 4 else "MEDIUM",
            responsible_person=responsible_person or "Compliance Team",
        )

        return activity


class Successor(models.Model):
    """
    Modelo para gestão de sucessão entre UBOs
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

    @classmethod
    def validar_percentuais_completos(cls, ubo_proprietario):
        """Valida se os percentuais de um UBO somam exatamente 100%"""
        total = (
            cls.objects.filter(
                ubo_proprietario=ubo_proprietario, ativo=True
            ).aggregate(total=models.Sum("percentual"))["total"]
            or 0
        )

        # Tolerância para problemas de precisão decimal
        return abs(total - 100) < 0.01

    def get_percentual_disponivel(self):
        """Retorna o percentual ainda disponível para o UBO proprietário"""
        outros_sucessores = Successor.objects.filter(
            ubo_proprietario=self.ubo_proprietario, ativo=True
        ).exclude(pk=self.pk if self.pk else None)

        total_usado = sum(s.percentual for s in outros_sucessores)
        return 100 - total_usado


class StructureOwnership(models.Model):
    """
    Tabela de propriedade entre estruturas (N↔N não-simétrica).
    Mapeia participação societária de uma estrutura em outra.
    """

    parent = models.ForeignKey(
        Structure,
        on_delete=models.CASCADE,
        related_name="owned_structures",
        help_text="Estrutura proprietária (parent)",
    )
    child = models.ForeignKey(
        Structure,
        on_delete=models.CASCADE,
        related_name="ownership_by",
        help_text="Estrutura possuída (child)",
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
        verbose_name = "Structure Ownership"
        verbose_name_plural = "Structure Ownerships"
        unique_together = ["parent", "child"]
        ordering = ["-percentage"]

    def __str__(self):
        return (
            f"{self.parent.nome} owns {self.percentage}% of "
            f"{self.child.nome}"
        )

    def clean(self):
        """Validações customizadas"""
        super().clean()

        # Validar que parent não é o mesmo que child
        if self.parent == self.child:
            raise ValidationError("Structure cannot own itself")

        # TODO: Validar ciclos na hierarquia de propriedade
        # FIXME: implementar detecção de ciclos para evitar loops infinitos
