# SIRIUS - Strategic Intelligence Relationship & Interactive Universal System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Django 4.2](https://img.shields.io/badge/django-4.2-green.svg)](https://docs.djangoproject.com/en/4.2/)

> Sistema profissional de gestão de estruturas corporativas através do Django Admin

## 🌟 Visão Geral

O SIRIUS é um sistema Django especializado na gestão de estruturas corporativas complexas, oferecendo uma interface administrativa robusta para profissionais jurídicos, consultores fiscais e especialistas em estruturação corporativa.

### ✨ Funcionalidades Principais

- **🏢 Gestão de Entidades**: Criação e administração de entidades corporativas
- **📊 Estruturas Hierárquicas**: Organização de relacionamentos entre entidades
- **💰 Gestão Financeira**: Controle de preços, custos e valores de participação
- **👥 Gestão de Pessoas**: Administração de UBOs, beneficiários e papéis
- **📋 Validação e Compliance**: Verificação automática de regras e regulamentações
- **📁 Gestão de Arquivos**: Organização de documentos e anexos

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.11+
- Git

### Instalação

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
# Editar .env conforme necessário

# 5. Executar migrações
python manage.py migrate

# 6. Criar superusuário
python manage.py createsuperuser

# 7. Executar servidor
python manage.py runserver
```

### Acesso ao Sistema

- **URL Principal:** http://localhost:8000/
- **Django Admin:** http://localhost:8000/admin/
- **Login:** Use as credenciais do superusuário criado

## 🏗️ Arquitetura

O SIRIUS está organizado em 5 apps Django principais:

### 🏢 Corporate
- **Entity**: Entidades corporativas (empresas, holdings, trusts)
- **Structure**: Estruturas hierárquicas corporativas
- **EntityOwnership**: Relacionamentos de propriedade
- **ValidationRule**: Regras de validação e compliance

### 💼 Sales
- **Partner**: Parceiros de negócios
- **Contact**: Contatos dos parceiros
- **StructureRequest**: Solicitações de estruturas
- **StructureApproval**: Processo de aprovação

### 💰 Financial Department
- **EntityPrice**: Preços de entidades por jurisdição
- **IncorporationCost**: Custos de incorporação
- **ServicePrice**: Preços de serviços
- **ServiceCost**: Custos associados aos serviços

### 👥 Parties
- **Party**: Pessoas físicas (UBOs, beneficiários)
- **PartyRole**: Papéis e poderes das pessoas
- **Passport**: Informações de passaportes
- **BeneficiaryRelation**: Relações de beneficiário
- **DocumentAttachment**: Anexos de documentos

### 🔗 Corporate Relationship
- **File**: Arquivos de estruturas aprovadas
- **Service**: Serviços oferecidos
- **ServiceActivity**: Atividades de serviços

## 📊 Funcionalidades Avançadas

### Gestão de Shares e Valores
- Cálculo automático de percentuais ↔ valores USD/EUR
- Validação de distribuição completa (100%)
- Suporte a múltiplas moedas

### Tax Impacts e Compliance
- Cálculo automático de impactos fiscais
- Validação de combinações proibidas
- Scores de severidade

### Interface Administrativa
- Django Admin customizado com cores de status
- Filtros avançados e busca
- Fieldsets organizados por categoria
- Validações em tempo real

## 🛠️ Tecnologias

- **Backend**: Django 4.2, Python 3.11
- **Banco de Dados**: SQLite (desenvolvimento), PostgreSQL (produção)
- **Interface**: Django Admin customizado
- **Segurança**: Configuração via variáveis de ambiente
- **Deploy**: Heroku, DigitalOcean, AWS, VPS

## 📚 Documentação

- **[Guia de Desenvolvimento](DEVELOPMENT_GUIDE.md)** - Setup e padrões de desenvolvimento
- **[Guia de Deploy](DEPLOYMENT_GUIDE.md)** - Instruções de deploy para produção
- **[Referência da API](API_REFERENCE.md)** - Documentação completa dos modelos
- **[Manual do Django Admin](MANUAL_DJANGO_ADMIN_SIRIUS.md)** - Guia de uso da interface
- **[Changelog](CHANGELOG.md)** - Histórico de mudanças

## 🔧 Configuração

### Variáveis de Ambiente

```bash
# Desenvolvimento
DEBUG=True
SECRET_KEY=sua-chave-secreta
ALLOWED_HOSTS=localhost,127.0.0.1

# Produção
DEBUG=False
SECRET_KEY=chave-super-secreta-50-caracteres
ALLOWED_HOSTS=seudominio.com
DATABASE_URL=postgres://user:pass@host:port/db
```

### Comandos Úteis

```bash
# Verificar configuração
python manage.py check

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic

# Executar testes
python manage.py test
```

## 🚀 Deploy

### Heroku (Recomendado)

```bash
# Deploy rápido no Heroku
heroku create sua-app
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=sua-chave-secreta
heroku addons:create heroku-postgresql:mini
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

Consulte o [Guia de Deploy](DEPLOYMENT_GUIDE.md) para outras plataformas.

## 🧪 Testes

```bash
# Executar todos os testes
python manage.py test

# Testes de um app específico
python manage.py test corporate

# Testes com coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adicionar nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Padrões de Desenvolvimento

- Seguir PEP 8 para formatação
- Escrever testes para novas funcionalidades
- Documentar mudanças no CHANGELOG.md
- Usar commits descritivos

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Suporte

- **Documentação**: Consulte os guias na pasta docs/
- **Issues**: Abra uma issue no GitHub
- **Email**: suporte@sirius-system.com

## 🏆 Status do Projeto

- ✅ **Estável**: Sistema em produção
- ✅ **Documentado**: Documentação completa
- ✅ **Testado**: Cobertura de testes
- ✅ **Seguro**: Configurações de segurança implementadas

---

**Desenvolvido com ❤️ para profissionais de estruturação corporativa**

