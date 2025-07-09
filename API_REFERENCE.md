# SIRIUS - Referência da API

**Sistema:** Strategic Intelligence Relationship & Interactive Universal System  
**Versão:** 2.0.0  
**Última atualização:** Janeiro 2025  

---

## 📋 Visão Geral

Esta documentação fornece uma referência completa dos modelos Django do SIRIUS, incluindo campos, relacionamentos e métodos disponíveis.

## 🏢 App: Corporate

### Entity (Entidade Corporativa)

Representa uma entidade corporativa (empresa, holding, etc.).

```python
class Entity(models.Model):
    # Campos principais
    name = models.CharField(max_length=255)
    entity_type = models.CharField(max_length=50, choices=ENTITY_TYPE_CHOICES)
    jurisdiction = models.CharField(max_length=100)
    incorporation_date = models.DateField(blank=True, null=True)
    
    # Identificação corporativa
    corporate_name = models.CharField(max_length=255, blank=True, null=True)
    hash_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Configurações
    templates = models.TextField(blank=True, null=True)
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Choices:**
- `ENTITY_TYPE_CHOICES`: Company, Holding, Trust, Foundation, Partnership

**Métodos:**
- `__str__()`: Retorna o nome da entidade
- `get_absolute_url()`: URL para visualização da entidade

### Structure (Estrutura Hierárquica)

Representa uma estrutura corporativa hierárquica.

```python
class Structure(models.Model):
    # Identificação
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='drafting')
    
    # Entidades relacionadas
    entities = models.ManyToManyField(Entity, through='EntityOwnership')
    
    # Valores de shares
    total_shares_usd = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_shares_eur = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Tax impacts calculados
    tax_impact_level = models.CharField(max_length=20, blank=True, null=True)
    severity_score = models.IntegerField(default=0)
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Choices:**
- `STATUS_CHOICES`: drafting, under_review, approved, rejected

**Métodos:**
- `calculate_tax_impacts()`: Calcula impactos fiscais
- `validate_structure()`: Valida a estrutura
- `get_total_percentage()`: Retorna percentual total de ownership

### EntityOwnership (Relacionamento de Propriedade)

Relacionamento many-to-many entre Entity e Structure com informações de propriedade.

```python
class EntityOwnership(models.Model):
    # Relacionamentos
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)
    
    # Propriedade
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    shares_usd = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    shares_eur = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
```

**Métodos:**
- `save()`: Auto-calcula shares baseado em percentage
- `clean()`: Valida que percentage está entre 0-100

### ValidationRule (Regra de Validação)

Define regras de validação para estruturas corporativas.

```python
class ValidationRule(models.Model):
    # Identificação
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    # Configuração
    entity_type = models.CharField(max_length=50, choices=ENTITY_TYPE_CHOICES)
    jurisdiction = models.CharField(max_length=100)
    
    # Tax impacts
    tax_impacts = models.JSONField(default=dict)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
```

## 💼 App: Sales

### Partner (Parceiro)

Representa um parceiro de negócios (anteriormente Client).

```python
class Partner(models.Model):
    # Identificação
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Endereço
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Contact (Contato)

Contatos associados aos parceiros.

```python
class Contact(models.Model):
    # Relacionamento
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='contacts')
    
    # Informações pessoais
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Função
    position = models.CharField(max_length=100, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
```

### StructureRequest (Solicitação de Estrutura)

Solicitações de criação de estruturas corporativas.

```python
class StructureRequest(models.Model):
    # Relacionamentos
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    structure = models.ForeignKey('corporate.Structure', on_delete=models.CASCADE)
    
    # Detalhes da solicitação
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Status
    status = models.CharField(max_length=20, choices=REQUEST_STATUS_CHOICES, default='pending')
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### StructureApproval (Aprovação de Estrutura)

Processo de aprovação de estruturas.

```python
class StructureApproval(models.Model):
    # Relacionamentos
    structure_request = models.OneToOneField(StructureRequest, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Aprovação
    approval_date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True, null=True)
    
    # Status
    is_approved = models.BooleanField(default=True)
```

## 💰 App: Financial Department

### EntityPrice (Preço de Entidade)

Preços para criação de entidades corporativas.

```python
class EntityPrice(models.Model):
    # Identificação
    entity_type = models.CharField(max_length=50, choices=ENTITY_TYPE_CHOICES)
    jurisdiction = models.CharField(max_length=100)
    
    # Preços
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    
    # Markup
    markup_type = models.CharField(max_length=20, choices=MARKUP_TYPE_CHOICES, default='percentage')
    markup_value = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### IncorporationCost (Custo de Incorporação)

Componentes de custo para incorporação de entidades.

```python
class IncorporationCost(models.Model):
    # Relacionamento
    entity_price = models.ForeignKey(EntityPrice, on_delete=models.CASCADE, related_name='costs')
    
    # Identificação
    cost_type = models.CharField(max_length=50, choices=COST_TYPE_CHOICES)
    description = models.CharField(max_length=255)
    
    # Valor
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    
    # Configuração
    is_mandatory = models.BooleanField(default=True)
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
```

### ServicePrice (Preço de Serviço)

Preços para serviços oferecidos.

```python
class ServicePrice(models.Model):
    # Identificação
    service_name = models.CharField(max_length=255)
    service_category = models.CharField(max_length=100)
    
    # Preço
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    
    # Configuração
    billing_type = models.CharField(max_length=20, choices=BILLING_TYPE_CHOICES, default='one_time')
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### ServiceCost (Custo de Serviço)

Custos associados aos serviços.

```python
class ServiceCost(models.Model):
    # Relacionamento
    service_price = models.ForeignKey(ServicePrice, on_delete=models.CASCADE, related_name='costs')
    
    # Identificação
    cost_description = models.CharField(max_length=255)
    
    # Valor
    cost_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
```

## 👥 App: Parties

### Party (Pessoa)

Representa uma pessoa física (anteriormente UBO).

```python
class Party(models.Model):
    # Informações pessoais
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    
    # Contato
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Endereço
    address = models.TextField()
    country_of_residence = models.CharField(max_length=100)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### PartyRole (Papel da Pessoa)

Papéis e poderes que uma pessoa pode ter.

```python
class PartyRole(models.Model):
    # Relacionamentos
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='roles')
    entity = models.ForeignKey('corporate.Entity', on_delete=models.CASCADE)
    
    # Papel
    role_type = models.CharField(max_length=50, choices=ROLE_TYPE_CHOICES)
    powers = models.JSONField(default=list)
    
    # Período
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
```

**Choices:**
- `ROLE_TYPE_CHOICES`: Director, Shareholder, Beneficiary, Authorized_Signatory, Secretary

### Passport (Passaporte)

Informações de passaporte das pessoas.

```python
class Passport(models.Model):
    # Relacionamento
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='passports')
    
    # Informações do passaporte
    passport_number = models.CharField(max_length=50)
    issuing_country = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    
    # Status
    is_primary = models.BooleanField(default=False)
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
```

**Métodos:**
- `is_expired()`: Verifica se o passaporte está expirado
- `days_until_expiry()`: Dias até a expiração

### BeneficiaryRelation (Relação de Beneficiário)

Relações de beneficiário (sucessor aprimorado).

```python
class BeneficiaryRelation(models.Model):
    # Relacionamentos
    beneficiary = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='beneficiary_relations')
    entity = models.ForeignKey('corporate.Entity', on_delete=models.CASCADE)
    
    # Benefício
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    relation_type = models.CharField(max_length=50, choices=RELATION_TYPE_CHOICES)
    
    # Condições
    conditions = models.TextField(blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
```

### DocumentAttachment (Anexo de Documento)

Documentos anexados baseados em URL.

```python
class DocumentAttachment(models.Model):
    # Relacionamento
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='documents')
    
    # Documento
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    document_url = models.URLField()
    description = models.CharField(max_length=255, blank=True, null=True)
    
    # Controle
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

