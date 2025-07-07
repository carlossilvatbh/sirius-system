# Análise Django Admin - Sistema Sirius

## Estrutura do Projeto

O Sistema Sirius é um projeto Django 4.2.7 com 3 apps principais:
- **corporate**: Gerenciamento de estruturas corporativas, UBOs, classificações fiscais
- **estruturas_app**: App legado para estruturas (mantido para compatibilidade)
- **sales**: Gerenciamento de produtos e vendas

## Apps e Modelos Identificados

### 1. App Corporate
**Modelos registrados no Admin:**
- `TaxClassification`: Classificações fiscais
- `Structure`: Estruturas corporativas principais
- `UBO`: Ultimate Beneficial Owners (Beneficiários finais)
- `ValidationRule`: Regras de validação entre estruturas
- `JurisdictionAlert`: Alertas por jurisdição
- `Successor`: Sucessores de UBOs
- `Service`: Serviços oferecidos
- `ServiceActivity`: Atividades dos serviços

### 2. App Estruturas_app (Legado)
**Modelos registrados no Admin:**
- `Estrutura`: Estruturas legais (mantido para compatibilidade)

### 3. App Sales
**Modelos registrados no Admin:**
- `Product`: Produtos comerciais
- `ProductHierarchy`: Hierarquia de produtos
- `PersonalizedProduct`: Produtos personalizados
- `PersonalizedProductUBO`: Relação UBO-Produto personalizado

## Funcionalidades Específicas do Admin Identificadas

### Corporate App
1. **TaxClassificationAdmin**:
   - Lista: nome, descrição, data criação
   - Filtros: nome, data criação
   - Busca: nome, descrição

2. **StructureAdmin**:
   - Lista: nome, classificações fiscais, jurisdição, custos, status
   - Filtros: classificações fiscais, jurisdição, status, data criação
   - Busca: nome, descrição
   - Fieldsets organizados por categoria
   - Filter horizontal para classificações fiscais

3. **UBOAdmin**:
   - Lista: nome, tipo pessoa, email, telefone, país, status
   - Filtros: tipo pessoa, país, status, data criação
   - Busca: nome, email, documento
   - Fieldsets organizados por categoria

4. **ValidationRuleAdmin**:
   - Lista: estrutura A, estrutura B, tipo relacionamento, severidade
   - Filtros: tipo relacionamento, severidade, status
   - Busca: estruturas relacionadas, descrição

5. **JurisdictionAlertAdmin**:
   - Lista: título, jurisdição, tipo alerta, deadline, prioridade
   - Filtros: jurisdição, tipo alerta, deadline type, prioridade
   - Busca: título, descrição
   - Filter horizontal para estruturas e UBOs aplicáveis
   - Fieldsets detalhados para configuração de deadlines

6. **SuccessorAdmin**:
   - Lista: UBO proprietário, UBO sucessor, percentual, status
   - Filtros: status, efetivado, data criação
   - Busca: nomes dos UBOs

7. **ServiceAdmin**:
   - Lista: nome serviço, tipo, status, estrutura associada, custo
   - Filtros: tipo serviço, status, ativo
   - Busca: nome serviço, descrição
   - Inline para ServiceActivity
   - Fieldsets organizados

### Estruturas_app (Legado)
1. **EstruturaAdmin**:
   - Lista com formatação customizada de custos
   - Display de complexidade com cores
   - Fieldsets organizados por categoria
   - Campos readonly para timestamps
   - Métodos customizados para formatação

### Sales App
1. **ProductAdmin**:
   - Lista: nome, nome comercial, complexidade, uso, status
   - Filtros: complexidade, status, data criação
   - Busca: nome, nome comercial, descrição
   - Inline para ProductHierarchy

2. **PersonalizedProductAdmin**:
   - Lista: nome, tipo base, status, versão, percentual total
   - Filtros: status, versão, ativo
   - Busca: nome, descrição, produto base
   - Inline para PersonalizedProductUBO
   - Métodos customizados para display

## Características Técnicas Observadas

