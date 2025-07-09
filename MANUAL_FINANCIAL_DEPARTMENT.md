# MANUAL DO APP FINANCIAL DEPARTMENT

**Data:** 9 de Janeiro de 2025  
**Objetivo:** Manual completo de uso do módulo Financial Department para gestão de preços e custos

---

## 🎯 **VISÃO GERAL DO APP FINANCIAL DEPARTMENT**

O App Financial Department é responsável pela gestão financeira centralizada do sistema SIRIUS, incluindo preços de entities, custos de incorporação, preços de serviços e análise de rentabilidade.

### **Funcionalidades Principais:**
- **Entity Prices** (preços de entities por jurisdição)
- **Incorporation Costs** (componentes de custo)
- **Service Prices** (preços de serviços)
- **Service Costs** (custos de serviços)
- **Análise de Rentabilidade**

---

## 💰 **ENTITY PRICES (Preços de Entities)**

### **O que são Entity Prices:**
Entity Prices definem o preço de incorporação de diferentes tipos de entities em diferentes jurisdições, incluindo markup e moedas base.

### **Acesso:**
```
Django Admin → Financial Department → Entity Prices
```

### **Campos do Entity Price:**

**Entity e Jurisdição:**
- **Entity Type**: Tipo de entity (Corporation, LLC, Trust, etc.)
- **Jurisdiction**: Jurisdição (US, BR, KY, etc.)

**Preços Base:**
- **Base Price**: Preço base em moeda local
- **Base Currency**: Moeda base (USD, EUR, BRL, etc.)

**Markup:**
- **Markup Type**: PERCENTAGE, FIXED_AMOUNT
- **Markup Value**: Valor do markup

**Preços Calculados (Automáticos):**
- **Final Price**: Preço final (base + markup)
- **Price USD**: Preço convertido para USD
- **Price EUR**: Preço convertido para EUR

**Configurações:**
- **Is Active**: Preço ativo/inativo
- **Effective Date**: Data de vigência
- **Notes**: Observações

### **Tipos de Markup:**

**PERCENTAGE:**
- Markup aplicado como percentual sobre o preço base
- Exemplo: Base $5,000 + 20% = $6,000

**FIXED_AMOUNT:**
- Markup aplicado como valor fixo
- Exemplo: Base $5,000 + $1,000 = $6,000

### **Como Criar um Entity Price:**

**Passo 1 - Definir Entity e Jurisdição:**
1. Acesse `Financial Department → Entity Prices`
2. Clique em **"Add Entity Price"**
3. Selecione **Entity Type** (ex: "Corporation")
4. Selecione **Jurisdiction** (ex: "US")

**Passo 2 - Configurar Preço Base:**
1. Defina **Base Price** (ex: 5000.00)
2. Selecione **Base Currency** (ex: "USD")

**Passo 3 - Configurar Markup:**
1. Selecione **Markup Type** (ex: "PERCENTAGE")
2. Defina **Markup Value** (ex: 20.00 para 20%)

**Passo 4 - Configurações Finais:**
1. Marque **Is Active** = True
2. Defina **Effective Date**
3. Adicione **Notes** se necessário
4. Clique em **"Save"**

### **Exemplo de Entity Price:**
```
Entity Type: Corporation
Jurisdiction: US
Base Price: 5,000.00
Base Currency: USD
Markup Type: PERCENTAGE
Markup Value: 20.00
Final Price: 6,000.00 (calculado automaticamente)
Price USD: 6,000.00
Price EUR: 5,400.00 (convertido automaticamente)
Is Active: True
Effective Date: 2025-01-01
Notes: "Standard Delaware Corporation pricing"
```

---

## 🏗️ **INCORPORATION COSTS (Custos de Incorporação)**

### **O que são Incorporation Costs:**
Incorporation Costs são componentes individuais que compõem o custo total de incorporação de uma entity, permitindo análise detalhada de rentabilidade.

### **Acesso:**
```
Django Admin → Financial Department → Incorporation Costs
```

### **Campos do Incorporation Cost:**

**Relacionamento:**
- **Entity Price**: Entity Price ao qual pertence

