# MANUAL DO APP CORPORATE - STRUCTURES

**Data:** 9 de Janeiro de 2025  
**Objetivo:** Manual completo de uso do módulo Corporate para criação e gestão de estruturas corporativas

---

## 🎯 **VISÃO GERAL DO APP CORPORATE**

O App Corporate é o núcleo do sistema SIRIUS, responsável pela criação, gestão e validação de estruturas corporativas complexas. Permite modelar ownership hierárquico em múltiplas camadas com validação automática de compliance.

### **Funcionalidades Principais:**
- **Gestão de Entities** (empresas, fundos, trusts)
- **Criação de Structures** (organogramas corporativos)
- **EntityOwnership** (relacionamentos de propriedade)
- **Validation Rules** (compliance automático)
- **Tax Impact Analysis** (análise fiscal)

---

## 🏢 **GESTÃO DE ENTITIES**

### **O que são Entities:**
Entities representam qualquer pessoa jurídica que pode participar de uma estrutura corporativa: empresas, fundos, trusts, foundations, etc.

### **Acesso:**
```
Django Admin → Corporate → Entities
```

### **Campos Principais:**

**Informações Básicas:**
- **Name**: Nome da entidade
- **Entity Type**: Corporation, LLC, Trust, Fund, etc.
- **Tax Classification**: C-Corp, S-Corp, Ltda, etc.

**Jurisdição:**
- **Jurisdiction**: País (US, BR, KY, etc.)
- **US State**: Estado americano (se aplicável)
- **BR State**: Estado brasileiro (se aplicável)

**Shares:**
- **Total Shares**: Número total de ações/quotas

**Implementação:**
- **Implementation Templates**: Templates de implementação
- **Implementation Time**: Tempo estimado (dias)
- **Complexity**: Nível de complexidade (1-10)

**Tax Information:**
- **Tax Impact USA**: Impacto fiscal nos EUA
- **Tax Impact Brazil**: Impacto fiscal no Brasil
- **Tax Impact Others**: Outros impactos fiscais

**Privacy & Protection:**
- **Confidentiality Level**: Nível de confidencialidade
- **Asset Protection**: Proteção de ativos
- **Privacy Impact**: Impacto na privacidade
- **Privacy Score**: Score de privacidade (1-10)

**Banking & Compliance:**
- **Banking Relation Score**: Score bancário (1-10)
- **Compliance Score**: Score de compliance (1-10)
- **Banking Facility**: Facilidade bancária

**Documentação:**
- **Required Documentation**: Documentos necessários
- **Documents URL**: URL dos documentos
- **Required Forms USA**: Formulários americanos
- **Required Forms Brazil**: Formulários brasileiros

### **Como Criar uma Entity:**

**Passo 1 - Informações Básicas:**
1. Acesse `Corporate → Entities`
2. Clique em **"Add Entity"**
3. Preencha **Name** (ex: "Delaware Holding Corp")
4. Selecione **Entity Type** (ex: "Corporation")
5. Defina **Tax Classification** (ex: "C-Corp")

**Passo 2 - Jurisdição:**
1. Selecione **Jurisdiction** (ex: "US")
2. Se US, selecione **US State** (ex: "Delaware")
3. Se BR, selecione **BR State** (ex: "São Paulo")

**Passo 3 - Shares:**
1. Defina **Total Shares** (ex: 1000)

**Passo 4 - Implementação:**
1. Selecione **Implementation Templates**
2. Defina **Implementation Time** (ex: 30 dias)
3. Avalie **Complexity** (1-10)

**Passo 5 - Salvar:**
1. Clique em **"Save"**
2. Entity estará disponível para uso em Structures

---

## 🏗️ **CRIAÇÃO DE STRUCTURES**

### **O que são Structures:**
Structures são organogramas corporativos completos que modelam relacionamentos de propriedade entre Entities e UBOs (Parties) em múltiplas camadas hierárquicas.

### **Acesso:**
```
Django Admin → Corporate → Structures
```

### **Campos da Structure:**

**Informações Básicas:**
- **Name**: Nome da estrutura (ex: "International Holding Structure")
- **Description**: Descrição detalhada da estrutura
- **Status**: DRAFTING, SENT_FOR_APPROVAL, APPROVED

