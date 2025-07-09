# MANUAL DO DASHBOARD SIRIUS

**Data:** 9 de Janeiro de 2025  
**Objetivo:** Manual completo de uso do Dashboard integrado ao Django Admin

---

## 🎯 **VISÃO GERAL DO DASHBOARD**

O Dashboard SIRIUS é uma interface centralizada que oferece visão completa e gestão eficiente de todo o fluxo de requisições de estruturas corporativas entre as equipes de Sales e Corporate.

### **Características Principais:**
- **Interface integrada** ao Django Admin
- **Estatísticas em tempo real**
- **Gestão completa de workflow**
- **Design responsivo** para todos os dispositivos
- **Ações rápidas** para eficiência operacional

---

## 🚀 **ACESSO AO DASHBOARD**

### **Como Acessar:**

**Método 1 - URL Direta:**
```
https://seu-dominio.com/admin/dashboard/
```

**Método 2 - Navegação:**
1. Acesse o Django Admin: `/admin/`
2. Clique em **"Dashboard"** no header superior
3. Ou clique no logo **"SIRIUS Administration"**

**Método 3 - Redirecionamento Automático:**
- Acesse a raiz do site (`/`)
- Será redirecionado automaticamente para o dashboard

### **Requisitos de Acesso:**
- ✅ **Login obrigatório** (usuário Django)
- ✅ **Permissão staff** (staff_member_required)
- ✅ **Navegador moderno** (Chrome, Firefox, Safari, Edge)

---

## 📊 **COMPONENTES DO DASHBOARD**

### **1. ESTATÍSTICAS RÁPIDAS (Quick Stats)**

**Localização:** Topo da página, cards coloridos

**Métricas Exibidas:**
```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│     15      │ │      8      │ │      3      │ │     42      │
│  Pending    │ │ In Progress │ │  Approval   │ │ Completed   │
│  Requests   │ │             │ │             │ │   (30d)     │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

**Significado dos Cards:**
- 🟡 **Pending Requests**: Requisições aguardando análise
- 🟠 **In Progress**: Estruturas sendo desenvolvidas
- 🔵 **Approval**: Estruturas aguardando aprovação
- 🟢 **Completed (30d)**: Requisições finalizadas nos últimos 30 dias

### **2. MÉTRICAS DE PERFORMANCE**

**Localização:** Seção abaixo das estatísticas rápidas

**KPIs Principais:**
- **Completion Rate**: Taxa de conclusão (%)
- **Avg. Processing Time**: Tempo médio de processamento (dias)
- **Approval Rate**: Taxa de aprovação (%)

**Como Interpretar:**
- **Completion Rate > 80%**: Excelente performance
- **Processing Time < 10 dias**: Tempo adequado
- **Approval Rate > 90%**: Alta qualidade das estruturas

### **3. REQUISIÇÕES PENDENTES**

**Localização:** Lado esquerdo, seção principal

**Informações Exibidas:**
- **ID da requisição** (#001, #002, etc.)
- **Status atual** (badge colorido)
- **Descrição** (truncada em 60 caracteres)
- **Número de parties** envolvidas
- **Data de submissão**
- **Point of contact**

**Ações Disponíveis:**
- 🎬 **Start Review**: Iniciar análise
- 👁️ **View**: Ver detalhes completos

### **4. ESTRUTURAS EM DESENVOLVIMENTO**

**Localização:** Centro, seção principal

**Informações Exibidas:**
- **Nome da estrutura**
- **Status** (Drafting)
- **Descrição** (truncada em 80 caracteres)
- **Número de entities**
- **Data de criação**

**Ações Disponíveis:**
- ✈️ **Send for Approval**: Enviar para aprovação
- ✏️ **Edit**: Editar estrutura

### **5. APROVAÇÕES PENDENTES**

**Localização:** Lado direito, seção principal

**Informações Exibidas:**
- **Nome da estrutura**
- **Status** (Sent for Approval)
- **Descrição**
- **Número de entities**
- **Data de envio**

**Ações Disponíveis:**
- ✅ **Approve**: Aprovar estrutura
- 👁️ **Review**: Revisar detalhes

### **6. ATIVIDADE RECENTE**

**Localização:** Seção inferior, largura completa

**Timeline de Atividades:**
- **Requisições submetidas**
- **Estruturas criadas**
- **Aprovações processadas**
- **Mudanças de status**

**Formato da Timeline:**
```
🔵 [Ícone] Título da Atividade
   Descrição detalhada
   ⏰ 2 horas atrás
