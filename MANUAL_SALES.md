# MANUAL DO APP SALES

**Data:** 9 de Janeiro de 2025  
**Objetivo:** Manual completo de uso do módulo Sales para gestão de partners, contacts e fluxo de requisições

---

## 🎯 **VISÃO GERAL DO APP SALES**

O App Sales é responsável pela gestão comercial do sistema SIRIUS, incluindo relacionamento com partners, gestão de contacts e todo o fluxo de requisições de estruturas corporativas.

### **Funcionalidades Principais:**
- **Gestão de Partners** (clientes e parceiros comerciais)
- **Gestão de Contacts** (pontos de contato)
- **Structure Requests** (requisições de estruturas)
- **Structure Approvals** (aprovações e feedback)

---

## 👥 **GESTÃO DE PARTNERS**

### **O que são Partners:**
Partners são clientes ou parceiros comerciais que solicitam estruturas corporativas. Podem ser pessoas físicas ou jurídicas que necessitam de serviços de estruturação.

### **Acesso:**
```
Django Admin → Sales → Partners
```

### **Campos do Partner:**

**Informação Principal:**
- **Party**: Vinculação com Party (UBO) do sistema
- **Company Name**: Nome da empresa (se aplicável)
- **Address**: Endereço completo

**Relacionamento Comercial:**
- **Partnership Type**: Tipo de parceria
- **Status**: Active, Inactive, Prospect
- **Priority Level**: High, Medium, Low

**Histórico:**
- **Created**: Data de criação
- **Updated**: Última atualização

### **Como Criar um Partner:**

**Passo 1 - Verificar Party:**
1. Acesse `Parties → Parties`
2. Verifique se a pessoa já existe
3. Se não existir, crie primeiro a Party

**Passo 2 - Criar Partner:**
1. Acesse `Sales → Partners`
2. Clique em **"Add Partner"**
3. Selecione **Party** existente
4. Preencha **Company Name** (se empresa)
5. Adicione **Address** completo

**Passo 3 - Configurar Relacionamento:**
1. Defina **Partnership Type**
2. Configure **Status** (geralmente "Active")
3. Defina **Priority Level**

**Passo 4 - Salvar:**
1. Clique em **"Save"**
2. Partner estará disponível para requisições

### **Exemplo de Partner:**
```
Party: John Smith
Company Name: Smith Holdings LLC
Address: 123 Wall Street, New York, NY 10005
Partnership Type: Premium Client
Status: Active
Priority Level: High
```

---

## 📞 **GESTÃO DE CONTACTS**

### **O que são Contacts:**
Contacts são pontos de contato específicos dentro de uma organização ou para um partner. Facilitam a comunicação durante o processo de estruturação.

### **Acesso:**
```
Django Admin → Sales → Contacts
```

### **Campos do Contact:**

**Informação Pessoal:**
- **Name**: Nome completo
- **Email**: Email principal
- **Phone**: Telefone de contato

**Relacionamento:**
- **Partner**: Partner ao qual pertence
- **Position**: Cargo/posição
- **Department**: Departamento

**Preferências:**
- **Preferred Contact Method**: Email, Phone, WhatsApp
- **Language**: Idioma preferido
- **Time Zone**: Fuso horário

**Status:**
- **Is Primary**: Contact principal
- **Is Active**: Ativo/inativo

### **Como Criar um Contact:**

**Passo 1 - Informações Básicas:**
1. Acesse `Sales → Contacts`
2. Clique em **"Add Contact"**
3. Preencha **Name** completo
4. Adicione **Email** e **Phone**

**Passo 2 - Vinculação:**
1. Selecione **Partner** correspondente
2. Defina **Position** (ex: "CFO", "Legal Counsel")
3. Especifique **Department** (ex: "Finance", "Legal")

**Passo 3 - Preferências:**
1. Configure **Preferred Contact Method**
2. Selecione **Language**
3. Defina **Time Zone**

**Passo 4 - Status:**
1. Marque **Is Primary** se for contact principal
2. Confirme **Is Active** = True
3. Clique em **"Save"**

### **Exemplo de Contact:**
```
Name: Maria Silva
Email: maria.silva@smithholdings.com
Phone: +1 (555) 123-4567
Partner: Smith Holdings LLC
Position: Chief Financial Officer
Department: Finance
Preferred Contact Method: Email
Language: English
Time Zone: America/New_York
Is Primary: True
Is Active: True
```