**Componente de Custo:**
- **Cost Type**: Tipo de custo (veja lista abaixo)
- **Description**: Descrição detalhada

**Valores:**
- **Cost Amount**: Valor do custo
- **Cost Currency**: Moeda do custo

**Fornecedor:**
- **Supplier**: Fornecedor do serviço
- **Supplier Reference**: Referência do fornecedor

### **Tipos de Custo (Cost Types):**

**GOVERNMENT_FEES:**
- Taxas governamentais obrigatórias
- Exemplo: Taxa de registro na Junta Comercial

**LEGAL_FEES:**
- Honorários advocatícios
- Exemplo: Elaboração de contrato social

**ACCOUNTING_FEES:**
- Honorários contábeis
- Exemplo: Abertura de livros contábeis

**REGISTERED_AGENT:**
- Serviços de agente registrado
- Exemplo: Registered agent em Delaware

**REGISTERED_OFFICE:**
- Serviços de endereço registrado
- Exemplo: Endereço comercial

**APOSTILLE:**
- Serviços de apostilamento
- Exemplo: Apostila de documentos

**TRANSLATION:**
- Serviços de tradução
- Exemplo: Tradução juramentada

**NOTARIZATION:**
- Serviços notariais
- Exemplo: Reconhecimento de firma

**BANK_ACCOUNT:**
- Abertura de conta bancária
- Exemplo: Conta corporativa

**OTHER:**
- Outros custos diversos
- Exemplo: Custos de courier

### **Como Criar um Incorporation Cost:**

**Passo 1 - Selecionar Entity Price:**
1. Acesse `Financial Department → Incorporation Costs`
2. Clique em **"Add Incorporation Cost"**
3. Selecione **Entity Price** correspondente

**Passo 2 - Definir Custo:**
1. Selecione **Cost Type** apropriado
2. Adicione **Description** detalhada
3. Defina **Cost Amount**
4. Selecione **Cost Currency**

**Passo 3 - Fornecedor:**
1. Especifique **Supplier** (se aplicável)
2. Adicione **Supplier Reference**

**Passo 4 - Salvar:**
1. Clique em **"Save"**
2. Custo será incluído na análise de rentabilidade

### **Exemplo de Incorporation Costs para Delaware Corporation:**
```
Cost 1:
- Entity Price: Delaware Corporation (US)
- Cost Type: GOVERNMENT_FEES
- Description: "Delaware State filing fee"
- Cost Amount: 89.00
- Cost Currency: USD
- Supplier: "Delaware Division of Corporations"

Cost 2:
- Entity Price: Delaware Corporation (US)
- Cost Type: REGISTERED_AGENT
- Description: "Registered agent service (1 year)"
- Cost Amount: 150.00
- Cost Currency: USD
- Supplier: "Delaware Registered Agent Inc."

Cost 3:
- Entity Price: Delaware Corporation (US)
- Cost Type: LEGAL_FEES
- Description: "Articles of incorporation preparation"
- Cost Amount: 500.00
- Cost Currency: USD
- Supplier: "Internal Legal Team"
```

---

## 🛠️ **SERVICE PRICES (Preços de Serviços)**

### **O que são Service Prices:**
Service Prices definem preços de serviços adicionais oferecidos além da incorporação básica, como serviços bancários, compliance, etc.

### **Acesso:**
```
Django Admin → Financial Department → Service Prices
```

### **Campos do Service Price:**

**Serviço:**
- **Service Name**: Nome do serviço
- **Service Category**: Categoria do serviço
- **Description**: Descrição detalhada

**Preços:**
- **Base Price**: Preço base
- **Base Currency**: Moeda base
- **Markup Type**: PERCENTAGE, FIXED_AMOUNT
- **Markup Value**: Valor do markup
- **Final Price**: Preço final (calculado)

**Configurações:**
- **Is Recurring**: Serviço recorrente
- **Billing Frequency**: Frequência de cobrança
- **Is Active**: Ativo/inativo

### **Categorias de Serviço:**

**BANKING:**
- Serviços bancários
- Exemplo: Abertura de conta, manutenção