## 🔗 App: Corporate Relationship

### File (Arquivo)

Arquivos de estruturas aprovadas.

```python
class File(models.Model):
    # Relacionamento
    structure = models.ForeignKey('corporate.Structure', on_delete=models.CASCADE, related_name='files')
    
    # Arquivo
    file_name = models.CharField(max_length=255)
    file_url = models.URLField()
    file_type = models.CharField(max_length=50)
    file_size = models.IntegerField()
    
    # Metadados
    description = models.TextField(blank=True, null=True)
    
    # Controle
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
```

### Service (Serviço)

Serviços oferecidos.

```python
class Service(models.Model):
    # Identificação
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    
    # Configuração
    is_active = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### ServiceActivity (Atividade de Serviço)

Atividades relacionadas aos serviços.

```python
class ServiceActivity(models.Model):
    # Relacionamentos
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='activities')
    entity = models.ForeignKey('corporate.Entity', on_delete=models.CASCADE)
    
    # Atividade
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPE_CHOICES)
    description = models.TextField()
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
```

## 🔍 Consultas Comuns

### Exemplos de QuerySets

```python
# Buscar entidades por tipo
entities = Entity.objects.filter(entity_type='Company')

# Buscar estruturas aprovadas
approved_structures = Structure.objects.filter(status='approved')

# Buscar parceiros ativos com contatos
active_partners = Partner.objects.filter(is_active=True).prefetch_related('contacts')

# Buscar preços por jurisdição
prices = EntityPrice.objects.filter(jurisdiction='Delaware', is_active=True)

# Buscar pessoas com passaportes válidos
valid_parties = Party.objects.filter(
    passports__expiry_date__gt=timezone.now().date()
).distinct()

# Buscar arquivos de uma estrutura
structure_files = File.objects.filter(structure_id=1).order_by('-uploaded_at')
```

### Agregações Úteis

```python
from django.db.models import Count, Sum, Avg

# Contar entidades por tipo
entity_counts = Entity.objects.values('entity_type').annotate(count=Count('id'))

# Soma total de shares por estrutura
structure_totals = Structure.objects.annotate(
    total_usd=Sum('entityownership__shares_usd'),
    total_eur=Sum('entityownership__shares_eur')
)

# Preço médio por jurisdição
avg_prices = EntityPrice.objects.values('jurisdiction').annotate(
    avg_price=Avg('base_price')
)
```

## 📝 Notas Importantes

### Relacionamentos

- **Entity ↔ Structure**: Many-to-Many através de EntityOwnership
- **Partner ↔ Contact**: One-to-Many
- **Party ↔ PartyRole**: One-to-Many
- **Structure ↔ File**: One-to-Many

### Validações

- Percentuais de ownership devem somar 100% por estrutura
- Passaportes têm validação de expiração
- Preços devem ser positivos
- Emails devem ser únicos onde aplicável

### Performance

- Use `select_related()` para ForeignKeys
- Use `prefetch_related()` para ManyToMany e reverse ForeignKeys
- Considere indexação para campos de busca frequente

---

**Esta documentação é atualizada automaticamente conforme mudanças nos modelos.**