---

## 📋 **STRUCTURE REQUESTS (Requisições)**

### **O que são Structure Requests:**
Structure Requests são solicitações formais de criação de estruturas corporativas. Contêm todos os detalhes necessários para que a equipe Corporate desenvolva a estrutura.

### **Acesso:**
```
Django Admin → Sales → Structure Requests
```

### **Campos da Structure Request:**

**Informação Principal:**
- **Description**: Descrição detalhada da estrutura solicitada
- **Point of Contact Party**: Party responsável pela comunicação

**Parties Envolvidas:**
- **Requesting Parties**: Parties que farão parte da estrutura

**Status e Timing:**
- **Status**: SUBMITTED, IN_REVIEW, IN_PROGRESS, COMPLETED
- **Submitted At**: Data/hora de submissão
- **Updated At**: Última atualização

**Relacionamento:**
- **Related Structure**: Structure criada (quando aplicável)

### **Status da Structure Request:**

**SUBMITTED** 🟡
- Requisição recém-criada
- Aguardando análise da equipe Corporate
- Visível no Dashboard como "Pending Request"

**IN_REVIEW** 🔵
- Corporate iniciou análise
- Requisitos sendo avaliados
- Possíveis esclarecimentos necessários

**IN_PROGRESS** 🟠
- Corporate está desenvolvendo a estrutura
- Structure sendo criada no sistema
- EntityOwnerships sendo configurados

**COMPLETED** 🟢
- Structure finalizada
- Enviada para aprovação do Sales
- Aguardando feedback final

### **Como Criar uma Structure Request:**

**Passo 1 - Informações Básicas:**
1. Acesse `Sales → Structure Requests`
2. Clique em **"Add Structure Request"**
3. Escreva **Description** detalhada

**Exemplo de Description:**
```
"Cliente necessita de holding internacional com as seguintes características:
- Holding em Delaware (EUA) 
- Subsidiária operacional no Brasil (São Paulo)
- Fundo de investimento em Cayman Islands
- Estrutura de propriedade: John Smith (60%) e Maria Silva (40%)
- Objetivo: Otimização fiscal e proteção de ativos
- Timeline: 45 dias para implementação"
```

**Passo 2 - Point of Contact:**
1. Selecione **Point of Contact Party**
2. Deve ser a pessoa principal para comunicação
3. Geralmente o decision maker

**Passo 3 - Requesting Parties:**
1. Adicione todas as **Requesting Parties**
2. Incluir todos os UBOs que farão parte da estrutura
3. Use Ctrl+Click para seleção múltipla

**Passo 4 - Finalizar:**
1. Status será automaticamente **"SUBMITTED"**
2. **Submitted At** será preenchido automaticamente
3. Clique em **"Save"**

### **Exemplo Completo de Structure Request:**
```
Description: "International holding structure for real estate investments. 
Delaware corporation as holding company, owning Brazilian Ltda for local 
operations and Cayman fund for international investments. 
John Smith (60%) and Maria Silva (40%) ownership."

Point of Contact Party: John Smith
Requesting Parties: [John Smith, Maria Silva]
Status: SUBMITTED
Submitted At: 2025-01-09 14:30:00
```

---

## ✅ **STRUCTURE APPROVALS (Aprovações)**

### **O que são Structure Approvals:**
Structure Approvals são o feedback final do Sales sobre structures criadas pela equipe Corporate. Permitem aprovar, solicitar correções ou rejeitar estruturas.

### **Acesso:**
```
Django Admin → Sales → Structure Approvals
```

### **Campos da Structure Approval:**

**Relacionamento:**
- **Structure**: Structure sendo avaliada
- **Structure Request**: Requisição original (se aplicável)

**Decisão:**
- **Action**: APPROVED, APPROVED_WITH_PRICE_CHANGE, NEED_CORRECTION, REJECTED
- **Comments**: Comentários detalhados

**Responsável:**
- **Approved By**: Usuário que fez a aprovação
- **Approved At**: Data/hora da aprovação

### **Ações de Approval:**

**APPROVED** ✅
- Structure aprovada sem alterações
- Pronta para implementação
- Cliente pode ser notificado