**Campos Calculados (Automáticos):**
- **Tax Impacts**: Impactos fiscais calculados automaticamente
- **Severity Levels**: Níveis de severidade baseados em validation rules

### **Como Criar uma Structure:**

**Passo 1 - Criar Structure Base:**
1. Acesse `Corporate → Structures`
2. Clique em **"Add Structure"**
3. Preencha **Name** (ex: "International Holding Structure")
4. Adicione **Description** detalhada
5. Status inicial será **"DRAFTING"**
6. Clique em **"Save"**

**Passo 2 - Adicionar EntityOwnerships:**
1. Acesse `Corporate → Entity Ownerships`
2. Clique em **"Add Entity Ownership"**
3. Configure conforme seções abaixo

---

## 🔗 **ENTITY OWNERSHIP (Relacionamentos)**

### **O que é EntityOwnership:**
EntityOwnership define quem possui o quê em uma estrutura. Pode ser:
- **UBO → Entity** (pessoa física possui empresa)
- **Entity → Entity** (empresa possui empresa)
- **Ownership misto** (múltiplos owners para mesma entity)

### **Campos do EntityOwnership:**

**Estrutura:**
- **Structure**: Estrutura à qual pertence

**Entity Owned:**
- **Owned Entity**: Entity que está sendo possuída

**Owner (um dos dois):**
- **Owner UBO**: Party (pessoa física) que possui
- **Owner Entity**: Entity (pessoa jurídica) que possui

**Identidade Corporativa:**
- **Corporate Name**: Nome corporativo do ownership
- **Hash Number**: Número identificador único

**Ownership:**
- **Owned Shares**: Número de ações/quotas possuídas
- **Ownership Percentage**: Percentual de propriedade

**Valoração:**
- **Share Value USD**: Valor por ação em USD
- **Share Value EUR**: Valor por ação em EUR
- **Total Value USD**: Valor total em USD (calculado)
- **Total Value EUR**: Valor total em EUR (calculado)

### **Cenários de Ownership:**

**Cenário 1 - UBO owns Entity (100%):**
```
Structure: International Holding
Owned Entity: Delaware Holding Corp
Owner UBO: John Smith
Corporate Name: John Smith Holdings
Hash Number: JSH001
Owned Shares: 1000
Ownership Percentage: 100%
Share Value USD: 100.00
```

**Cenário 2 - Multiple UBOs own Entity:**
```
Ownership 1:
- Owned Entity: Delaware Holding Corp
- Owner UBO: John Smith (60%)
- Owned Shares: 600

Ownership 2:
- Owned Entity: Delaware Holding Corp  
- Owner UBO: Maria Silva (40%)
- Owned Shares: 400
```

**Cenário 3 - Entity owns Entity:**
```
Structure: International Holding
Owned Entity: Brazil Subsidiary Ltda
Owner Entity: Delaware Holding Corp
Corporate Name: Delaware Holdings Brazil
Hash Number: DHB001
Owned Shares: 10000
Ownership Percentage: 100%
```

**Cenário 4 - Hierarquia Complexa (3 camadas):**
```
Camada 1: UBOs → Holding
- John Smith (60%) → Delaware Holding Corp
- Maria Silva (40%) → Delaware Holding Corp

Camada 2: Holding → Subsidiárias
- Delaware Holding Corp (100%) → Brazil Subsidiary
- Delaware Holding Corp (100%) → Cayman Fund

Camada 3: Subsidiária → Sub-subsidiária
- Brazil Subsidiary (100%) → Local Operations Ltda
```

### **Validações Automáticas:**

**Validação de 100%:**
- Sistema verifica se ownership total = 100%
- Alerta se distribuição incompleta
- Bloqueia aprovação se inválido

**Validação de Shares:**
- Owned Shares não pode exceder Total Shares da Entity
- Auto-cálculo entre shares ↔ percentage
- Validação de valores USD/EUR

**Validação de Combinações:**
- Validation Rules verificam combinações proibidas
- Tax impacts calculados automaticamente
- Severity levels determinados

---

