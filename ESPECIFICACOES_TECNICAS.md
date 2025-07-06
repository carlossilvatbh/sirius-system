# ESPECIFICAÇÕES TÉCNICAS DETALHADAS
## SIRIUS - Implementação dos Novos Módulos

**Autor:** Manus AI  
**Data:** 06 de Janeiro de 2025  
**Versão:** 1.0  

---

## ESTRUTURAS DE MODELOS DJANGO

### Modelo UBO (Ultimate Beneficial Owner)

```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import re

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
        super().clean()
        
        # Validação básica de TIN (pode ser expandida por país)
        if self.tin and not re.match(r'^[A-Z0-9\-]{5,20}$', self.tin.upper()):
            raise ValidationError({
                'tin': 'TIN deve conter apenas letras, números e hífens (5-20 caracteres)'
            })
    
    def get_products_associados(self):
        """Retorna todos os Products associados a este UBO"""
        return Product.objects.filter(
            personalizedproduct__ubos=self
        ).distinct()
    
    def get_structures_associadas(self):
        """Retorna todas as Legal Structures associadas a este UBO"""
        return Estrutura.objects.filter(
            personalizedproduct__ubos=self
        ).distinct()
```

### Modelo Successor

```python
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
    
    # Produto específico (opcional)
    personalized_product = models.ForeignKey(
        'PersonalizedProduct',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Produto específico sendo transferido (se aplicável)"
    )
    
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
        unique_together = ['ubo_proprietario', 'ubo_sucessor', 'personalized_product']
        indexes = [
            models.Index(fields=['ubo_proprietario', 'ativo']),
            models.Index(fields=['data_efetivacao']),
        ]
    
    def __str__(self):
        return f"{self.ubo_proprietario.nome_completo} → {self.ubo_sucessor.nome_completo} ({self.percentual}%)"
    
    def clean(self):
        """Validações customizadas"""
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
```

### Modelo Product (Refatoração de Template)

```python
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
        
        total_custo = 0
        hierarquias = self.producthierarchy_set.all()
        
        for hierarquia in hierarquias:
            estrutura_custo = (
                hierarquia.child_structure.custo_base + 
                hierarquia.child_structure.custo_manutencao
            )
            # Aplica percentual se especificado
            if hierarquia.ownership_percentage:
                estrutura_custo *= (hierarquia.ownership_percentage / 100)
            
            total_custo += estrutura_custo
        
        return total_custo
    
    def incrementar_uso(self):
        """Incrementa contador de uso"""
        self.uso_count += 1
        self.save(update_fields=['uso_count'])
    
    def get_estruturas_hierarquia(self):
        """Retorna estruturas organizadas por hierarquia"""
        hierarquias = self.producthierarchy_set.select_related(
            'parent_structure', 'child_structure'
        ).order_by('hierarchy_level', 'child_structure__nome')
        
        return hierarquias
```

### Modelo ProductHierarchy

```python
class ProductHierarchy(models.Model):
    """
    Modelo para definir hierarquia entre Legal Structures dentro de um Product
    """
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        help_text="Produto ao qual esta hierarquia pertence"
    )
    parent_structure = models.ForeignKey(
        'estruturas_app.Estrutura',
        on_delete=models.CASCADE,
        related_name='children_in_products',
        null=True,
        blank=True,
        help_text="Estrutura pai (null para estruturas raiz)"
    )
    child_structure = models.ForeignKey(
        'estruturas_app.Estrutura',
        on_delete=models.CASCADE,
        related_name='parents_in_products',
        help_text="Estrutura filha"
    )
    ownership_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.01), MaxValueValidator(100.00)],
        help_text="Percentual de propriedade (opcional)"
    )
    hierarchy_level = models.IntegerField(
        default=0,
        help_text="Nível na hierarquia (0=raiz, 1=primeiro nível, etc.)"
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Product Hierarchy"
        verbose_name_plural = "Product Hierarchies"
        unique_together = ['product', 'child_structure']
        indexes = [
            models.Index(fields=['product', 'hierarchy_level']),
            models.Index(fields=['parent_structure']),
        ]
    
    def __str__(self):
        if self.parent_structure:
            return f"{self.parent_structure.nome} → {self.child_structure.nome}"
        return f"[ROOT] → {self.child_structure.nome}"
    
    def clean(self):
        """Validações para prevenir loops hierárquicos"""
        super().clean()
        
        # Prevenir auto-referência
        if self.parent_structure == self.child_structure:
            raise ValidationError("Estrutura não pode ser pai de si mesma")
        
        # Prevenir loops (implementação básica)
        if self.parent_structure:
            current = self.parent_structure
            visited = set()
            
            while current:
                if current.id in visited:
                    raise ValidationError("Hierarquia criaria um loop")
                visited.add(current.id)
                
                # Buscar próximo pai na hierarquia
                parent_hierarchy = ProductHierarchy.objects.filter(
                    product=self.product,
                    child_structure=current
                ).first()
                
                current = parent_hierarchy.parent_structure if parent_hierarchy else None
```