**APPROVED_WITH_PRICE_CHANGE** 💰
- Structure aprovada com ajuste de preço
- Requer renegociação comercial
- Implementação pode prosseguir

**NEED_CORRECTION** ⚠️
- Structure precisa de ajustes
- Retorna para Corporate
- Comentários específicos obrigatórios

**REJECTED** ❌
- Structure rejeitada
- Não atende requisitos
- Nova abordagem necessária

### **Como Processar uma Structure Approval:**

**Passo 1 - Acessar Approval:**
1. Acesse `Sales → Structure Approvals`
2. Clique em **"Add Structure Approval"**
3. Ou use ação rápida do Dashboard

**Passo 2 - Selecionar Structure:**
1. Escolha **Structure** para avaliar
2. Vincule **Structure Request** original (se aplicável)

**Passo 3 - Analisar Structure:**
1. Revise entities criadas
2. Verifique ownerships configurados
3. Confirme tax impacts
4. Valide contra requisitos originais

**Passo 4 - Tomar Decisão:**
1. Selecione **Action** apropriada
2. Adicione **Comments** detalhados
3. **Approved By** será preenchido automaticamente
4. Clique em **"Save"**

### **Exemplos de Comments por Action:**

**APPROVED:**
```
"Structure meets all requirements perfectly. Delaware holding with 
Brazilian subsidiary and Cayman fund configured correctly. 
Ownership percentages match client specifications (60%/40%). 
Tax optimization achieved. Ready for implementation."
```

**APPROVED_WITH_PRICE_CHANGE:**
```
"Structure approved but complexity higher than estimated. 
Additional compliance requirements for Cayman fund increase 
implementation cost by $5,000. Client approval needed for 
revised pricing before proceeding."
```

**NEED_CORRECTION:**
```
"Structure needs adjustments: 1) Brazilian entity should be 
in Rio de Janeiro, not São Paulo per client requirements. 
2) Cayman fund needs different share class structure. 
3) Add nominee director for Delaware corp. Please revise."
```

**REJECTED:**
```
"Structure cannot achieve client's tax objectives due to recent 
regulatory changes in Brazil. Recommend alternative approach 
using Uruguayan holding instead of direct Brazilian subsidiary. 
New structure request needed."
```

---

## 🔄 **FLUXO COMPLETO SALES**

### **Fluxo Típico de Requisição:**

**Etapa 1 - Preparação (Sales):**
1. **Reunião** com cliente
2. **Identificação** de necessidades
3. **Criação** de Party (se necessário)
4. **Criação** de Partner
5. **Configuração** de Contacts

**Etapa 2 - Requisição (Sales):**
1. **Criação** de Structure Request
2. **Descrição** detalhada dos requisitos
3. **Definição** de point of contact
4. **Adição** de requesting parties
5. **Submissão** para Corporate

**Etapa 3 - Desenvolvimento (Corporate):**
1. **Análise** da requisição (IN_REVIEW)
2. **Desenvolvimento** da estrutura (IN_PROGRESS)
3. **Criação** de entities e ownerships
4. **Validação** de compliance
5. **Finalização** (COMPLETED)

**Etapa 4 - Aprovação (Sales):**
1. **Revisão** da structure criada
2. **Validação** contra requisitos
3. **Processamento** de approval
4. **Feedback** para Corporate (se necessário)

**Etapa 5 - Implementação:**
1. **Aprovação** final do cliente
2. **Início** da implementação
3. **Acompanhamento** do progresso
4. **Entrega** final

### **Timeline Típica:**
- **Requisição**: 1 dia
- **Análise**: 2-3 dias
- **Desenvolvimento**: 5-10 dias
- **Aprovação**: 1-2 dias
- **Implementação**: 30-60 dias

---

## 📊 **RELATÓRIOS E MÉTRICAS**

### **Métricas de Sales:**

**Volume:**
- **Requisições por mês**
- **Partners ativos**
- **Structures aprovadas**

**Performance:**
- **Tempo médio de aprovação**
- **Taxa de aprovação**
- **Satisfação do cliente**

**Pipeline:**
- **Requisições pendentes**
- **Structures em desenvolvimento**
- **Aprovações aguardando**

### **Relatórios Disponíveis:**

**Partner Report:**
- Lista de partners ativos
- Histórico de requisições
- Performance comercial