**COMPLIANCE:**
- Serviços de compliance
- Exemplo: Annual reports, tax filings

**LEGAL:**
- Serviços legais
- Exemplo: Contratos, due diligence

**ACCOUNTING:**
- Serviços contábeis
- Exemplo: Bookkeeping, financial statements

**SECRETARIAL:**
- Serviços secretariais
- Exemplo: Board meetings, resolutions

**OTHER:**
- Outros serviços
- Exemplo: Serviços especializados

### **Como Criar um Service Price:**

**Passo 1 - Definir Serviço:**
1. Acesse `Financial Department → Service Prices`
2. Clique em **"Add Service Price"**
3. Preencha **Service Name**
4. Selecione **Service Category**
5. Adicione **Description**

**Passo 2 - Configurar Preço:**
1. Defina **Base Price**
2. Selecione **Base Currency**
3. Configure **Markup Type** e **Markup Value**

**Passo 3 - Configurações:**
1. Marque **Is Recurring** se aplicável
2. Defina **Billing Frequency**
3. Marque **Is Active** = True

### **Exemplo de Service Price:**
```
Service Name: "Annual Compliance Delaware"
Service Category: COMPLIANCE
Description: "Annual report filing and registered agent maintenance"
Base Price: 300.00
Base Currency: USD
Markup Type: PERCENTAGE
Markup Value: 15.00
Final Price: 345.00
Is Recurring: True
Billing Frequency: ANNUAL
Is Active: True
```

---

## 💸 **SERVICE COSTS (Custos de Serviços)**

### **O que são Service Costs:**
Service Costs são os custos associados à prestação de serviços, permitindo análise de rentabilidade por serviço.

### **Acesso:**
```
Django Admin → Financial Department → Service Costs
```

### **Campos do Service Cost:**

**Relacionamento:**
- **Service Price**: Service Price ao qual pertence

**Custo:**
- **Cost Type**: Tipo de custo
- **Description**: Descrição do custo
- **Cost Amount**: Valor do custo
- **Cost Currency**: Moeda do custo

**Fornecedor:**
- **Supplier**: Fornecedor
- **Supplier Reference**: Referência

### **Como Criar um Service Cost:**

**Passo 1 - Selecionar Service Price:**
1. Acesse `Financial Department → Service Costs`
2. Clique em **"Add Service Cost"**
3. Selecione **Service Price**

**Passo 2 - Definir Custo:**
1. Selecione **Cost Type**
2. Adicione **Description**
3. Defina **Cost Amount** e **Cost Currency**

**Passo 3 - Fornecedor:**
1. Especifique **Supplier**
2. Adicione **Supplier Reference**

---

## 📊 **ANÁLISE DE RENTABILIDADE**

### **Cálculos Automáticos:**

**Para Entity Prices:**
- **Total Costs**: Soma de todos os Incorporation Costs
- **Gross Margin**: Final Price - Total Costs
- **Margin %**: (Gross Margin / Final Price) × 100

**Para Service Prices:**
- **Total Service Costs**: Soma de todos os Service Costs
- **Service Margin**: Final Price - Total Service Costs
- **Service Margin %**: (Service Margin / Final Price) × 100

### **Relatórios de Rentabilidade:**

**Por Entity Type:**
- Margem por tipo de entity
- Comparação entre jurisdições
- Análise de competitividade

**Por Serviço:**
- Rentabilidade por categoria
- Serviços mais/menos lucrativos
- Oportunidades de otimização

---

## 💱 **GESTÃO DE MOEDAS**

### **Moedas Suportadas:**
- **USD** - Dólar Americano
- **EUR** - Euro
- **BRL** - Real Brasileiro
- **GBP** - Libra Esterlina
- **CHF** - Franco Suíço
- **CAD** - Dólar Canadense

### **Conversão Automática:**
- Preços convertidos automaticamente para USD e EUR
- Taxas de câmbio atualizadas periodicamente
- Histórico de conversões mantido

### **Configuração de Taxas:**
- Taxas podem ser configuradas manualmente
- Integração com APIs de câmbio (futuro)
- Alertas para variações significativas

---

## 📈 **RELATÓRIOS FINANCEIROS**