---

## CONFIGURAÇÕES DO DJANGO ADMIN

### UBO Admin

```python
from django.contrib import admin
from django.utils.html import format_html
from .models import UBO, Successor, Product, ProductHierarchy

@admin.register(UBO)
class UBOAdmin(admin.ModelAdmin):
    list_display = [
        'nome_completo',
        'nacionalidade_display',
        'tin',
        'data_nascimento',
        'products_count',
        'ativo'
    ]
    list_filter = [
        'nacionalidade',
        'ativo',
        'created_at'
    ]
    search_fields = [
        'nome_completo',
        'tin',
        'email'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome_completo', 'data_nascimento', 'nacionalidade')
        }),
        ('Informações Fiscais', {
            'fields': ('tin', 'endereco_residencia_fiscal')
        }),
        ('Contato', {
            'fields': ('telefone', 'email'),
            'classes': ('collapse',)
        }),
        ('Observações', {
            'fields': ('observacoes',),
            'classes': ('collapse',)
        }),
        ('Status e Metadados', {
            'fields': ('ativo', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def nacionalidade_display(self, obj):
        return obj.get_nacionalidade_display()
    nacionalidade_display.short_description = "Nacionalidade"
    nacionalidade_display.admin_order_field = 'nacionalidade'
    
    def products_count(self, obj):
        count = obj.get_products_associados().count()
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if count > 0 else 'gray',
            count
        )
    products_count.short_description = "Products"
```

### Successor Admin

```python
@admin.register(Successor)
class SuccessorAdmin(admin.ModelAdmin):
    list_display = [
        'ubo_proprietario',
        'ubo_sucessor',
        'percentual_display',
        'data_efetivacao',
        'efetivado',
        'ativo'
    ]
    list_filter = [
        'efetivado',
        'ativo',
        'data_definicao'
    ]
    search_fields = [
        'ubo_proprietario__nome_completo',
        'ubo_sucessor__nome_completo'
    ]
    autocomplete_fields = ['ubo_proprietario', 'ubo_sucessor', 'personalized_product']
    readonly_fields = ['data_definicao', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Sucessão', {
            'fields': (
                'ubo_proprietario',
                'ubo_sucessor',
                'percentual',
                'personalized_product'
            )
        }),
        ('Datas', {
            'fields': (
                'data_definicao',
                'data_efetivacao',
                'data_efetivacao_real'
            )
        }),
        ('Condições', {
            'fields': ('condicoes',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('ativo', 'efetivado', 'created_at', 'updated_at')
        }),
    )
    
    def percentual_display(self, obj):
        color = 'green' if obj.percentual == 100 else 'orange'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.2f}%</span>',
            color,
            obj.percentual
        )
    percentual_display.short_description = "Percentual"
    percentual_display.admin_order_field = 'percentual'
    
    def get_form(self, request, obj=None, **kwargs):
        """Customiza form para mostrar percentual disponível"""
        form = super().get_form(request, obj, **kwargs)
        
        if obj and obj.ubo_proprietario:
            # Calcula percentual disponível
            outros_sucessores = Successor.objects.filter(
                ubo_proprietario=obj.ubo_proprietario,
                ativo=True
            ).exclude(pk=obj.pk)
            
            total_usado = sum(s.percentual for s in outros_sucessores)
            disponivel = 100 - total_usado
            
            form.base_fields['percentual'].help_text = f"Disponível: {disponivel:.2f}%"
        
        return form
```

