# FLUXO DE REQUISIÇÃO DE ESTRUTURAS - SIRIUS SYSTEM

**Data:** 9 de Janeiro de 2025  
**Objetivo:** Explicar como funciona o fluxo de requisição de estruturas entre Sales e Corporate

---

## 🔄 **FLUXO COMPLETO DE REQUISIÇÃO**

### **ETAPA 1: REQUISIÇÃO NO APP SALES** 📝

#### **Onde acontece:**
- **App:** Sales
- **Modelo:** `StructureRequest`
- **Interface:** Django Admin → Sales → Structure Requests

#### **Quem faz:**
- Time de Sales
- Partners (clientes)
- Contacts dos Partners

#### **Informações da Requisição:**
```python
class StructureRequest:
    description = TextField()                    # Descrição detalhada da estrutura
    requesting_parties = ManyToMany(Party)      # Parties envolvidas (obrigatório)
    
    # Point of Contact (um dos três):
    point_of_contact_party = ForeignKey(Party)
    point_of_contact_partner = ForeignKey(Partner)  
    point_of_contact_contact = ForeignKey(Contact)
    
    status = CharField()                         # SUBMITTED, IN_REVIEW, IN_PROGRESS, COMPLETED, REJECTED
    submitted_at = DateTimeField()
```

#### **Status da Requisição:**
- 🟡 **SUBMITTED** - Requisição enviada
- 🔵 **IN_REVIEW** - Em análise pelo Corporate
- 🟠 **IN_PROGRESS** - Corporate montando a estrutura
- 🟢 **COMPLETED** - Estrutura finalizada
- 🔴 **REJECTED** - Requisição rejeitada

---

### **ETAPA 2: VISUALIZAÇÃO NO APP CORPORATE** 👀

#### **Onde o Corporate vê as requisições:**

**🎯 LOCALIZAÇÃO PRINCIPAL:**
```
Django Admin → Sales → Structure Requests
```

**📊 Interface de Visualização:**
- Lista todas as requisições por status
- Filtros por status e data
- Busca por descrição
- Detalhes completos de cada requisição

**🔍 Informações Visíveis para Corporate:**
- Descrição detalhada do que é solicitado
- Parties envolvidas na estrutura
- Point of Contact para esclarecimentos
- Status atual da requisição
- Data de submissão

---

### **ETAPA 3: MONTAGEM DA ESTRUTURA NO CORPORATE** 🏗️

#### **Processo de Trabalho:**

1. **Análise da Requisição:**
   - Corporate acessa `Sales → Structure Requests`
   - Analisa a descrição e requirements
   - Muda status para `IN_REVIEW`

2. **Montagem da Structure:**
   - Corporate vai para `Corporate → Structures`
   - Cria nova Structure baseada na requisição
   - Adiciona EntityOwnerships conforme solicitado
   - Status da Structure: `DRAFTING`

3. **Desenvolvimento:**
   - Monta hierarquia de ownership
   - Define Corporate Names e Hash Numbers
   - Configura shares e percentuais
   - Valida combinações de entities
   - Status da requisição: `IN_PROGRESS`

4. **Finalização:**
   - Structure status: `SENT_FOR_APPROVAL`
   - Requisição status: `COMPLETED`

---

### **ETAPA 4: APROVAÇÃO DA ESTRUTURA** ✅

#### **Onde acontece:**
- **App:** Sales
- **Modelo:** `StructureApproval`
- **Interface:** Django Admin → Sales → Structure Approvals

#### **Processo de Aprovação:**
```python
class StructureApproval:
    structure = OneToOne(Structure)              # Estrutura a ser aprovada
    action = CharField()                         # APPROVED, APPROVED_WITH_PRICE_CHANGE, etc.
    
    # Campos específicos por ação:
    approver = ForeignKey(Party)                 # Quem aprovou
    final_price = DecimalField()                 # Preço final (se mudou)
    correction_comment = TextField()             # Comentários para correção
    rejector = ForeignKey(Party)                 # Quem rejeitou
    rejection_reason = TextField()               # Motivo da rejeição
```

