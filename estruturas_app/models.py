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


class AlertaJurisdicao(models.Model):
    """
    Model for jurisdiction-specific alerts and compliance requirements.
    Enhanced with deadline management, recurrence patterns, and service connections.
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
        ('RENEWAL', 'License/Registration Renewal'),
        ('FILING', 'Required Filing'),
    ]
    
    DEADLINE_TYPES = [
        ('SINGLE', 'Single Deadline'),
        ('RECURRING', 'Recurring Deadline'),
    ]
    
    RECURRENCE_PATTERNS = [
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('SEMIANNUAL', 'Semiannual'),
        ('ANNUAL', 'Annual'),
        ('BIENNIAL', 'Biennial'),
        ('CUSTOM', 'Custom Pattern'),
    ]
    
    # Basic Information
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
        'Estrutura',
        blank=True,
        help_text="Structures to which this alert applies"
    )
    
    # UBO Relationships (NEW)
    ubos_aplicaveis = models.ManyToManyField(
        'UBO',
        blank=True,
        help_text="UBOs to which this alert applies"
    )
    
    # Deadline Management (NEW)
    deadline_type = models.CharField(
        max_length=20,
        choices=DEADLINE_TYPES,
        default='SINGLE',
        help_text="Type of deadline (single or recurring)"
    )
    single_deadline = models.DateField(
        null=True,
        blank=True,
        help_text="Single deadline date (for non-recurring alerts)"
    )
    recurrence_pattern = models.CharField(
        max_length=20,
        choices=RECURRENCE_PATTERNS,
        null=True,
        blank=True,
        help_text="Pattern for recurring deadlines"
    )
    next_deadline = models.DateField(
        null=True,
        blank=True,
        help_text="Next calculated deadline date"
    )
    last_completed = models.DateField(
        null=True,
        blank=True,
        help_text="Date when this alert was last completed"
    )
    
    # Templates and Links (NEW)
    template_url = models.URLField(
        blank=True,
        help_text="URL to template or form for this alert"
    )
    compliance_url = models.URLField(
        blank=True,
        help_text="URL to compliance information or portal"
    )
    
    # Service Connection (NEW)
    service_connection = models.ForeignKey(
        'Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Associated service for this alert"
    )
    
    # Advanced Configuration (NEW)
    advance_notice_days = models.PositiveIntegerField(
        default=30,
        help_text="Days before deadline to trigger advance notice"
    )
    auto_calculate_next = models.BooleanField(
        default=True,
        help_text="Automatically calculate next deadline after completion"
    )
    custom_recurrence_config = models.JSONField(
        default=dict,
        help_text="Custom configuration for complex recurrence patterns"
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
        ordering = ['-prioridade', 'next_deadline', 'jurisdicao']
        indexes = [
            models.Index(fields=['jurisdicao', 'tipo_alerta']),
            models.Index(fields=['next_deadline']),
            models.Index(fields=['deadline_type']),
            models.Index(fields=['prioridade']),
            models.Index(fields=['ativo']),
        ]
    
    def __str__(self):
        return f"{self.get_jurisdicao_display()}: {self.titulo}"
    
    def clean(self):
        """Validate deadline configuration"""
        if self.deadline_type == 'SINGLE':
            if not self.single_deadline:
                raise ValidationError(
                    "Single deadline date is required for single deadline type"
                )
            if self.recurrence_pattern:
                raise ValidationError(
                    "Recurrence pattern should not be set for single deadline type"
                )
        elif self.deadline_type == 'RECURRING':
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
        if self.deadline_type != 'RECURRING' or not self.recurrence_pattern:
            return None
        
        from dateutil.relativedelta import relativedelta
        
        # Use last_completed as base, or current date if never completed
        base_date = self.last_completed or timezone.now().date()
        
        if self.recurrence_pattern == 'MONTHLY':
            return base_date + relativedelta(months=1)
        elif self.recurrence_pattern == 'QUARTERLY':
            return base_date + relativedelta(months=3)
        elif self.recurrence_pattern == 'SEMIANNUAL':
            return base_date + relativedelta(months=6)
        elif self.recurrence_pattern == 'ANNUAL':
            return base_date + relativedelta(years=1)
        elif self.recurrence_pattern == 'BIENNIAL':
            return base_date + relativedelta(years=2)
        elif self.recurrence_pattern == 'CUSTOM':
            # Handle custom patterns from custom_recurrence_config
            config = self.custom_recurrence_config
            if 'months' in config:
                return base_date + relativedelta(months=config['months'])
            elif 'days' in config:
                return base_date + relativedelta(days=config['days'])
        
        return None
    
    def update_next_deadline(self):
        """Update the next_deadline field based on calculation"""
        if self.deadline_type == 'SINGLE':
            self.next_deadline = self.single_deadline
        elif self.deadline_type == 'RECURRING' and self.auto_calculate_next:
            self.next_deadline = self.calculate_next_deadline()
        
        self.save(update_fields=['next_deadline'])
    
    def mark_completed(self, completion_date=None):
        """Mark alert as completed and update next deadline"""
        completion_date = completion_date or timezone.now().date()
        self.last_completed = completion_date
        
        if self.deadline_type == 'RECURRING' and self.auto_calculate_next:
            self.next_deadline = self.calculate_next_deadline()
        
        self.save(update_fields=['last_completed', 'next_deadline'])
    
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
            return '#dc3545'  # Red
        elif self.needs_advance_notice():
            return '#ffc107'  # Yellow
        elif self.next_deadline:
            return '#28a745'  # Green
        else:
            return '#6c757d'  # Gray
    
    def get_applicable_entities(self):
        """Get all entities (structures and UBOs) this alert applies to"""
        entities = []
        entities.extend(list(self.estruturas_aplicaveis.all()))
        entities.extend(list(self.ubos_aplicaveis.all()))
        return entities
    
    def create_service_activity(self, activity_title=None, responsible_person=None):
        """Create a ServiceActivity if this alert is connected to a service"""
        if not self.service_connection:
            return None
        
        from .models import ServiceActivity
        
        activity = ServiceActivity.objects.create(
            service=self.service_connection,
            activity_title=activity_title or f"Alert: {self.titulo}",
            activity_description=f"Compliance activity for {self.titulo}. {self.descricao}",
            start_date=timezone.now().date(),
            due_date=self.next_deadline,
            status='PLANNED',
            priority='HIGH' if self.prioridade >= 4 else 'MEDIUM',
            responsible_person=responsible_person or 'Compliance Team'
        )
        
        return activity




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



class Product(models.Model):
    """
    Produto comercial que conecta duas ou mais Legal Structures
    Refatoração do modelo Template existente
    """
    
    COMPLEXIDADE_PRODUCT = [
        ('BASIC', 'Basic Configuration'),
        ('INTERMEDIATE', 'Intermediate Configuration'),
        ('ADVANCED', 'Advanced Configuration'),
        ('EXPERT', 'Expert Configuration'),
    ]
    
    # Campos básicos (mantidos do Template)
    nome = models.CharField(max_length=100, help_text="Nome do produto")
    complexidade_template = models.CharField(
        max_length=20,
        choices=COMPLEXIDADE_PRODUCT,
        default='BASIC',
        help_text="Nível de complexidade"
    )
    descricao = models.TextField(help_text="Descrição detalhada do produto")
    
    # Novos campos comerciais
    commercial_name = models.CharField(
        max_length=200,
        help_text="Nome comercial do produto (texto livre)"
    )
    master_agreement_url = models.URLField(
        help_text="URL para documento de Master Agreement"
    )
    
    # Hierarquia de Legal Structures
    legal_structures = models.ManyToManyField(
        'Estrutura',
        through='ProductHierarchy',
        through_fields=('product', 'structure'),
        help_text="Legal structures included in this product"
    )
    
    # Configuração e custos
    configuracao = models.JSONField(
        help_text="Configuração completa do produto em JSON"
    )
    custo_automatico = models.BooleanField(
        default=True,
        help_text="Se True, custo é calculado automaticamente das estruturas"
    )
    custo_manual = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Custo manual (usado quando custo_automatico=False)"
    )
    
    # Campos mantidos do Template
    tempo_total_implementacao = models.IntegerField(
        help_text="Tempo total de implementação em dias"
    )
    uso_count = models.IntegerField(
        default=0,
        help_text="Número de vezes que este produto foi usado"
    )
    publico_alvo = models.TextField(
        blank=True,
        help_text="Público-alvo do produto"
    )
    casos_uso = models.TextField(
        blank=True,
        help_text="Casos de uso comuns"
    )
    
    # Metadados
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-uso_count', 'commercial_name']
        indexes = [
            models.Index(fields=['commercial_name']),
            models.Index(fields=['ativo']),
        ]
    
    def __str__(self):
        return f"{self.commercial_name} ({self.nome})"
    
    def get_custo_total_calculado(self):
        """Calcula custo total baseado nas estruturas hierárquicas"""
        if not self.custo_automatico:
            return self.custo_manual or 0
        
        # Por enquanto retorna 0, será implementado quando ProductHierarchy for criado
        # na Fase 4 (PersonalizedProduct)
        return 0
    
    def incrementar_uso(self):
        """Incrementa contador de uso"""
        self.uso_count += 1
        self.save(update_fields=['uso_count'])
    
    def get_estruturas_incluidas(self):
        """Retorna lista de IDs de estruturas incluídas neste produto"""
        try:
            config = self.configuracao
            if isinstance(config, str):
                import json
                config = json.loads(config)
            
            elementos = config.get('elementos', [])
            return [elemento.get('estrutura_id') for elemento in elementos if elemento.get('estrutura_id')]
        except (json.JSONDecodeError, AttributeError):
            return []
    
    def get_custo_total_primeiro_ano(self):
        """Calcula custo total do primeiro ano"""
        if self.custo_automatico:
            return self.get_custo_total_calculado()
        else:
            return self.custo_manual or 0


class ProductHierarchy(models.Model):
    """
    Modelo intermediário para gerenciar hierarquia de Legal Structures dentro de um Product
    """
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        help_text="Product to which this hierarchy belongs"
    )
    structure = models.ForeignKey(
        'Estrutura',
        on_delete=models.CASCADE,
        help_text="Legal Structure in this hierarchy"
    )
    parent_structure = models.ForeignKey(
        'Estrutura',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='child_structures',
        help_text="Parent structure (if this structure is owned by another)"
    )
    ownership_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.01), MaxValueValidator(100.00)],
        help_text="Percentage of ownership (optional)"
    )
    hierarchy_level = models.PositiveIntegerField(
        default=1,
        help_text="Level in hierarchy (1 = top level, 2 = second level, etc.)"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes about this hierarchy relationship"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Product Hierarchy"
        verbose_name_plural = "Product Hierarchies"
        unique_together = ['product', 'structure']
        indexes = [
            models.Index(fields=['product', 'hierarchy_level']),
            models.Index(fields=['structure']),
            models.Index(fields=['parent_structure']),
        ]
    
    def __str__(self):
        if self.parent_structure:
            return f"{self.product.commercial_name}: {self.parent_structure.nome} owns {self.structure.nome}"
        else:
            return f"{self.product.commercial_name}: {self.structure.nome} (Top Level)"
    
    def clean(self):
        """Validate hierarchy relationships"""
        super().clean()
        
        # A structure cannot be its own parent
        if self.parent_structure == self.structure:
            raise ValidationError("A structure cannot be its own parent")
        
        # Check for circular references
        if self.parent_structure:
            current = self.parent_structure
            visited = set()
            while current:
                if current == self.structure:
                    raise ValidationError("Circular reference detected in hierarchy")
                if current.id in visited:
                    break
                visited.add(current.id)
                # Find parent of current structure in the same product
                parent_rel = ProductHierarchy.objects.filter(
                    product=self.product,
                    structure=current
                ).first()
                current = parent_rel.parent_structure if parent_rel else None
    
    def get_children(self):
        """Get all direct children of this structure in the same product"""
        return ProductHierarchy.objects.filter(
            product=self.product,
            parent_structure=self.structure
        )
    
    def get_all_descendants(self):
        """Get all descendants (children, grandchildren, etc.) of this structure"""
        descendants = []
        children = self.get_children()
        for child in children:
            descendants.append(child)
            descendants.extend(child.get_all_descendants())
        return descendants
    
    def is_top_level(self):
        """Check if this structure is at the top level (no parent)"""
        return self.parent_structure is None
    
    def get_hierarchy_path(self):
        """Get the full path from top to this structure"""
        path = []
        current = self
        while current:
            path.insert(0, current.structure.nome)
            if current.parent_structure:
                current = ProductHierarchy.objects.filter(
                    product=current.product,
                    structure=current.parent_structure
                ).first()
            else:
                current = None
        return " → ".join(path)


class PersonalizedProduct(models.Model):
    """
    Produto personalizado que representa Products ou Legal Structures associadas a UBOs
    Refatoração do modelo ConfiguracaoSalva existente
    """
    
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('ARCHIVED', 'Archived'),
    ]
    
    # Informações básicas
    nome = models.CharField(
        max_length=200,
        help_text="Nome do produto personalizado"
    )
    descricao = models.TextField(
        blank=True,
        help_text="Descrição detalhada do produto personalizado"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT',
        help_text="Status atual do produto personalizado"
    )
    
    # Relacionamentos base (um dos dois deve ser preenchido)
    base_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Product base para este produto personalizado"
    )
    base_structure = models.ForeignKey(
        Estrutura,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Legal Structure base para este produto personalizado"
    )
    
    # Relacionamentos com UBOs - conexão direta
    ubos = models.ManyToManyField(
        UBO,
        blank=True,
        help_text="UBOs associated with this personalized product"
    )
    
    # Versionamento
    version_number = models.PositiveIntegerField(
        default=1,
        help_text="Número da versão (incrementado automaticamente)"
    )
    parent_version = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='child_versions',
        help_text="Versão anterior deste produto personalizado"
    )
    
    # Configuração personalizada
    configuracao_personalizada = models.JSONField(
        default=dict,
        help_text="Configurações específicas deste produto personalizado"
    )
    
    # Custos personalizados
    custo_personalizado = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Custo personalizado (sobrescreve cálculo automático)"
    )
    
    # Observações e notas
    observacoes = models.TextField(
        blank=True,
        help_text="Observações e notas específicas"
    )
    
    # Metadados
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Personalized Product"
        verbose_name_plural = "Personalized Products"
        ordering = ['-version_number', '-created_at']
        indexes = [
            models.Index(fields=['base_product']),
            models.Index(fields=['base_structure']),
            models.Index(fields=['status']),
            models.Index(fields=['version_number']),
            models.Index(fields=['ativo']),
        ]
    
    def __str__(self):
        base_name = ""
        if self.base_product:
            base_name = self.base_product.commercial_name
        elif self.base_structure:
            base_name = self.base_structure.nome
        
        return f"{self.nome} (v{self.version_number}) - {base_name}"
    
    def clean(self):
        """Validações customizadas"""
        super().clean()
        
        # Validar que apenas um dos campos base está preenchido
        if self.base_product and self.base_structure:
            raise ValidationError(
                "Produto personalizado deve ter apenas um base (Product ou Structure)"
            )
        
        if not self.base_product and not self.base_structure:
            raise ValidationError(
                "Produto personalizado deve ter um base (Product ou Structure)"
            )
    
    def get_base_object(self):
        """Retorna o objeto base (Product ou Structure)"""
        return self.base_product or self.base_structure
    
    def get_base_type(self):
        """Retorna o tipo do objeto base"""
        if self.base_product:
            return "Product"
        elif self.base_structure:
            return "Structure"
        return None
    
    def get_custo_total(self):
        """Calcula custo total considerando personalização"""
        if self.custo_personalizado:
            return self.custo_personalizado
        
        base_obj = self.get_base_object()
        if hasattr(base_obj, 'get_custo_total_primeiro_ano'):
            return base_obj.get_custo_total_primeiro_ano()
        elif hasattr(base_obj, 'get_custo_total_primeiro_ano'):
            return base_obj.get_custo_total_primeiro_ano()
        
        return 0
    
    def create_new_version(self, changes_description=""):
        """Cria nova versão deste produto personalizado"""
        new_version = PersonalizedProduct.objects.create(
            nome=self.nome,
            descricao=self.descricao,
            status='DRAFT',
            base_product=self.base_product,
            base_structure=self.base_structure,
            version_number=self.version_number + 1,
            parent_version=self,
            configuracao_personalizada=self.configuracao_personalizada.copy(),
            custo_personalizado=self.custo_personalizado,
            observacoes=f"{self.observacoes}\n\n--- Versão {self.version_number + 1} ---\n{changes_description}".strip()
        )
        
        # Copiar relacionamentos UBO
        new_version.ubos.set(self.ubos.all())
        
        return new_version
    
    def get_ubos_ativos(self):
        """Retorna UBOs ativos associados"""
        return self.ubos.filter(ativo=True)
    
    def get_first_level_structure(self):
        """Retorna a primeira estrutura da hierarquia para conexão com UBOs"""
        if self.base_structure:
            return self.base_structure
        elif self.base_product:
            # Busca a estrutura de primeiro nível (sem parent) no product
            try:
                first_level = ProductHierarchy.objects.filter(
                    product=self.base_product,
                    parent_structure__isnull=True
                ).first()
                return first_level.structure if first_level else None
            except:
                return None
        return None


class Service(models.Model):
    """
    Model representing services that can be associated with Products or Legal Structures.
    Services can be transformed into PersonalizedProducts when associated with specific entities.
    """
    
    SERVICE_TYPES = [
        ('LEGAL', 'Legal'),
        ('TAX', 'Tax'),
        ('COMPLIANCE', 'Compliance'),
        ('ADMINISTRATIVE', 'Administrative'),
        ('CONSULTING', 'Consulting'),
        ('FORMATION', 'Formation'),
        ('MAINTENANCE', 'Maintenance'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('DRAFT', 'Draft'),
        ('ARCHIVED', 'Archived'),
    ]
    
    # Basic Information
    service_name = models.CharField(
        max_length=200,
        help_text="Name of the service"
    )
    description = models.TextField(
        help_text="Detailed description of the service"
    )
    service_type = models.CharField(
        max_length=20,
        choices=SERVICE_TYPES,
        help_text="Type of service provided"
    )
    
    # Cost and Duration
    cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Cost of the service (optional)"
    )
    estimated_duration = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Estimated duration in days"
    )
    
    # Optional Associations
    associated_product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Product this service is associated with (optional)"
    )
    associated_structure = models.ForeignKey(
        'Estrutura',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Legal Structure this service is associated with (optional)"
    )
    
    # Service Configuration
    requirements = models.JSONField(
        default=dict,
        help_text="Service requirements and prerequisites"
    )
    deliverables = models.JSONField(
        default=dict,
        help_text="Expected deliverables and outcomes"
    )
    
    # Status and Metadata
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT',
        help_text="Current status of the service"
    )
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['service_name']
        indexes = [
            models.Index(fields=['service_type']),
            models.Index(fields=['status']),
            models.Index(fields=['associated_product']),
            models.Index(fields=['associated_structure']),
            models.Index(fields=['ativo']),
        ]
    
    def __str__(self):
        return f"{self.service_name} ({self.get_service_type_display()})"
    
    def clean(self):
        """Validate that service has at most one association"""
        if self.associated_product and self.associated_structure:
            raise ValidationError(
                "Service cannot be associated with both Product and Structure simultaneously"
            )
    
    def get_association_type(self):
        """Return the type of association (Product, Structure, or None)"""
        if self.associated_product:
            return "Product"
        elif self.associated_structure:
            return "Structure"
        return "Standalone"
    
    def get_associated_object(self):
        """Return the associated object (Product or Structure)"""
        if self.associated_product:
            return self.associated_product
        elif self.associated_structure:
            return self.associated_structure
        return None
    
    def create_personalized_service(self, ubos=None, custom_config=None):
        """
        Create a PersonalizedProduct based on this Service.
        This method transforms a Service into a PersonalizedProduct when needed.
        """
        from .models import PersonalizedProduct, PersonalizedProductUBO
        
        # Create PersonalizedProduct based on Service
        personalized_data = {
            'nome': f"Service: {self.service_name}",
            'descricao': f"Personalized service based on {self.service_name}. {self.description}",
            'status': 'DRAFT',
            'configuracao_personalizada': {
                'service_id': self.id,
                'service_type': self.service_type,
                'requirements': self.requirements,
                'deliverables': self.deliverables,
                'estimated_duration': self.estimated_duration,
                **(custom_config or {})
            }
        }
        
        # Set base association
        if self.associated_product:
            personalized_data['base_product'] = self.associated_product
        elif self.associated_structure:
            personalized_data['base_structure'] = self.associated_structure
        
        # Set custom cost if available
        if self.cost:
            personalized_data['custo_personalizado'] = self.cost
        
        personalized_product = PersonalizedProduct.objects.create(**personalized_data)
        
        # Associate UBOs if provided
        if ubos:
            for ubo_data in ubos:
                PersonalizedProductUBO.objects.create(
                    personalized_product=personalized_product,
                    ubo=ubo_data['ubo'],
                    ownership_percentage=ubo_data.get('percentage'),
                    role=ubo_data.get('role', 'OWNER'),
                    data_inicio=ubo_data.get('start_date', timezone.now().date())
                )
        
        return personalized_product
    
    def get_total_cost(self):
        """Calculate total cost including associated entity costs"""
        total = self.cost or 0
        
        if self.associated_product:
            total += self.associated_product.get_custo_total()
        elif self.associated_structure:
            total += self.associated_structure.get_custo_total_primeiro_ano()
        
        return total
    
    def is_available_for_association(self):
        """Check if service is available for new associations"""
        return self.status == 'ACTIVE' and self.ativo
    
    def get_service_activities(self):
        """Get all activities associated with this service"""
        return self.serviceactivity_set.filter(ativo=True).order_by('-start_date')


class ServiceActivity(models.Model):
    """
    Model for tracking specific activities performed within a Service.
    Allows detailed tracking of service execution and progress.
    """
    
    ACTIVITY_STATUS = [
        ('PLANNED', 'Planned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('ON_HOLD', 'On Hold'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    PRIORITY_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]
    
    # Relationships
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        help_text="Service this activity belongs to"
    )
    
    # Activity Information
    activity_description = models.TextField(
        help_text="Detailed description of the activity"
    )
    activity_title = models.CharField(
        max_length=200,
        help_text="Short title for the activity"
    )
    
    # Dates and Timeline
    start_date = models.DateField(
        help_text="Planned or actual start date"
    )
    completion_date = models.DateField(
        null=True,
        blank=True,
        help_text="Actual completion date (optional)"
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        help_text="Due date for completion (optional)"
    )
    
    # Status and Priority
    status = models.CharField(
        max_length=20,
        choices=ACTIVITY_STATUS,
        default='PLANNED',
        help_text="Current status of the activity"
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_LEVELS,
        default='MEDIUM',
        help_text="Priority level of the activity"
    )
    
    # Responsibility and Notes
    responsible_person = models.CharField(
        max_length=200,
        help_text="Person responsible for this activity"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes and observations"
    )
    
    # Cost and Effort
    estimated_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Estimated hours for completion"
    )
    actual_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Actual hours spent"
    )
    
    # Metadata
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Service Activity"
        verbose_name_plural = "Service Activities"
        ordering = ['-start_date', 'priority']
        indexes = [
            models.Index(fields=['service', 'status']),
            models.Index(fields=['start_date']),
            models.Index(fields=['due_date']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['responsible_person']),
        ]
    
    def __str__(self):
        return f"{self.activity_title} - {self.service.service_name}"
    
    def clean(self):
        """Validate activity dates"""
        if self.completion_date and self.start_date:
            if self.completion_date < self.start_date:
                raise ValidationError(
                    "Completion date cannot be earlier than start date"
                )
        
        if self.due_date and self.start_date:
            if self.due_date < self.start_date:
                raise ValidationError(
                    "Due date cannot be earlier than start date"
                )
    
    def is_overdue(self):
        """Check if activity is overdue"""
        if not self.due_date or self.status == 'COMPLETED':
            return False
        return timezone.now().date() > self.due_date
    
    def get_progress_percentage(self):
        """Calculate progress percentage based on status"""
        status_progress = {
            'PLANNED': 0,
            'IN_PROGRESS': 50,
            'COMPLETED': 100,
            'ON_HOLD': 25,
            'CANCELLED': 0,
        }
        return status_progress.get(self.status, 0)
    
    def get_duration_days(self):
        """Calculate duration in days if completed"""
        if self.completion_date and self.start_date:
            return (self.completion_date - self.start_date).days
        return None
    
    def mark_completed(self, completion_date=None):
        """Mark activity as completed with optional completion date"""
        self.status = 'COMPLETED'
        self.completion_date = completion_date or timezone.now().date()
        self.save()
    
    def get_status_color(self):
        """Return color code for status display"""
        colors = {
            'PLANNED': '#6c757d',      # Gray
            'IN_PROGRESS': '#007bff',  # Blue
            'COMPLETED': '#28a745',    # Green
            'ON_HOLD': '#ffc107',      # Yellow
            'CANCELLED': '#dc3545',    # Red
        }
        return colors.get(self.status, '#6c757d')
    
    def get_priority_color(self):
        """Return color code for priority display"""
        colors = {
            'LOW': '#28a745',      # Green
            'MEDIUM': '#ffc107',   # Yellow
            'HIGH': '#fd7e14',     # Orange
            'URGENT': '#dc3545',   # Red
        }
        return colors.get(self.priority, '#6c757d')