---

## MIGRAÇÕES DE DADOS

### Migração de Template para Product

```python
# migrations/0002_migrate_template_to_product.py
from django.db import migrations

def migrate_templates_to_products(apps, schema_editor):
    """Migra dados de Template para Product"""
    Template = apps.get_model('estruturas_app', 'Template')
    Product = apps.get_model('estruturas_app', 'Product')
    
    for template in Template.objects.all():
        # Cria Product baseado no Template
        product = Product.objects.create(
            nome=template.nome,
            categoria=template.categoria,
            complexidade_template=template.complexidade_template,
            descricao=template.descricao,
            commercial_name=template.nome,  # Usar nome como commercial_name inicial
            master_agreement_url='https://example.com/agreement',  # URL padrão
            configuracao=template.configuracao,
            custo_automatico=True,
            tempo_total_implementacao=template.tempo_total_implementacao,
            uso_count=template.uso_count,
            publico_alvo=template.publico_alvo,
            casos_uso=template.casos_uso,
            ativo=template.ativo,
            created_at=template.created_at,
            updated_at=template.updated_at,
        )
        
        # Migrar estruturas se existirem na configuração
        if template.configuracao and 'elementos' in template.configuracao:
            migrate_template_structures(product, template.configuracao['elementos'])

def migrate_template_structures(product, elementos):
    """Migra estruturas do template para hierarquia do product"""
    ProductHierarchy = apps.get_model('estruturas_app', 'ProductHierarchy')
    Estrutura = apps.get_model('estruturas_app', 'Estrutura')
    
    for i, elemento in enumerate(elementos):
        if 'estrutura_id' in elemento:
            try:
                estrutura = Estrutura.objects.get(id=elemento['estrutura_id'])
                ProductHierarchy.objects.create(
                    product=product,
                    child_structure=estrutura,
                    hierarchy_level=elemento.get('level', 0),
                    ownership_percentage=elemento.get('percentage')
                )
            except Estrutura.DoesNotExist:
                continue

def reverse_migration(apps, schema_editor):
    """Reverter migração se necessário"""
    # Implementar lógica de reversão se necessário
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('estruturas_app', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(
            migrate_templates_to_products,
            reverse_migration
        ),
    ]
```

---

## VALIDAÇÕES E TESTES

### Testes para Modelo UBO

```python
# tests/test_ubo.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from estruturas_app.models import UBO

class UBOModelTest(TestCase):
    def setUp(self):
        self.ubo_data = {
            'nome_completo': 'João Silva Santos',
            'data_nascimento': '1980-01-15',
            'nacionalidade': 'BR',
            'tin': 'CPF12345678901'
        }
    
    def test_create_ubo_valid(self):
        """Testa criação de UBO com dados válidos"""
        ubo = UBO.objects.create(**self.ubo_data)
        self.assertEqual(ubo.nome_completo, 'João Silva Santos')
        self.assertEqual(ubo.nacionalidade, 'BR')
        self.assertTrue(ubo.ativo)
    
    def test_ubo_tin_validation(self):
        """Testa validação de TIN"""
        # TIN válido
        ubo = UBO(**self.ubo_data)
        ubo.full_clean()  # Não deve gerar erro
        
        # TIN inválido
        self.ubo_data['tin'] = 'invalid@tin'
        ubo = UBO(**self.ubo_data)
        with self.assertRaises(ValidationError):
            ubo.full_clean()
    
    def test_ubo_str_representation(self):
        """Testa representação string do UBO"""
        ubo = UBO.objects.create(**self.ubo_data)
        expected = f"{self.ubo_data['nome_completo']} ({self.ubo_data['tin']})"
        self.assertEqual(str(ubo), expected)
```

### Testes para Validação de Percentuais

