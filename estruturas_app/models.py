from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date
import json

class Estrutura(models.Model):
    """
    Model representing legal structures available in the SIRIUS system.
    Each structure contains detailed information about costs, tax implications,
    privacy impacts, and operational requirements.
    
    NOTE: This model is kept for backward compatibility.
    New applications should use corporate.Structure instead.
    """
    
    TIPOS_ESTRUTURA = [
        ('TRUST', 'Trust'),
        ('FOREIGN_TRUST', 'Foreign Trust'),
        ('FUND', 'Fund'),
        ('IBC', 'International Business Company'),
        ('LLC_DISREGARDED', 'LLC Disregarded Entity'),
        ('LLC_PARTNERSHIP', 'LLC Partnership'),
        ('LLC_AS_CORP', 'LLC as a Corp'),
        ('CORP', 'Corp'),
        ('WYOMING_FOUNDATION', 'Wyoming Statutory Foundation'),
    ]
    
    JURISDICOES = [
        ('US', 'United States'),
        ('BS', 'Bahamas'),
        ('BR', 'Brazil'),
        ('BZ', 'Belize'),
        ('VG', 'British Virgin Islands'),
        ('KY', 'Cayman Islands'),
        ('PA', 'Panama'),
    ]
    
    US_STATES = [
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), 
        ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), 
        ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'), 
        ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
        ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), 
        ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), 
        ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), 
        ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
        ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), 
        ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), 
        ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), 
        ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
        ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), 
        ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), 
        ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), 
        ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'), ('WY', 'Wyoming'), ('DC', 'District of Columbia'),
    ]
    
    BR_STATES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), 
        ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), 
        ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), 
        ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), 
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), 
        ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), 
        ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
    ]
    
    # Basic Information
    nome = models.CharField(max_length=100, help_text="Structure name")
    tipo = models.CharField(max_length=50, choices=TIPOS_ESTRUTURA, 
                          help_text="Structure type")
    descricao = models.TextField(help_text="Detailed description of the structure")
    
    # Jurisdiction Information
    jurisdicao = models.CharField(
        max_length=10, 
        choices=JURISDICOES, 
        default='US',
        help_text="Primary jurisdiction"
    )
    estado_us = models.CharField(
        max_length=10, 
        choices=US_STATES, 
        blank=True, 
        null=True,
        help_text="US State (only if jurisdiction is United States)"
    )
    estado_br = models.CharField(
        max_length=10, 
        choices=BR_STATES, 
        blank=True, 
        null=True,
        help_text="Brazilian State (only if jurisdiction is Brazil)"
    )
    
    # Cost Information
    custo_base = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Base setup cost in USD"
    )
    custo_manutencao = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Annual maintenance cost in USD"
    )
    
    # Implementation Details
    tempo_implementacao = models.IntegerField(
        help_text="Implementation time in days",
        validators=[MinValueValidator(1), MaxValueValidator(365)]
    )
    complexidade = models.IntegerField(
        choices=[(i, f"Level {i}") for i in range(1, 6)],
        help_text="Complexity level from 1 (simple) to 5 (very complex)"
    )
    
    # Tax Impact Information
    impacto_tributario_eua = models.TextField(
        help_text="Detailed tax implications in the United States"
    )
    impacto_tributario_brasil = models.TextField(
        help_text="Detailed tax implications in Brazil"
    )
    impacto_tributario_outros = models.TextField(
        blank=True,
        help_text="Tax implications in other jurisdictions"
    )
    
    # Privacy and Asset Protection
    nivel_confidencialidade = models.IntegerField(
        choices=[(i, f"Level {i}") for i in range(1, 6)],
        help_text="Confidentiality level from 1 (low) to 5 (very high)"
    )
    protecao_patrimonial = models.IntegerField(
        choices=[(i, f"Level {i}") for i in range(1, 6)],
        help_text="Asset protection level from 1 (low) to 5 (very high)"
    )
    impacto_privacidade = models.TextField(
        help_text="Detailed privacy implications and protections"
    )
    
    # Operational Information
    facilidade_banking = models.IntegerField(
        choices=[(i, f"Level {i}") for i in range(1, 6)],
        help_text="Banking facility level from 1 (difficult) to 5 (very easy)"
    )
    documentacao_necessaria = models.TextField(
        help_text="Required documentation for setup"
    )
    
    # Document URLs
    url_documentos = models.URLField(
        blank=True,
        help_text="URL for structure documents and templates"
    )
    
    # Compliance and Reporting
    formularios_obrigatorios_eua = models.TextField(
        blank=True,
        help_text="Required US forms and reporting obligations"
    )
    formularios_obrigatorios_brasil = models.TextField(
        blank=True,
        help_text="Required Brazilian forms and reporting obligations"
    )
    
    # Status and Metadata
    ativo = models.BooleanField(default=True, 
                              help_text="Whether structure is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Legal Structure"
        verbose_name_plural = "Legal Structures"
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"
    
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
            5: "Very Complex"
        }
        return complexity_map.get(self.complexidade, "Unknown")
    
    def clean(self):
        """Validate jurisdiction and state combinations"""
        super().clean()
        
        # Validate US state is only set when jurisdiction is US
        if self.estado_us and self.jurisdicao != 'US':
            raise ValidationError({
                'estado_us': 'US State can only be set when jurisdiction is US'
            })
        
        # Validate BR state is only set when jurisdiction is BR
        if self.estado_br and self.jurisdicao != 'BR':
            raise ValidationError({
                'estado_br': 'Brazilian State can only be set when jurisdiction is Brazil'
            })
    
    def get_full_jurisdiction_display(self):
        """Get full jurisdiction including state if applicable"""
        jurisdiction = self.get_jurisdicao_display()
        
        if self.jurisdicao == 'US' and self.estado_us:
            state = dict(self.US_STATES).get(self.estado_us, self.estado_us)
            return f"{state}, {jurisdiction}"
        elif self.jurisdicao == 'BR' and self.estado_br:
            state = dict(self.BR_STATES).get(self.estado_br, self.estado_br)
            return f"{state}, {jurisdiction}"
        
        return jurisdiction