#### **Opções de Aprovação:**
- ✅ **APPROVED** - Aprovado sem alterações
- 💰 **APPROVED_WITH_PRICE_CHANGE** - Aprovado com mudança de preço
- ⚠️ **NEED_CORRECTION** - Precisa de correções
- ❌ **REJECTED** - Rejeitado

---

## 🗺️ **MAPA DO FLUXO VISUAL**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   APP SALES     │    │  APP CORPORATE  │    │   APP SALES     │
│                 │    │                 │    │                 │
│ 1. Partner faz  │───▶│ 2. Corporate vê │───▶│ 4. Aprovação    │
│    requisição   │    │    requisições  │    │    final        │
│                 │    │                 │    │                 │
│ StructureRequest│    │ 3. Monta        │    │ StructureApproval│
│                 │    │    Structure    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 📍 **ONDE CADA EQUIPE TRABALHA**

### **👥 EQUIPE DE SALES:**

**Acessa:**
- `Sales → Structure Requests` (criar e acompanhar)
- `Sales → Structure Approvals` (aprovar estruturas finalizadas)
- `Sales → Partners` (gerenciar clientes)
- `Sales → Contacts` (gerenciar contatos)

**Responsabilidades:**
- Receber solicitações de clientes
- Criar StructureRequests detalhadas
- Acompanhar progresso das requisições
- Fazer aprovação final das estruturas

### **🏢 EQUIPE DE CORPORATE:**

**Acessa:**
- `Sales → Structure Requests` (ver requisições pendentes)
- `Corporate → Structures` (montar estruturas)
- `Corporate → Entities` (gerenciar entidades)
- `Corporate → Entity Ownerships` (configurar ownership)

**Responsabilidades:**
- Analisar requisições do Sales
- Montar estruturas corporativas complexas
- Configurar ownership hierárquico
- Validar compliance e tax impacts

---

## 🔧 **EXEMPLO PRÁTICO DE USO**

### **Cenário: Cliente quer Holding Internacional**

**1. Sales recebe solicitação:**
```
Cliente: "Preciso de uma holding em Delaware para controlar 
         subsidiárias no Brasil e Cayman Islands"
```

**2. Sales cria StructureRequest:**
- **Descrição:** "Holding structure with Delaware parent controlling BR and Cayman subsidiaries"
- **Parties:** John Smith (UBO), Maria Silva (UBO)
- **Point of Contact:** John Smith
- **Status:** SUBMITTED

**3. Corporate vê a requisição:**
- Acessa `Sales → Structure Requests`
- Vê requisição pendente
- Muda status para IN_REVIEW

**4. Corporate monta Structure:**
- Cria "International Holding Structure"
- Adiciona EntityOwnerships:
  - John Smith 60% → Delaware Holding Corp
  - Maria Silva 40% → Delaware Holding Corp
  - Delaware Holding Corp 100% → Brazil Subsidiary
  - Delaware Holding Corp 100% → Cayman Investment Fund

**5. Sales aprova:**
- Structure aparece em `Sales → Structure Approvals`
- Sales seleciona APPROVED
- Define approver e finaliza

---

## 🎯 **PONTOS IMPORTANTES**

### **✅ O que está funcionando:**
- Fluxo completo implementado
- Integração entre Sales e Corporate
- Rastreamento de status
- Aprovação estruturada

### **⚠️ Melhorias possíveis:**
- Dashboard unificado para acompanhamento
- Notificações automáticas entre equipes
- Templates de requisições comuns
- Relatórios de performance

### **🔗 Integração atual:**
- Sales cria requisições
- Corporate vê e executa
- Sales aprova resultado final
- Tudo rastreado no Django Admin

---

## 📋 **RESUMO EXECUTIVO**

**Pergunta:** "Onde aparece a requisição para que ela seja montada em Corporate?"

**Resposta:** As requisições aparecem em **`Django Admin → Sales → Structure Requests`**, onde o time de Corporate pode:

1. ✅ Ver todas as requisições pendentes
2. 📋 Analisar detalhes e requirements  
3. 👥 Identificar parties envolvidas
4. 📞 Contactar point of contact
5. 🔄 Atualizar status conforme progresso
6. 🏗️ Montar a Structure correspondente

**O fluxo está 100% implementado e funcional!** 🚀