```python
# tests/test_successor.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from estruturas_app.models import UBO, Successor

class SuccessorValidationTest(TestCase):
    def setUp(self):
        self.ubo1 = UBO.objects.create(
            nome_completo='Proprietário Teste',
            data_nascimento='1970-01-01',
            nacionalidade='BR',
            tin='PROP123456'
        )
        self.ubo2 = UBO.objects.create(
            nome_completo='Sucessor 1',
            data_nascimento='1990-01-01',
            nacionalidade='BR',
            tin='SUCC123456'
        )
        self.ubo3 = UBO.objects.create(
            nome_completo='Sucessor 2',
            data_nascimento='1995-01-01',
            nacionalidade='BR',
            tin='SUCC789012'
        )
    
    def test_percentual_sum_validation(self):
        """Testa validação de soma de percentuais"""
        # Criar primeiro sucessor com 60%
        successor1 = Successor.objects.create(
            ubo_proprietario=self.ubo1,
            ubo_sucessor=self.ubo2,
            percentual=60.00
        )
        
        # Criar segundo sucessor com 40% (total = 100%)
        successor2 = Successor(
            ubo_proprietario=self.ubo1,
            ubo_sucessor=self.ubo3,
            percentual=40.00
        )
        successor2.full_clean()  # Não deve gerar erro
        successor2.save()
        
        # Tentar criar terceiro sucessor (excederia 100%)
        successor3 = Successor(
            ubo_proprietario=self.ubo1,
            ubo_sucessor=self.ubo2,  # Mesmo sucessor, percentual diferente
            percentual=10.00
        )
        with self.assertRaises(ValidationError):
            successor3.full_clean()
    
    def test_self_succession_prevention(self):
        """Testa prevenção de auto-sucessão"""
        successor = Successor(
            ubo_proprietario=self.ubo1,
            ubo_sucessor=self.ubo1,  # Mesmo UBO
            percentual=100.00
        )
        with self.assertRaises(ValidationError):
            successor.full_clean()
```

---

## OTIMIZAÇÕES DE PERFORMANCE

### Consultas Otimizadas

```python
# utils/queries.py
from django.db import models
from estruturas_app.models import UBO, Product, PersonalizedProduct

class OptimizedQueries:
    @staticmethod
    def get_ubo_with_products(ubo_id):
        """Busca UBO com todos os produtos associados otimizado"""
        return UBO.objects.select_related().prefetch_related(
            'personalizedproduct_set__base_product',
            'personalizedproduct_set__base_structure',
            'sucessores_definidos__ubo_sucessor'
        ).get(id=ubo_id)
    
    @staticmethod
    def get_product_hierarchy(product_id):
        """Busca hierarquia completa de um produto"""
        return Product.objects.prefetch_related(
            models.Prefetch(
                'producthierarchy_set',
                queryset=ProductHierarchy.objects.select_related(
                    'parent_structure',
                    'child_structure'
                ).order_by('hierarchy_level')
            )
        ).get(id=product_id)
    
    @staticmethod
    def get_personalized_products_report():
        """Consulta otimizada para relatório de produtos personalizados"""
        return PersonalizedProduct.objects.select_related(
            'base_product',
            'base_structure'
        ).prefetch_related(
            'ubos',
            'successor_set__ubo_sucessor',
            'service_set'
        ).filter(status='Active')
```

### Cache para Cálculos Complexos

```python
# utils/cache.py
from django.core.cache import cache
from django.utils.encoding import force_str

class ProductCostCache:
    @staticmethod
    def get_cache_key(product_id):
        return f"product_cost_{product_id}"
    
    @staticmethod
    def get_cached_cost(product):
        """Busca custo em cache ou calcula se necessário"""
        cache_key = ProductCostCache.get_cache_key(product.id)
        cached_cost = cache.get(cache_key)
        
        if cached_cost is None:
            cached_cost = product.get_custo_total_calculado()
            # Cache por 1 hora
            cache.set(cache_key, cached_cost, 3600)
        
        return cached_cost
    
    @staticmethod
    def invalidate_cache(product_id):
        """Invalida cache quando produto é modificado"""
        cache_key = ProductCostCache.get_cache_key(product_id)
        cache.delete(cache_key)
```

---

## RELATÓRIOS E EXPORTAÇÃO

### Relatório Principal de Personalized Product