### **Relatório de Preços:**
- Lista completa de Entity Prices
- Comparação entre jurisdições
- Histórico de alterações

### **Relatório de Custos:**
- Breakdown detalhado de custos
- Análise por fornecedor
- Identificação de oportunidades

### **Relatório de Rentabilidade:**
- Margem por produto/serviço
- Tendências de rentabilidade
- Benchmarking competitivo

### **Relatório de Serviços:**
- Performance de serviços recorrentes
- Análise de churn
- Oportunidades de upsell

---

## 🔍 **BUSCA E FILTROS**

### **Filtros Disponíveis:**

**Entity Prices:**
- Por Entity Type
- Por Jurisdiction
- Por Is Active
- Por Base Currency

**Incorporation Costs:**
- Por Cost Type
- Por Supplier
- Por Cost Currency

**Service Prices:**
- Por Service Category
- Por Is Recurring
- Por Is Active

**Service Costs:**
- Por Cost Type
- Por Supplier

### **Busca Textual:**
- **Entity Prices**: Por entity_type, jurisdiction
- **Service Prices**: Por service_name, description
- **Costs**: Por description, supplier

---

## 📊 **DASHBOARD FINANCEIRO**

### **KPIs Principais:**
- **Revenue**: Receita total
- **Costs**: Custos totais
- **Gross Margin**: Margem bruta
- **Margin %**: Percentual de margem

### **Gráficos:**
- **Revenue by Entity Type**: Receita por tipo
- **Margin Trends**: Tendências de margem
- **Cost Breakdown**: Breakdown de custos
- **Service Performance**: Performance de serviços

---

## 🚨 **ALERTAS FINANCEIROS**

### **Alertas Automáticos:**
- **Margem baixa**: < 20%
- **Custo alto**: Acima da média
- **Preço desatualizado**: > 6 meses
- **Moeda volátil**: Variação > 10%

### **Notificações:**
- **Email**: Para gestores financeiros
- **Dashboard**: Alertas visuais
- **Relatórios**: Seção de alertas

---

## 🔧 **CONFIGURAÇÕES AVANÇADAS**

### **Markup Automático:**
- Regras de markup por categoria
- Ajuste automático por volume
- Desconto por fidelidade

### **Integração Contábil:**
- Export para sistemas contábeis
- Reconciliação automática
- Controle de receitas/custos

### **Aprovações:**
- Workflow de aprovação de preços
- Limites de autorização
- Histórico de alterações

---

## 🔧 **SOLUÇÃO DE PROBLEMAS**

### **Problema: "Preço final não calcula"**
**Soluções:**
1. Verifique se Base Price está preenchido
2. Confirme Markup Type e Value
3. Salve novamente o registro

### **Problema: "Conversão de moeda incorreta"**
**Soluções:**
1. Verifique taxa de câmbio configurada
2. Confirme Base Currency
3. Atualize taxas manualmente

### **Problema: "Custos não aparecem no relatório"**
**Soluções:**
1. Verifique se Entity Price está ativo
2. Confirme vinculação dos custos
3. Verifique filtros aplicados

---

## 🏆 **MELHORES PRÁTICAS**

### **Gestão de Preços:**
1. **Revise** preços trimestralmente
2. **Monitore** competitividade
3. **Ajuste** markup conforme mercado
4. **Documente** alterações

### **Controle de Custos:**
1. **Negocie** com fornecedores
2. **Monitore** variações
3. **Otimize** processos
4. **Analise** rentabilidade

### **Relatórios:**
1. **Gere** relatórios mensais
2. **Analise** tendências
3. **Identifique** oportunidades
4. **Tome** ações corretivas

---

## 🎯 **RESUMO EXECUTIVO**

O App Financial Department é fundamental para:

1. **Controlar** preços e custos
2. **Analisar** rentabilidade
3. **Otimizar** margens
4. **Monitorar** performance financeira
5. **Tomar** decisões baseadas em dados

**Resultado:** Gestão financeira eficiente, rentabilidade otimizada e controle total sobre preços e custos.

**🎉 Use este manual para dominar a gestão financeira no SIRIUS!**