```

---

## ⚡ **AÇÕES RÁPIDAS**

### **Para Requisições Pendentes:**

**Start Review:**
1. Clique no botão **"Start Review"**
2. Status muda para "IN_REVIEW"
3. Requisição aparece na lista de trabalho do Corporate

**View Details:**
1. Clique no botão **"View"**
2. Abre página de detalhes da requisição
3. Permite edição completa

### **Para Estruturas em Desenvolvimento:**

**Send for Approval:**
1. Clique no botão **"Send for Approval"**
2. Status muda para "SENT_FOR_APPROVAL"
3. Estrutura aparece na lista de aprovações

**Edit Structure:**
1. Clique no botão **"Edit"**
2. Abre página de edição da estrutura
3. Permite modificar entities e ownerships

### **Para Aprovações Pendentes:**

**Approve Structure:**
1. Clique no botão **"Approve"**
2. Abre formulário de aprovação
3. Permite definir ação e comentários

**Review Structure:**
1. Clique no botão **"Review"**
2. Abre página de detalhes da estrutura
3. Permite análise completa antes da aprovação

---

## 🔄 **FUNCIONALIDADES AUTOMÁTICAS**

### **Auto-Refresh:**
- **Estatísticas**: Atualizam a cada 2 minutos
- **Atividade recente**: Atualiza a cada 5 minutos
- **Página completa**: Recarrega a cada 5 minutos

### **Refresh Manual:**
- **Botão flutuante** no canto superior direito
- **Atalho de teclado**: Ctrl+R (ou Cmd+R no Mac)
- **Atualização instantânea** de todos os dados

### **Estados de Loading:**
- **Botões ficam desabilitados** durante processamento
- **Ícone de spinner** indica carregamento
- **Feedback visual** para todas as ações

---

## 📱 **RESPONSIVIDADE**

### **Desktop (> 1024px):**
- **Layout em grid** completo
- **3 colunas** para seções principais
- **Sidebar** com estatísticas
- **Todas as funcionalidades** visíveis

### **Tablet (768px - 1024px):**
- **Layout em 2 colunas**
- **Seções empilhadas**
- **Navegação adaptada**
- **Touch-friendly**

### **Mobile (< 768px):**
- **Layout em coluna única**
- **Cards empilhados**
- **Menu colapsável**
- **Botões maiores** para touch

---

## 🎨 **SISTEMA DE CORES**

### **Status Colors:**
- 🟡 **#FFC107** - Pending (Amarelo)
- 🔵 **#007BFF** - In Review (Azul)
- 🟠 **#FF8C00** - In Progress (Laranja)
- 🟢 **#28A745** - Completed/Approved (Verde)
- 🔴 **#DC3545** - Rejected (Vermelho)

### **Significado Visual:**
- **Amarelo**: Aguardando ação
- **Azul**: Em análise
- **Laranja**: Em desenvolvimento
- **Verde**: Finalizado com sucesso
- **Vermelho**: Rejeitado ou com problema

---

## 🔧 **SOLUÇÃO DE PROBLEMAS**

### **Dashboard não carrega:**
1. Verifique se está logado no Django Admin
2. Confirme permissões de staff
3. Limpe cache do navegador
4. Tente acessar `/admin/dashboard/` diretamente

### **Estatísticas não atualizam:**
1. Clique no botão de refresh manual
2. Verifique conexão com internet
3. Aguarde o próximo auto-refresh (2-5 min)

### **Ações não funcionam:**
1. Verifique se tem permissões adequadas
2. Aguarde o processamento (botão fica desabilitado)
3. Recarregue a página se necessário

### **Layout quebrado em mobile:**
1. Atualize o navegador
2. Limpe cache
3. Verifique se JavaScript está habilitado

---

## 📋 **FLUXO DE TRABALHO TÍPICO**

### **Para Equipe de Sales:**

**Manhã (9h):**
1. Acesse o dashboard
2. Verifique **Pending Requests**
3. Revise **Pending Approvals**
4. Processe aprovações pendentes

**Durante o dia:**
1. Monitore **Recent Activity**
2. Acompanhe **Performance Metrics**
3. Responda a notificações

**Final do dia (18h):**
1. Revise **Completed** do dia
2. Verifique pendências para amanhã

### **Para Equipe de Corporate:**

**Manhã (9h):**
1. Acesse o dashboard
2. Verifique **Pending Requests**
3. Inicie análise com **Start Review**
4. Priorize por data de submissão

**Durante o dia:**
1. Trabalhe em **Structures in Progress**
2. Envie estruturas prontas para aprovação
3. Monitore métricas de performance

**Final do dia (18h):**
1. Atualize status das estruturas
2. Envie estruturas finalizadas

---

## 📊 **RELATÓRIOS E MÉTRICAS**

### **Métricas Diárias:**
- **Requisições processadas**
- **Estruturas criadas**
- **Aprovações realizadas**
- **Tempo médio de processamento**

### **Métricas Semanais:**
- **Taxa de conclusão**
- **Gargalos identificados**
- **Performance por usuário**
- **Tendências de volume**

### **Métricas Mensais:**
- **Crescimento de demanda**
- **Eficiência operacional**
- **Satisfação do cliente**
- **ROI do processo**

---

## 🎯 **DICAS DE PRODUTIVIDADE**

### **Atalhos de Teclado:**
- **Ctrl+R**: Refresh manual
- **Ctrl+D**: Focar no dashboard
- **Esc**: Fechar modais

### **Navegação Eficiente:**
- Use **links diretos** nos cards
- Aproveite **ações rápidas**
- Monitore **Recent Activity**
- Configure **auto-refresh**

### **Gestão de Tempo:**
- Priorize por **data de submissão**
- Use **filtros de status**
- Acompanhe **métricas de tempo**
- Defina **metas diárias**

---

## 🔗 **INTEGRAÇÃO COM OUTROS MÓDULOS**

### **Links Diretos:**
- **Sales → Structure Requests**: Gestão completa
- **Corporate → Structures**: Desenvolvimento
- **Sales → Structure Approvals**: Aprovações
- **Parties**: Gestão de UBOs
- **Financial Department**: Preços e custos

### **Navegação Contextual:**
- **Breadcrumbs** em todas as páginas
- **Botões de retorno** ao dashboard
- **Links relacionados** em cada objeto

---

## 📞 **SUPORTE E AJUDA**

### **Documentação:**
- **Manual completo** (este documento)
- **API Reference**: Documentação técnica
- **Development Guide**: Para desenvolvedores

### **Contato:**
- **Suporte técnico**: Via Django Admin
- **Treinamento**: Sessões disponíveis
- **Feedback**: Melhorias contínuas

---

## 🏆 **RESUMO EXECUTIVO**

O Dashboard SIRIUS é uma ferramenta poderosa que:

1. **Centraliza** toda a gestão do fluxo de requisições
2. **Simplifica** o trabalho das equipes Sales e Corporate
3. **Melhora** a visibilidade e controle do processo
4. **Oferece** métricas em tempo real para tomada de decisão
5. **Escala** com o crescimento do negócio

**Resultado:** Interface profissional, eficiente e totalmente integrada que transforma a gestão de estruturas corporativas em um processo fluido e controlado.

**🎉 Use o dashboard diariamente para maximizar a eficiência operacional!**

