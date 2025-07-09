from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from datetime import timedelta


class Party(models.Model):
    """
    Unified model for all persons/entities (formerly UBO)
    Handles both natural and juridical persons
    Enhanced with multiple roles and passport management
    """

    PERSON_TYPES = [
        ('NATURAL_PERSON', 'Natural Person'),
        ('JURIDICAL_PERSON', 'Juridical Person'),
    ]

    NATIONALITIES = [
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

    COUNTRIES = [
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

    person_type = models.CharField(max_length=20, choices=PERSON_TYPES)

    # Basic Information
    name = models.CharField(max_length=200, help_text="Full name")
    is_partner = models.BooleanField(default=False, help_text="Is this party a business partner?")

    # Contact Information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # Address Information
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    # Tax Information
    tax_identification_number = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Tax ID number from fiscal residence country"
    )

    # Basic Information (nationality and birth/incorporation date)
    nationality = models.CharField(max_length=10, choices=NATIONALITIES, blank=True)
    birth_date = models.DateField(
        null=True, 
        blank=True, 
        help_text="Birth date for natural persons, incorporation date for juridical persons"
    )

    # Metadata
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Party"
        verbose_name_plural = "Parties"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["person_type"]),
            models.Index(fields=["tax_identification_number"]),
            models.Index(fields=["nationality"]),
            models.Index(fields=["active"]),
            models.Index(fields=["is_partner"]),
        ]

    def __str__(self):
        if self.tax_identification_number:
            return f"{self.name} ({self.tax_identification_number})"
        return f"{self.name} ({self.get_person_type_display()})"

    def clean(self):
        """Validações customizadas"""
        super().clean()

        # Validação básica de TIN (pode ser expandida por país)
        if self.tax_identification_number:
            import re
            if not re.match(r"^[A-Z0-9\-]{5,20}$", self.tax_identification_number.upper()):
                raise ValidationError(
                    {
                        "tax_identification_number": "TIN deve conter apenas letras, números e hífens (5-20 caracteres)"
                    }
                )

    def get_full_address(self):
        """Retorna endereço completo formatado"""
        parts = [self.address, self.city, self.state, self.country, self.postal_code]
        return ", ".join([part for part in parts if part])


