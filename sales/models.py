from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Product(models.Model):
    """
    Produto comercial que conecta duas ou mais Legal Structures
    """
    
    COMPLEXIDADE_PRODUCT = [
        ('BASIC', 'Basic Configuration'),
        ('INTERMEDIATE', 'Intermediate Configuration'),
        ('ADVANCED', 'Advanced Configuration'),
        ('EXPERT', 'Expert Configuration'),
    ]
    
    # Campos básicos
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
        'corporate.Structure',
        through='ProductHierarchy',
        through_fields=('product', 'structure'),
        help_text="Legal structures included in this product"
    )
    
    # Configuração e custos
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
    
    # Campos de implementação
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
    
    def get_custo_total(self):
        """Calcula custo total do produto"""
        if not self.custo_automatico and self.custo_manual:
            return self.custo_manual
        
        # Calcular automaticamente baseado nas estruturas
        total = 0
        for hierarchy in self.producthierarchy_set.all():
            total += hierarchy.structure.get_custo_total_primeiro_ano()
        
        return total


class ProductHierarchy(models.Model):
    """
    Hierarquia de Legal Structures dentro de um Product
    """
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        help_text="Product that contains this structure"
    )
    structure = models.ForeignKey(
        'corporate.Structure',
        on_delete=models.CASCADE,
        help_text="Legal structure included in the product"
    )
    order = models.PositiveIntegerField(
        help_text="Order of this structure in the product hierarchy"
    )
    
    # Configuração específica da estrutura no produto
    custom_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Custom cost for this structure in this product"
    )
    notes = models.TextField(
        blank=True,
        help_text="Specific notes for this structure in this product"
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Product Hierarchy"
        verbose_name_plural = "Product Hierarchies"
        ordering = ['product', 'order']
        unique_together = [['product', 'structure'], ['product', 'order']]
        indexes = [
            models.Index(fields=['product', 'order']),
        ]
    
    def __str__(self):
        return f"{self.product.commercial_name} - {self.structure.nome} (#{self.order})"
    
    def get_effective_cost(self):
        """Retorna o custo efetivo da estrutura no produto"""
        if self.custom_cost:
            return self.custom_cost
        return self.structure.get_custo_total_primeiro_ano()


class PersonalizedProductUBO(models.Model):
    """
    Relacionamento many-to-many entre PersonalizedProduct e UBO com percentual
    """
    
    personalized_product = models.ForeignKey(
        'PersonalizedProduct',
        on_delete=models.CASCADE,
        help_text="Produto personalizado"
    )
    ubo = models.ForeignKey(
        'corporate.UBO',
        on_delete=models.CASCADE,
        help_text="UBO (Ultimate Beneficial Owner)"
    )
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(100.00)],
        help_text="Percentual de participação do UBO (0.01 a 100.00%)"
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Personalized Product UBO"
        verbose_name_plural = "Personalized Product UBOs"
        unique_together = [['personalized_product', 'ubo']]
        indexes = [
            models.Index(fields=['personalized_product']),
            models.Index(fields=['ubo']),
        ]
    
    def __str__(self):
        return f"{self.personalized_product.nome} - {self.ubo.nome} ({self.percentage}%)"


class PersonalizedProduct(models.Model):
    """
    Produto personalizado que representa Products ou Legal Structures associadas a UBOs
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
        'corporate.Structure',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Legal Structure base para este produto personalizado"
    )
    
    # Relacionamentos com UBOs - através do modelo intermediário
    ubos = models.ManyToManyField(
        'corporate.UBO',
        through=PersonalizedProductUBO,
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
        
        # Usar custo do objeto base
        base_obj = self.get_base_object()
        if base_obj:
            if hasattr(base_obj, 'get_custo_total'):
                return base_obj.get_custo_total()
            elif hasattr(base_obj, 'get_custo_total_primeiro_ano'):
                return base_obj.get_custo_total_primeiro_ano()
        
        return 0
    
    def get_total_percentage(self):
        """Calcula o percentual total dos UBOs"""
        return sum(
            ubo_rel.percentage 
            for ubo_rel in self.personalizedproductubo_set.all()
        )
    
    def validate_ubos_percentage(self):
        """Valida se a soma dos percentuais dos UBOs é válida"""
        total = self.get_total_percentage()
        if total > 100:
            raise ValidationError(
                f"Total percentage of UBOs ({total}%) cannot exceed 100%"
            )
        return total