## 📊 **VALIDATION RULES**

### **O que são Validation Rules:**
Regras que definem combinações permitidas/proibidas entre entities, calculam tax impacts e determinam severity levels.

### **Acesso:**
```
Django Admin → Corporate → Validation Rules
```

### **Campos:**

**Entities:**
- **Parent Entity**: Entity "pai" na relação
- **Related Entity**: Entity "filho" na relação

**Relacionamento:**
- **Relationship Type**: Tipo de relacionamento
- **Severity**: HIGH, MEDIUM, LOW
- **Description**: Descrição da regra

**Tax Information:**
- **Tax Impacts**: Impactos fiscais detalhados

### **Exemplo de Validation Rule:**
```
Parent Entity: Delaware Corporation
Related Entity: Brazil Ltda
Relationship Type: SUBSIDIARY
Severity: MEDIUM
Description: Delaware corp owning Brazilian subsidiary requires CFC compliance
Tax Impacts: US CFC rules apply, Brazilian withholding tax on distributions
```

---

## 🎨 **INTERFACE VISUAL**

### **Cores de Status:**
- **DRAFTING**: Cinza (#6C757D)
- **SENT_FOR_APPROVAL**: Azul (#17A2B8)
- **APPROVED**: Verde (#28A745)

### **Indicadores Visuais:**
- **Tax Impact**: Badges coloridos por severidade
- **Ownership %**: Barras de progresso
- **Validation Status**: Ícones de check/warning

---

## 🔄 **FLUXO DE TRABALHO**

### **Fluxo Completo de Criação:**

**Etapa 1 - Preparação:**
1. Receber requisição do Sales
2. Analisar requirements
3. Identificar entities necessárias

**Etapa 2 - Criação de Entities:**
1. Criar/verificar entities existentes
2. Configurar jurisdições e shares
3. Definir tax classifications

**Etapa 3 - Criação da Structure:**
1. Criar structure base
2. Adicionar description detalhada
3. Manter status DRAFTING

**Etapa 4 - Configuração de Ownerships:**
1. Criar EntityOwnerships camada por camada
2. Começar pelos UBOs (camada superior)
3. Descer hierarquia até subsidiárias

**Etapa 5 - Validação:**
1. Verificar 100% de distribuição
2. Revisar tax impacts
3. Confirmar compliance

**Etapa 6 - Aprovação:**
1. Mudar status para SENT_FOR_APPROVAL
2. Enviar para Sales
3. Aguardar feedback

### **Exemplo Prático - Holding Internacional:**

**Requisição:** "Cliente quer holding em Delaware controlando subsidiárias no Brasil e Cayman"

**Entities Necessárias:**
1. Delaware Holding Corp (US/Delaware)
2. Brazil Operations Ltda (BR/São Paulo)  
3. Cayman Investment Fund (KY)

**Structure: "International Holding Structure"**

**Ownerships:**
```
1. John Smith (60%) → Delaware Holding Corp
   - Corporate Name: "John Smith Holdings"
   - Hash Number: "JSH001"
   - Shares: 600/1000

2. Maria Silva (40%) → Delaware Holding Corp
   - Corporate Name: "Maria Silva Holdings"  
   - Hash Number: "MSH001"
   - Shares: 400/1000

3. Delaware Holding Corp (100%) → Brazil Operations Ltda
   - Corporate Name: "Delaware Holdings Brazil"
   - Hash Number: "DHB001"
   - Shares: 10000/10000

4. Delaware Holding Corp (100%) → Cayman Investment Fund
   - Corporate Name: "Delaware Holdings Cayman"
   - Hash Number: "DHC001"
   - Shares: 5000/5000
```

**Resultado:** Estrutura hierárquica com 2 UBOs controlando holding americana que possui subsidiárias no Brasil e Cayman.

---

## 🧮 **CÁLCULOS AUTOMÁTICOS**

### **Auto-preenchimento Shares ↔ Percentage:**

**Se informar Shares:**
- Sistema calcula Ownership Percentage automaticamente
- Fórmula: (Owned Shares / Total Shares) × 100

**Se informar Percentage:**
- Sistema calcula Owned Shares automaticamente
- Fórmula: (Ownership Percentage / 100) × Total Shares

### **Cálculo de Valores:**

**Total Value USD:**
- Fórmula: Owned Shares × Share Value USD

**Total Value EUR:**
- Fórmula: Owned Shares × Share Value EUR

### **Tax Impacts:**
- Calculados automaticamente baseado em Validation Rules
- Agregados por Structure
- Exibidos em formato legível

---

## 🔍 **BUSCA E FILTROS**

### **Filtros Disponíveis:**

**Entities:**
- Por Entity Type
- Por Jurisdiction
- Por Active status
- Por Created date

**Structures:**
- Por Status
- Por Created date
- Por Tax impacts

**EntityOwnerships:**
- Por Structure
- Por Owned Entity
- Por Owner (UBO ou Entity)

### **Busca Textual:**
- **Entities**: Por name, tax_classification
- **Structures**: Por name, description
- **EntityOwnerships**: Por corporate_name, hash_number

---

## 📋 **RELATÓRIOS**

### **Relatório de Structure:**
- **Organograma visual** da estrutura
- **Lista de ownerships** por camada
- **Tax impacts** consolidados
- **Compliance status**

### **Relatório de Entity:**
- **Participações** em structures
- **Ownership history**
- **Tax implications**
- **Banking relationships**

---

## 🚨 **ALERTAS E VALIDAÇÕES**

### **Alertas Automáticos:**
- **Distribuição incompleta** (< 100%)
- **Excesso de shares** (> Total Shares)
- **Combinações proibidas** (Validation Rules)
- **Tax compliance** issues

### **Validações de Salvamento:**
- **Campos obrigatórios** preenchidos
- **Valores numéricos** válidos
- **Relacionamentos** consistentes
- **Business rules** respeitadas

---

## 🔧 **SOLUÇÃO DE PROBLEMAS**

### **Erro: "Distribuição não soma 100%"**
**Solução:**
1. Verifique todos os EntityOwnerships da mesma Entity
2. Some os percentuais manualmente
3. Ajuste percentuais para totalizar 100%

### **Erro: "Shares excedem total"**
**Solução:**
1. Verifique Total Shares da Entity
2. Confirme Owned Shares de todos os ownerships
3. Ajuste valores para não exceder total

### **Erro: "Combinação proibida"**
**Solução:**
1. Verifique Validation Rules aplicáveis
2. Revise estrutura proposta
3. Considere jurisdições alternativas

### **Tax Impacts não calculam**
**Solução:**
1. Verifique se Validation Rules existem
2. Confirme relacionamentos entre entities
3. Salve Structure novamente

---

## 📞 **SUPORTE AVANÇADO**

### **Cenários Complexos:**
- **Structures circulares**: Como evitar
- **Multiple jurisdictions**: Compliance
- **Tax optimization**: Estratégias
- **Regulatory changes**: Adaptação

### **Consultoria Especializada:**
- **Estruturas internacionais**
- **Compliance multi-jurisdicional**
- **Otimização fiscal**
- **Due diligence**

---

## 🏆 **MELHORES PRÁTICAS**

### **Planejamento:**
1. **Analise** requisitos completamente
2. **Identifique** entities necessárias
3. **Desenhe** estrutura no papel primeiro
4. **Valide** compliance antes de implementar

### **Implementação:**
1. **Crie entities** antes de structures
2. **Configure ownerships** camada por camada
3. **Valide** cada etapa
4. **Documente** decisões importantes

### **Manutenção:**
1. **Monitore** mudanças regulatórias
2. **Atualize** validation rules
3. **Revise** structures periodicamente
4. **Mantenha** documentação atualizada

---

## 🎯 **RESUMO EXECUTIVO**

O App Corporate é uma ferramenta poderosa para:

1. **Modelar** estruturas corporativas complexas
2. **Validar** compliance automaticamente
3. **Calcular** tax impacts
4. **Gerenciar** ownership hierárquico
5. **Documentar** decisões estruturais

**Resultado:** Criação eficiente e segura de estruturas corporativas com compliance automático e validação completa.

**🎉 Use este manual para dominar a criação de structures no SIRIUS!**

