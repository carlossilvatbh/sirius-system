from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import json


class Estrutura(models.Model):
    """
    Model representing legal structures available in the SIRIUS system.
    Each structure contains detailed information about costs, tax implications,
    privacy impacts, and operational requirements.
    """
    
    TIPOS_ESTRUTURA = [
        ('BDAO_SAC', 'Bahamas DAO SAC'),
        ('WYOMING_DAO_LLC', 'Wyoming DAO LLC'),
        ('BTS_VAULT', 'BTS Vault'),
        ('WYOMING_FOUNDATION', 'Wyoming Statutory Foundation'),
        ('WYOMING_CORP', 'Wyoming Corporation'),
        ('NATIONALIZATION', 'Nacionalização'),
        ('FUND_TOKEN', 'Fund Token as a Service'),
    ]
    
    # Basic Information
    nome = models.CharField(max_length=100, help_text="Structure name")
    tipo = models.CharField(max_length=50, choices=TIPOS_ESTRUTURA, help_text="Structure type")
    descricao = models.TextField(help_text="Detailed description of the structure")
    
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
    ativo = models.BooleanField(default=True, help_text="Whether structure is active")
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


class RegraValidacao(models.Model):
    """
    Model representing validation rules between different legal structures.
    Defines compatibility, requirements, and restrictions between structures.
    """
    
    TIPOS_RELACIONAMENTO = [
        ('REQUIRED', 'Required Combination'),
        ('RECOMMENDED', 'Recommended Combination'),
        ('INCOMPATIBLE', 'Incompatible Combination'),
        ('CONDITIONAL', 'Conditional Combination'),
        ('SYNERGISTIC', 'Synergistic Combination'),
    ]
    
    SEVERIDADE = [
        ('ERROR', 'Error - Blocks configuration'),
        ('WARNING', 'Warning - Potential issue'),
        ('INFO', 'Information - Suggestion'),
    ]
    
    estrutura_a = models.ForeignKey(
        Estrutura, 
        on_delete=models.CASCADE, 
        related_name='regras_como_a',
        help_text="First structure in the relationship"
    )
    estrutura_b = models.ForeignKey(
        Estrutura, 
        on_delete=models.CASCADE, 
        related_name='regras_como_b',
        help_text="Second structure in the relationship"
    )
    tipo_relacionamento = models.CharField(
        max_length=20, 
        choices=TIPOS_RELACIONAMENTO,
        help_text="Type of relationship between structures"
    )
    severidade = models.CharField(
        max_length=10,
        choices=SEVERIDADE,
        default='INFO',
        help_text="Severity level of the validation rule"
    )
    descricao = models.TextField(
        help_text="Detailed description of the validation rule"
    )
    condicoes = models.JSONField(
        blank=True, 
        null=True,
        help_text="JSON object containing specific conditions for the rule"
    )
    jurisdicao_aplicavel = models.CharField(
        max_length=100,
        blank=True,
        help_text="Specific jurisdiction where this rule applies"
    )
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Validation Rule"
        verbose_name_plural = "Validation Rules"
        unique_together = ['estrutura_a', 'estrutura_b', 'tipo_relacionamento']
    
    def __str__(self):
        return f"{self.estrutura_a.nome} -> {self.estrutura_b.nome} ({self.get_tipo_relacionamento_display()})"