```python
# utils/reports.py
from django.http import HttpResponse
import json
from estruturas_app.models import PersonalizedProduct

class PersonalizedProductReport:
    @staticmethod
    def generate_complete_report(personalized_product_id):
        """Gera relatório completo de um Personalized Product"""
        pp = PersonalizedProduct.objects.select_related(
            'base_product',
            'base_structure'
        ).prefetch_related(
            'ubos',
            'successor_set__ubo_sucessor',
            'service_set'
        ).get(id=personalized_product_id)
        
        report_data = {
            'personalized_product': {
                'id': pp.id,
                'nome': pp.nome,
                'status': pp.status,
                'version_number': pp.version_number,
                'created_at': pp.created_at.isoformat(),
                'updated_at': pp.updated_at.isoformat(),
            },
            'base_info': {},
            'ubos': [],
            'successors': [],
            'hierarchy': [],
            'services': [],
            'costs': {},
            'alerts': []
        }
        
        # Informações base (Product ou Structure)
        if pp.base_product:
            report_data['base_info'] = {
                'type': 'Product',
                'commercial_name': pp.base_product.commercial_name,
                'categoria': pp.base_product.get_categoria_display(),
                'complexidade': pp.base_product.get_complexidade_template_display(),
                'master_agreement_url': pp.base_product.master_agreement_url,
            }
            # Adicionar hierarquia de estruturas
            for hierarchy in pp.base_product.get_estruturas_hierarquia():
                report_data['hierarchy'].append({
                    'level': hierarchy.hierarchy_level,
                    'parent': hierarchy.parent_structure.nome if hierarchy.parent_structure else None,
                    'child': hierarchy.child_structure.nome,
                    'ownership_percentage': float(hierarchy.ownership_percentage) if hierarchy.ownership_percentage else None,
                })
        
        elif pp.base_structure:
            report_data['base_info'] = {
                'type': 'Legal Structure',
                'nome': pp.base_structure.nome,
                'tipo': pp.base_structure.get_tipo_display(),
                'complexidade': pp.base_structure.get_complexity_display_text(),
            }
        
        # UBOs associados
        for ubo in pp.ubos.all():
            report_data['ubos'].append({
                'nome_completo': ubo.nome_completo,
                'nacionalidade': ubo.get_nacionalidade_display(),
                'tin': ubo.tin,
                'data_nascimento': ubo.data_nascimento.isoformat(),
            })
        
        # Sucessores definidos
        for successor in pp.successor_set.filter(ativo=True):
            report_data['successors'].append({
                'sucessor_nome': successor.ubo_sucessor.nome_completo,
                'percentual': float(successor.percentual),
                'data_efetivacao': successor.data_efetivacao.isoformat() if successor.data_efetivacao else None,
                'efetivado': successor.efetivado,
            })
        
        # Serviços associados
        for service in pp.service_set.filter(ativo=True):
            report_data['services'].append({
                'service_name': service.service_name,
                'service_type': service.get_service_type_display(),
                'description': service.description,
                'cost': float(service.cost) if service.cost else None,
            })
        
        # Cálculos de custo
        if pp.base_product:
            report_data['costs'] = {
                'custo_total': float(pp.base_product.get_custo_total_calculado()),
                'custo_automatico': pp.base_product.custo_automatico,
            }
        elif pp.base_structure:
            report_data['costs'] = {
                'custo_base': float(pp.base_structure.custo_base),
                'custo_manutencao': float(pp.base_structure.custo_manutencao),
                'custo_total_primeiro_ano': float(pp.base_structure.get_custo_total_primeiro_ano()),
            }
        
        return report_data
    
    @staticmethod
    def export_to_json(personalized_product_id):
        """Exporta relatório em formato JSON"""
        report_data = PersonalizedProductReport.generate_complete_report(personalized_product_id)
        
        response = HttpResponse(
            json.dumps(report_data, indent=2, ensure_ascii=False),
            content_type='application/json'
        )
        response['Content-Disposition'] = f'attachment; filename="personalized_product_{personalized_product_id}_report.json"'
        
        return response
```

Este documento técnico fornece a base completa para implementação das melhorias no SIRIUS, incluindo estruturas de modelos, configurações de admin, migrações, testes e otimizações de performance.