class PartyRole(models.Model):
    """
    Multiple roles/powers that a Party can have
    """

    ROLE_TYPES = [
        ('MANAGER', 'Manager'),
        ('HOLDER', 'Holder'),
        ('ULTIMATE_BENEFICIAL_OWNER', 'Ultimate Beneficial Owner'),
        ('BENEFICIARY', 'Beneficiary'),
        ('SETTLOR', 'Settlor'),
        ('PROTECTOR', 'Protector'),
        ('ATTORNEY', 'Attorney'),
        ('ADVISOR', 'Advisor'),
        ('TRUSTEE', 'Trustee'),
        ('CUSTODIAN', 'Custodian'),
    ]

    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='roles')
    role_type = models.CharField(max_length=30, choices=ROLE_TYPES)

    # Context information
    context = models.CharField(max_length=200, blank=True, help_text="Context where this role applies")
    active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Party Role"
        verbose_name_plural = "Party Roles"
        unique_together = ['party', 'role_type', 'context']
        indexes = [
            models.Index(fields=["party"]),
            models.Index(fields=["role_type"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self):
        context_str = f" ({self.context})" if self.context else ""
        return f"{self.party.name} - {self.get_role_type_display()}{context_str}"


class Passport(models.Model):
    """
    Multiple passport management for parties
    Includes expiration tracking and notifications
    """

    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='passports')
    number = models.CharField(max_length=50, help_text="Passport number")
    issued_at = models.DateField(help_text="Issue date")
    expires_at = models.DateField(help_text="Expiration date")

    # Issuing country
    issuing_country = models.CharField(max_length=10, choices=Party.COUNTRIES)

    active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Passport"
        verbose_name_plural = "Passports"
        ordering = ["-expires_at"]
        indexes = [
            models.Index(fields=["party"]),
            models.Index(fields=["expires_at"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self):
        return f"{self.party.name} - {self.number} ({self.get_issuing_country_display()})"

    def clean(self):
        # Validate expiration date is not in the past
        if self.expires_at and self.expires_at < timezone.now().date():
            raise ValidationError("Passport expiration date cannot be in the past")

    def is_expiring_soon(self, days=30):
        """Check if passport expires within specified days"""
        if not self.expires_at:
            return False
        return (self.expires_at - timezone.now().date()).days <= days

    @classmethod
    def get_expiring_passports(cls, days=30):
        """Get all passports expiring within specified days"""
        cutoff_date = timezone.now().date() + timedelta(days=days)
        return cls.objects.filter(
            expires_at__lte=cutoff_date,
            expires_at__gte=timezone.now().date(),
            active=True
        )


class BeneficiaryRelation(models.Model):
    """
    Manages beneficiary relationships (formerly Successor)
    Enhanced to handle Entity and UBO givers
    """

    # Giver can be Party, Entity, or UBO
    giver_party = models.ForeignKey(
        Party, 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE,
        related_name='given_benefits'
    )
    giver_entity = models.ForeignKey(
        'corporate.Entity',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='given_benefits'
    )

    # Beneficiary is always a Party
    beneficiary = models.ForeignKey(
        Party,
        on_delete=models.CASCADE,
        related_name='received_benefits'
    )

    # Percentage with validation
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(100.00)]
    )

    conditions = models.TextField(blank=True, help_text="Specific conditions for the benefit")
    effective_date = models.DateField(null=True, blank=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Beneficiary Relation"
        verbose_name_plural = "Beneficiary Relations"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["giver_party"]),
            models.Index(fields=["giver_entity"]),
            models.Index(fields=["beneficiary"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self):
        giver_name = ""
        if self.giver_party:
            giver_name = str(self.giver_party)
        elif self.giver_entity:
            giver_name = str(self.giver_entity)
        
        return f"{giver_name} → {self.beneficiary.name} ({self.percentage}%)"

    def clean(self):
        # Validate exactly one giver type
        giver_count = sum([bool(self.giver_party), bool(self.giver_entity)])
        if giver_count != 1:
            raise ValidationError("Must specify exactly one giver (Party or Entity)")

        # Validate total percentages don't exceed 100%
        self.validate_percentage_total()

    def validate_percentage_total(self):
        """Ensure total benefits from same giver don't exceed 100%"""
        if self.giver_party:
            total = BeneficiaryRelation.objects.filter(
                giver_party=self.giver_party,
                active=True
            ).exclude(pk=self.pk).aggregate(
                total=models.Sum('percentage')
            )['total'] or 0
        else:
            total = BeneficiaryRelation.objects.filter(
                giver_entity=self.giver_entity,
                active=True
            ).exclude(pk=self.pk).aggregate(
                total=models.Sum('percentage')
            )['total'] or 0

        if total + self.percentage > 100:
            raise ValidationError("Total benefits cannot exceed 100%")

    def save(self, *args, **kwargs):
        """Auto-create beneficiary role when saving (FASE 7)"""
        super().save(*args, **kwargs)
        
        # Automatically add role of beneficiary
        beneficiary_role, created = PartyRole.objects.get_or_create(
            party=self.beneficiary,
            role_type='BENEFICIARY',
            defaults={
                'context': f'Beneficiary of {self.get_giver_name()}',
                'active': True
            }
        )

    def get_giver_name(self):
        """Get name of the giver"""
        if self.giver_party:
            return self.giver_party.name
        elif self.giver_entity:
            return self.giver_entity.name
        return "Unknown"


class DocumentAttachment(models.Model):
    """
    Document management for parties
    URL-based document storage
    """

    DOCUMENT_TYPES = [
        ('PASSPORT', 'Passport'),
        ('PROOF_OF_INCOME', 'Proof of Income'),
        ('PROOF_OF_ADDRESS', 'Proof of Address'),
        ('POWER_OF_ATTORNEY', 'Power of Attorney'),
        ('MANAGEMENT_AGREEMENT', 'Management Agreement'),
        ('ADVISORY_AGREEMENT', 'Advisory Agreement'),
    ]

    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES)
    url = models.URLField(help_text="URL to the document (not uploaded to system)")

    # Metadata
    description = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Document Attachment"
        verbose_name_plural = "Document Attachments"
        ordering = ["-uploaded_at"]
        indexes = [
            models.Index(fields=["party"]),
            models.Index(fields=["document_type"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self):
        return f"{self.party.name} - {self.get_document_type_display()}"

