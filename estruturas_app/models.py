from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

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



class Product(models.Model):
    """
    Produto comercial que conecta duas ou mais Legal Structures
    Refatoração do modelo Template existente
    """
    
    CATEGORIAS = [
        ('TECH', 'Technology'),
        ('REAL_ESTATE', 'Real Estate'),
        ('TRADING', 'Trading'),
        ('FAMILY_OFFICE', 'Family Office'),
        ('INVESTMENT', 'Investment'),
        ('GENERAL', 'General'),
    ]
    
    COMPLEXIDADE_PRODUCT = [
        ('BASIC', 'Basic Configuration'),
        ('INTERMEDIATE', 'Intermediate Configuration'),
        ('ADVANCED', 'Advanced Configuration'),
        ('EXPERT', 'Expert Configuration'),
    ]
    
    # Campos básicos (mantidos do Template)
    nome = models.CharField(max_length=100, help_text="Nome do produto")
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS,
        help_text="Categoria do produto"
    )
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
            models.Index(fields=['categoria']),
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
    
    # Relacionamentos com UBOs
    ubos = models.ManyToManyField(
        UBO,
        through='PersonalizedProductUBO',
        help_text="UBOs associados a este produto personalizado"
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
        for pp_ubo in self.personalizedproductubo_set.all():
            PersonalizedProductUBO.objects.create(
                personalized_product=new_version,
                ubo=pp_ubo.ubo,
                ownership_percentage=pp_ubo.ownership_percentage,
                role=pp_ubo.role,
                data_inicio=pp_ubo.data_inicio,
                ativo=pp_ubo.ativo
            )
        
        return new_version
    
    def get_ubos_ativos(self):
        """Retorna UBOs ativos associados"""
        return self.ubos.filter(
            personalizedproductubo__ativo=True
        ).distinct()
    
    def get_total_ownership_percentage(self):
        """Calcula percentual total de propriedade"""
        total = self.personalizedproductubo_set.filter(
            ativo=True
        ).aggregate(
            total=models.Sum('ownership_percentage')
        )['total'] or 0
        
        return total


class PersonalizedProductUBO(models.Model):
    """
    Modelo intermediário para relacionamento PersonalizedProduct-UBO
    """
    
    ROLE_CHOICES = [
        ('OWNER', 'Owner'),
        ('BENEFICIARY', 'Beneficiary'),
        ('DIRECTOR', 'Director'),
        ('SHAREHOLDER', 'Shareholder'),
        ('TRUSTEE', 'Trustee'),
        ('OTHER', 'Other'),
    ]
    
    personalized_product = models.ForeignKey(
        PersonalizedProduct,
        on_delete=models.CASCADE,
        help_text="Produto personalizado"
    )
    ubo = models.ForeignKey(
        UBO,
        on_delete=models.CASCADE,
        help_text="UBO associado"
    )
    ownership_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.01), MaxValueValidator(100.00)],
        help_text="Percentual de propriedade (opcional)"
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='OWNER',
        help_text="Papel do UBO neste produto"
    )
    data_inicio = models.DateField(
        help_text="Data de início da associação"
    )
    data_fim = models.DateField(
        null=True,
        blank=True,
        help_text="Data de fim da associação (opcional)"
    )
    observacoes = models.TextField(
        blank=True,
        help_text="Observações específicas desta associação"
    )
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Personalized Product UBO"
        verbose_name_plural = "Personalized Product UBOs"
        unique_together = ['personalized_product', 'ubo', 'role']
        indexes = [
            models.Index(fields=['personalized_product', 'ativo']),
            models.Index(fields=['ubo', 'ativo']),
            models.Index(fields=['data_inicio']),
        ]
    
    def __str__(self):
        percentage_str = f" ({self.ownership_percentage}%)" if self.ownership_percentage else ""
        return f"{self.ubo.nome_completo} - {self.get_role_display()}{percentage_str}"
    
    def clean(self):
        """Validações customizadas"""
        super().clean()
        
        # Validar que data_fim é posterior a data_inicio
        if self.data_fim and self.data_inicio and self.data_fim <= self.data_inicio:
            raise ValidationError({
                'data_fim': 'Data de fim deve ser posterior à data de início'
            })