class Template(models.Model):
    """
    Model representing pre-configured templates for specific business sectors.
    Templates contain complete structure configurations that can be reused.
    """
    
    CATEGORIAS = [
        ('TECH', 'Technology'),
        ('REAL_ESTATE', 'Real Estate'),
        ('TRADING', 'Trading'),
        ('FAMILY_OFFICE', 'Family Office'),
        ('INVESTMENT', 'Investment'),
        ('GENERAL', 'General'),
    ]
    
    COMPLEXIDADE_TEMPLATE = [
        ('BASIC', 'Basic Configuration'),
        ('INTERMEDIATE', 'Intermediate Configuration'),
        ('ADVANCED', 'Advanced Configuration'),
        ('EXPERT', 'Expert Configuration'),
    ]
    
    # Basic Information
    nome = models.CharField(max_length=100, help_text="Template name")
    categoria = models.CharField(
        max_length=20, 
        choices=CATEGORIAS,
        help_text="Business sector category"
    )
    complexidade_template = models.CharField(
        max_length=20,
        choices=COMPLEXIDADE_TEMPLATE,
        default='BASIC',
        help_text="Template complexity level"
    )
    descricao = models.TextField(help_text="Detailed template description")
    
    # Configuration Data
    configuracao = models.JSONField(
        help_text="Complete structure configuration saved as JSON"
    )
    
    # Cost and Time Information
    custo_total = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        help_text="Total cost for all structures in template"
    )
    tempo_total_implementacao = models.IntegerField(
        help_text="Total implementation time in days"
    )
    
    # Usage Statistics
    uso_count = models.IntegerField(
        default=0,
        help_text="Number of times this template has been used"
    )
    
    # Target Information
    publico_alvo = models.TextField(
        blank=True,
        help_text="Target audience description"
    )
    casos_uso = models.TextField(
        blank=True,
        help_text="Common use cases for this template"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Configuration Template"
        verbose_name_plural = "Configuration Templates"
        ordering = ['-uso_count', 'nome']
    
    def __str__(self):
        return f"{self.nome} ({self.get_categoria_display()})"
    
    def incrementar_uso(self):
        """Increment usage counter"""
        self.uso_count += 1
        self.save(update_fields=['uso_count'])
    
    def get_estruturas_incluidas(self):
        """Get list of structure IDs included in this template"""
        try:
            config = self.configuracao
            if isinstance(config, str):
                config = json.loads(config)
            
            elementos = config.get('elementos', [])
            return [elemento.get('estrutura_id') for elemento in elementos if elemento.get('estrutura_id')]
        except (json.JSONDecodeError, AttributeError):
            return []


class ConfiguracaoSalva(models.Model):
    """
    Model for saving user configurations that are not templates.
    Allows users to save work in progress.
    """
    
    nome = models.CharField(max_length=100, help_text="Configuration name")
    descricao = models.TextField(blank=True, help_text="Configuration description")
    configuracao = models.JSONField(help_text="Complete configuration data")
    
    # Cost and Time Information
    custo_estimado = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Estimated total cost"
    )
    tempo_estimado = models.IntegerField(
        null=True,
        blank=True,
        help_text="Estimated implementation time in days"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Saved Configuration"
        verbose_name_plural = "Saved Configurations"
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.nome


class AlertaJurisdicao(models.Model):
    """
    Model for jurisdiction-specific alerts and compliance requirements.
    """
    
    JURISDICOES = [
        ('US', 'United States'),
        ('BR', 'Brazil'),
        ('BS', 'Bahamas'),
        ('WY', 'Wyoming'),
        ('GLOBAL', 'Global/Multiple'),
    ]
    
    TIPOS_ALERTA = [
        ('TAX', 'Tax Obligation'),
        ('COMPLIANCE', 'Compliance Requirement'),
        ('REPORTING', 'Reporting Obligation'),
        ('DEADLINE', 'Important Deadline'),
        ('REGULATORY', 'Regulatory Change'),
    ]
    
    jurisdicao = models.CharField(
        max_length=10,
        choices=JURISDICOES,
        help_text="Applicable jurisdiction"
    )
    tipo_alerta = models.CharField(
        max_length=20,
        choices=TIPOS_ALERTA,
        help_text="Type of alert"
    )
    titulo = models.CharField(max_length=200, help_text="Alert title")
    descricao = models.TextField(help_text="Detailed alert description")
    
    # Applicability
    estruturas_aplicaveis = models.ManyToManyField(
        Estrutura,
        blank=True,
        help_text="Structures to which this alert applies"
    )
    
    # Priority and Status
    prioridade = models.IntegerField(
        choices=[(i, f"Priority {i}") for i in range(1, 6)],
        default=3,
        help_text="Alert priority from 1 (low) to 5 (critical)"
    )
    ativo = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Jurisdiction Alert"
        verbose_name_plural = "Jurisdiction Alerts"
        ordering = ['-prioridade', 'jurisdicao']
    
    def __str__(self):
        return f"{self.get_jurisdicao_display()}: {self.titulo}"




class UBO(models.Model):
    """
    Ultimate Beneficial Owner - Pessoa física proprietária ou beneficiária
    de Products ou Legal Structures
    """
    
    NACIONALIDADES = [
        ('BR', 'Brasil'),
        ('US', 'Estados Unidos'),
        ('BS', 'Bahamas'),
        ('KN', 'São Cristóvão e Nevis'),
        ('VG', 'Ilhas Virgens Britânicas'),
        ('PA', 'Panamá'),
        ('CH', 'Suíça'),
        ('SG', 'Singapura'),
        ('HK', 'Hong Kong'),
        ('OTHER', 'Outro'),
    ]
    
    # Campos obrigatórios
    nome_completo = models.CharField(
        max_length=200,
        help_text="Nome completo do Ultimate Beneficial Owner"
    )
    data_nascimento = models.DateField(
        help_text="Data de nascimento"
    )
    nacionalidade = models.CharField(
        max_length=10,
        choices=NACIONALIDADES,
        help_text="Nacionalidade do UBO"
    )
    tin = models.CharField(
        max_length=50,
        help_text="Tax Identification Number - número emitido pelo país de residência fiscal"
    )
    
    # Campos opcionais
    endereco_residencia_fiscal = models.TextField(
        blank=True,
        help_text="Endereço completo de residência fiscal"
    )
    telefone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Telefone de contato"
    )
    email = models.EmailField(
        blank=True,
        help_text="Email de contato"
    )
    observacoes = models.TextField(
        blank=True,
        help_text="Observações adicionais sobre o UBO"
    )
    
    # Metadados
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Ultimate Beneficial Owner"
        verbose_name_plural = "Ultimate Beneficial Owners"
        ordering = ['nome_completo']
        indexes = [
            models.Index(fields=['tin']),
            models.Index(fields=['nacionalidade']),
            models.Index(fields=['ativo']),
        ]
    
    def __str__(self):
        return f"{self.nome_completo} ({self.tin})"
    
    def clean(self):
        """Validações customizadas"""
        from django.core.exceptions import ValidationError
        import re
        
        super().clean()
        
        # Validação básica de TIN (pode ser expandida por país)
        if self.tin and not re.match(r'^[A-Z0-9\-]{5,20}$', self.tin.upper()):
            raise ValidationError({
                'tin': 'TIN deve conter apenas letras, números e hífens (5-20 caracteres)'
            })
    
    def get_products_associados(self):
        """Retorna todos os Products associados a este UBO"""
        # Implementação será expandida quando Product for refatorado
        return []
    
    def get_structures_associadas(self):
        """Retorna todas as Legal Structures associadas a este UBO"""
        # Implementação será expandida quando PersonalizedProduct for implementado
        return []