**Request Report:**
- Status de todas as requisições
- Timeline de desenvolvimento
- Gargalos identificados

**Approval Report:**
- Histórico de aprovações
- Motivos de rejeição
- Tempo de resposta

---

## 🔍 **BUSCA E FILTROS**

### **Filtros por Módulo:**

**Partners:**
- Por Status (Active, Inactive, Prospect)
- Por Priority Level
- Por Partnership Type
- Por Created date

**Contacts:**
- Por Partner
- Por Is Primary
- Por Is Active
- Por Preferred Contact Method

**Structure Requests:**
- Por Status
- Por Submitted date
- Por Point of Contact Party
- Por Requesting Parties

**Structure Approvals:**
- Por Action
- Por Approved By
- Por Approved date
- Por Structure

### **Busca Textual:**
- **Partners**: Por company_name, party__name
- **Contacts**: Por name, email, position
- **Structure Requests**: Por description
- **Structure Approvals**: Por comments

---

## 📱 **INTEGRAÇÃO COM DASHBOARD**

### **Visualização no Dashboard:**

**Pending Requests:**
- Mostra Structure Requests com status SUBMITTED
- Ação rápida "Start Review"
- Link direto para edição

**Pending Approvals:**
- Mostra Structures com status SENT_FOR_APPROVAL
- Ação rápida "Approve"
- Link para criar Structure Approval

**Recent Activity:**
- Timeline de requisições criadas
- Aprovações processadas
- Mudanças de status

---

## 🚨 **ALERTAS E NOTIFICAÇÕES**

### **Alertas Automáticos:**

**Para Sales:**
- **Nova structure** pronta para aprovação
- **Requisição** precisa de esclarecimentos
- **Approval** processada com sucesso

**Para Corporate:**
- **Nova requisição** submetida
- **Approval** com need_correction
- **Requisição** atualizada

### **Notificações por Email:**
- **Configuráveis** por usuário
- **Templates** personalizáveis
- **Histórico** de envios

---

## 🔧 **SOLUÇÃO DE PROBLEMAS**

### **Problema: "Não consigo criar Structure Request"**
**Soluções:**
1. Verifique se Point of Contact Party existe
2. Confirme que Requesting Parties estão selecionadas
3. Verifique permissões de usuário

### **Problema: "Partner não aparece na lista"**
**Soluções:**
1. Verifique se Status = Active
2. Confirme que Party está vinculada
3. Limpe filtros aplicados

### **Problema: "Approval não salva"**
**Soluções:**
1. Verifique se Structure está selecionada
2. Confirme que Action está definida
3. Adicione Comments obrigatórios

### **Problema: "Contact não recebe notificações"**
**Soluções:**
1. Verifique email cadastrado
2. Confirme Is Active = True
3. Verifique configurações de notificação

---

## 📞 **SUPORTE E TREINAMENTO**

### **Recursos Disponíveis:**
- **Manual completo** (este documento)
- **Vídeos tutoriais**
- **Sessões de treinamento**
- **Suporte técnico**

### **Contatos:**
- **Suporte Sales**: Via Django Admin
- **Treinamento**: Sessões agendadas
- **Feedback**: Melhorias contínuas

---

## 🏆 **MELHORES PRÁTICAS**

### **Para Partners:**
1. **Mantenha** informações atualizadas
2. **Configure** contacts principais
3. **Documente** preferências de comunicação
4. **Monitore** status regularmente

### **Para Structure Requests:**
1. **Seja específico** na description
2. **Inclua** todos os requisitos
3. **Defina** timeline realista
4. **Mantenha** comunicação ativa

### **Para Approvals:**
1. **Revise** cuidadosamente antes de aprovar
2. **Seja específico** nos comments
3. **Processe** rapidamente
4. **Comunique** decisões claramente

---

## 🎯 **RESUMO EXECUTIVO**

O App Sales é essencial para:

1. **Gerenciar** relacionamento comercial
2. **Processar** requisições de estruturas
3. **Aprovar** structures desenvolvidas
4. **Manter** comunicação eficiente
5. **Monitorar** performance comercial

**Resultado:** Fluxo comercial eficiente e controlado, com alta satisfação do cliente e processos otimizados.

**🎉 Use este manual para dominar o módulo Sales do SIRIUS!**