1. **Uso de Inlines**: ServiceActivityInline, ProductHierarchyInline, PersonalizedProductUBOInline
2. **Fieldsets organizados**: Agrupamento lógico de campos
3. **Filter horizontal**: Para relacionamentos many-to-many
4. **Métodos customizados**: Para formatação e display
5. **Formatação HTML**: Uso de format_html para cores e estilos
6. **Campos readonly**: Para metadados e timestamps
7. **Validações customizadas**: Nos modelos
8. **Ordenação customizada**: Em várias listas



## Funcionalidades Específicas Identificadas

### 1. Gestão de Classificações Fiscais
- **Modelo**: TaxClassification
- **Funcionalidades**:
  - Cadastro de classificações fiscais predefinidas
  - Busca por nome e descrição
  - Filtros por nome e data de criação
  - Relacionamento many-to-many com estruturas

### 2. Gestão de Estruturas Corporativas
- **Modelo**: Structure (principal) e Estrutura (legado)
- **Funcionalidades**:
  - Cadastro completo de estruturas legais
  - Gestão de jurisdições (US, Brasil, offshore)
  - Controle de custos (base e manutenção)
  - Scores de privacidade e compliance
  - Tempo de implementação
  - Documentação necessária
  - Status ativo/inativo

### 3. Gestão de UBOs (Ultimate Beneficial Owners)
- **Modelo**: UBO
- **Funcionalidades**:
  - Cadastro de pessoas físicas e jurídicas
  - Informações de contato completas
  - Documentação de identidade
  - Endereços por país
  - Status ativo/inativo

### 4. Sistema de Alertas por Jurisdição
- **Modelo**: JurisdictionAlert
- **Funcionalidades**:
  - Alertas específicos por jurisdição
  - Configuração de deadlines únicos ou recorrentes
  - Priorização de alertas
  - Aplicabilidade a estruturas e UBOs específicos
  - Cálculo automático de próximos deadlines

### 5. Gestão de Sucessão
- **Modelo**: Successor
- **Funcionalidades**:
  - Definição de sucessores para UBOs
  - Controle de percentuais
  - Status de efetivação
  - Datas de definição

### 6. Gestão de Serviços
- **Modelo**: Service e ServiceActivity
- **Funcionalidades**:
  - Cadastro de serviços oferecidos
  - Atividades relacionadas aos serviços
  - Controle de custos e duração
  - Status e responsáveis
  - Priorização de atividades

### 7. Gestão de Produtos Comerciais
- **Modelo**: Product, ProductHierarchy, PersonalizedProduct
- **Funcionalidades**:
  - Produtos com hierarquia de estruturas
  - Personalização de produtos
  - Controle de versões
  - Relacionamento com UBOs
  - Custos automáticos e manuais

## Recursos Avançados do Admin

### 1. Inlines (Edição em linha)
- ServiceActivityInline: Atividades dentro de serviços
- ProductHierarchyInline: Hierarquia dentro de produtos
- PersonalizedProductUBOInline: UBOs dentro de produtos personalizados

### 2. Fieldsets Organizados
- Agrupamento lógico de campos por categoria
- Seções colapsáveis para informações detalhadas
- Organização por: Basic Info, Costs, Implementation, Status, etc.

### 3. Filtros Horizontais
- Para relacionamentos many-to-many
- Facilita seleção múltipla de classificações fiscais
- Aplicação de alertas a múltiplas estruturas/UBOs

### 4. Métodos Customizados de Display
- Formatação de moedas (custo_base_formatted, custo_manutencao_formatted)
- Display com cores (complexidade_display)
- Concatenação de informações (get_full_jurisdiction_display)
- Cálculos dinâmicos (get_total_percentage)

### 5. Campos Readonly
- Timestamps (created_at, updated_at)
- Campos calculados automaticamente
- Metadados do sistema

### 6. Validações Customizadas
- Validação de relacionamentos entre estruturas
- Controle de percentuais de sucessão
- Validação de jurisdições e estados

## Configurações de Acesso

### URL do Admin
- Acesso via: `/admin/`
- Configurado em `sirius_project/urls.py`

### Apps Registrados
1. **corporate**: Funcionalidades principais do sistema
2. **estruturas_app**: Compatibilidade com versão anterior
3. **sales**: Gestão comercial e produtos

### Dependências
- Django 4.2.7
- django.contrib.admin (padrão)
- corsheaders (para API)
- whitenoise (arquivos estáticos)