class Successor(models.Model):
    """
    Modelo para gestão de sucessão entre UBOs
    """
    
    # Relacionamentos
    ubo_proprietario = models.ForeignKey(
        UBO,
        on_delete=models.CASCADE,
        related_name='sucessores_definidos',
        help_text="UBO que está definindo a sucessão"
    )
    ubo_sucessor = models.ForeignKey(
        UBO,
        on_delete=models.CASCADE,
        related_name='sucessoes_recebidas',
        help_text="UBO que receberá a sucessão"
    )
    
    # Campos de sucessão
    percentual = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(100.00)],
        help_text="Percentual que o sucessor receberá (0.01 a 100.00)"
    )
    data_definicao = models.DateTimeField(
        auto_now_add=True,
        help_text="Data em que a sucessão foi definida"
    )
    data_efetivacao = models.DateField(
        null=True,
        blank=True,
        help_text="Data em que a sucessão deve ser efetivada (opcional)"
    )
    condicoes = models.TextField(
        blank=True,
        help_text="Condições específicas para a sucessão"
    )
    
    # Produto específico (opcional) - usando string para referência forward
    # personalized_product será implementado na Fase 4
    # personalized_product = models.ForeignKey(
    #     'PersonalizedProduct',
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    #     help_text="Produto específico sendo transferido (se aplicável)"
    # )
    
    # Status
    ativo = models.BooleanField(default=True)
    efetivado = models.BooleanField(default=False)
    data_efetivacao_real = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Data real em que a sucessão foi efetivada"
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Successor"
        verbose_name_plural = "Successors"
        ordering = ['-data_definicao']
        unique_together = ['ubo_proprietario', 'ubo_sucessor']
        indexes = [
            models.Index(fields=['ubo_proprietario', 'ativo']),
            models.Index(fields=['data_efetivacao']),
        ]
    
    def __str__(self):
        return f"{self.ubo_proprietario.nome_completo} → {self.ubo_sucessor.nome_completo} ({self.percentual}%)"
    
    def clean(self):
        """Validações customizadas"""
        from django.core.exceptions import ValidationError
        
        super().clean()
        
        # Validar que sucessor não é o mesmo que proprietário
        if self.ubo_proprietario == self.ubo_sucessor:
            raise ValidationError("UBO não pode ser sucessor de si mesmo")
        
        # Validar soma de percentuais para o mesmo proprietário
        if self.pk:
            outros_sucessores = Successor.objects.filter(
                ubo_proprietario=self.ubo_proprietario,
                ativo=True
            ).exclude(pk=self.pk)
        else:
            outros_sucessores = Successor.objects.filter(
                ubo_proprietario=self.ubo_proprietario,
                ativo=True
            )
        
        total_outros = sum(s.percentual for s in outros_sucessores)
        if total_outros + self.percentual > 100:
            raise ValidationError({
                'percentual': f'Soma dos percentuais excede 100%. Disponível: {100 - total_outros}%'
            })
    
    @classmethod
    def validar_percentuais_completos(cls, ubo_proprietario):
        """Valida se os percentuais de um UBO somam exatamente 100%"""
        total = cls.objects.filter(
            ubo_proprietario=ubo_proprietario,
            ativo=True
        ).aggregate(
            total=models.Sum('percentual')
        )['total'] or 0
        
        return abs(total - 100) < 0.01  # Tolerância para problemas de precisão decimal
    
    def get_percentual_disponivel(self):
        """Retorna o percentual ainda disponível para o UBO proprietário"""
        outros_sucessores = Successor.objects.filter(
            ubo_proprietario=self.ubo_proprietario,
            ativo=True
        ).exclude(pk=self.pk if self.pk else None)
        
        total_usado = sum(s.percentual for s in outros_sucessores)
        return 100 - total_usado

