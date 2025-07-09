# SIRIUS - Guia de Desenvolvimento

**Sistema:** Strategic Intelligence Relationship & Interactive Universal System  
**Versão:** 2.0.0  
**Última atualização:** Janeiro 2025  

---

## 📋 Visão Geral

O SIRIUS é um sistema Django focado na gestão de estruturas corporativas através do Django Admin. Este guia fornece todas as informações necessárias para desenvolvedores trabalharem no projeto.

## 🛠️ Configuração do Ambiente de Desenvolvimento

### Pré-requisitos

- Python 3.11+
- Git
- Editor de código (VS Code recomendado)

### Setup Inicial

```bash
# 1. Clonar o repositório
git clone https://github.com/carlossilvatbh/sirius-system.git
cd sirius-system

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações

# 5. Executar migrações
python manage.py migrate

# 6. Criar superusuário
python manage.py createsuperuser

# 7. Executar servidor de desenvolvimento
python manage.py runserver
```

### Acesso ao Sistema

- **URL:** http://localhost:8000/
- **Admin:** http://localhost:8000/admin/
- **Login:** Use as credenciais do superusuário criado

## 🏗️ Arquitetura do Sistema

### Apps Django

O SIRIUS está organizado em 5 apps principais:

1. **corporate** - Entidades corporativas e estruturas
2. **sales** - Parceiros e solicitações de estruturas
3. **corporate_relationship** - Relacionamentos e arquivos
4. **financial_department** - Gestão de preços e custos
5. **parties** - Pessoas e papéis (UBO, beneficiários)

### Modelos Principais

```python
# corporate/models.py
Entity          # Entidades corporativas
Structure       # Estruturas hierárquicas
EntityOwnership # Relacionamentos de propriedade
ValidationRule  # Regras de validação

# sales/models.py
Partner         # Parceiros (ex-Client)
Contact         # Contatos
StructureRequest # Solicitações de estruturas
StructureApproval # Aprovações

# financial_department/models.py
EntityPrice     # Preços de entidades
IncorporationCost # Custos de incorporação
ServicePrice    # Preços de serviços
ServiceCost     # Custos de serviços

# parties/models.py
Party           # Pessoas (ex-UBO)
PartyRole       # Papéis e poderes
Passport        # Passaportes
BeneficiaryRelation # Relações de beneficiário

# corporate_relationship/models.py
File            # Arquivos de estruturas
Service         # Serviços
ServiceActivity # Atividades de serviços
```

## 🔧 Padrões de Desenvolvimento

### Convenções de Código

- **PEP 8** para formatação Python
- **Nomes descritivos** para variáveis e funções
- **Docstrings** para classes e métodos complexos
- **Type hints** quando apropriado

### Estrutura de Modelos

```python
class ExampleModel(models.Model):
    """Docstring explicando o propósito do modelo."""
    
    # Campos obrigatórios primeiro
    name = models.CharField(max_length=255)
    
    # Campos opcionais depois
    description = models.TextField(blank=True, null=True)
    
    # Campos de controle por último
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Example"
        verbose_name_plural = "Examples"
        ordering = ['name']
    
    def __str__(self):
        return self.name
```

### Admin Configuration

```python
@admin.register(ExampleModel)
class ExampleModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'description')
        }),
        ('Controle', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
```

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes
python manage.py test

# Testes de um app específico
python manage.py test corporate

# Teste específico
python manage.py test corporate.tests.TestEntityModel
```

### Estrutura de Testes

```python
from django.test import TestCase
from django.contrib.auth.models import User
from .models import ExampleModel

class ExampleModelTest(TestCase):
    def setUp(self):
        """Configuração inicial para cada teste."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_model_creation(self):
        """Teste de criação do modelo."""
        example = ExampleModel.objects.create(
            name='Test Example'
        )
        self.assertEqual(example.name, 'Test Example')
        self.assertTrue(example.created_at)
```

## 🔍 Debug e Troubleshooting

### Comandos Úteis

```bash
# Verificar configuração
python manage.py check

# Ver migrações
python manage.py showmigrations

# Shell Django
python manage.py shell

# Coletar arquivos estáticos
python manage.py collectstatic

# Limpar cache
python manage.py clear_cache  # Se configurado
```

### Logs de Debug

```python
import logging

logger = logging.getLogger(__name__)

def example_function():
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
```

## 📦 Dependências

### Principais Bibliotecas

- **Django 4.2** - Framework web
- **python-dotenv** - Variáveis de ambiente
- **Pillow** - Processamento de imagens
- **psycopg2-binary** - PostgreSQL (produção)

### Adicionando Novas Dependências

```bash
# Instalar nova dependência
pip install nova-biblioteca

# Atualizar requirements.txt
pip freeze > requirements.txt

# Ou usar pip-tools (recomendado)
pip-compile requirements.in
```

## 🚀 Deploy

### Preparação para Deploy

```bash
# 1. Coletar arquivos estáticos
python manage.py collectstatic --noinput

# 2. Executar migrações
python manage.py migrate

# 3. Verificar configuração
python manage.py check --deploy
```

### Variáveis de Ambiente (Produção)

```bash
DEBUG=False
SECRET_KEY=sua-chave-secreta-super-segura
ALLOWED_HOSTS=seudominio.com,www.seudominio.com
DATABASE_URL=postgres://user:pass@host:port/dbname
```

## 🤝 Contribuindo

### Fluxo de Trabalho

1. **Fork** do repositório
2. **Criar branch** para feature: `git checkout -b feature/nova-funcionalidade`
3. **Fazer commits** descritivos
4. **Executar testes** antes do push
5. **Criar Pull Request** com descrição detalhada

### Padrões de Commit

```bash
feat: adicionar novo modelo de exemplo
fix: corrigir bug na validação de dados
docs: atualizar documentação da API
style: formatar código conforme PEP 8
refactor: reorganizar estrutura de modelos
test: adicionar testes para modelo Example
```

## 📚 Recursos Adicionais

- [Documentação Django](https://docs.djangoproject.com/)
- [Django Admin Cookbook](https://books.agiliq.com/projects/django-admin-cookbook/)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)

---

**Dúvidas?** Consulte a documentação ou abra uma issue no repositório.

