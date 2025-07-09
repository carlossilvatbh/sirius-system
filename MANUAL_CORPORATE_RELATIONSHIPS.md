# MANUAL DO APP CORPORATE RELATIONSHIPS

**Data:** 9 de Janeiro de 2025  
**Objetivo:** Manual completo de uso do módulo Corporate Relationships para gestão de arquivos e relacionamentos

---

## 🎯 **VISÃO GERAL DO APP CORPORATE RELATIONSHIPS**

O App Corporate Relationships é responsável pela gestão de arquivos de estruturas aprovadas e documentação de relacionamentos corporativos, servindo como repositório central de estruturas finalizadas.

### **Funcionalidades Principais:**
- **File Management** (arquivos de estruturas aprovadas)
- **Relationship Documentation** (documentação de relacionamentos)
- **Approval Tracking** (rastreamento de aprovações)
- **Archive Management** (gestão de arquivos)

---

## 📁 **FILE MANAGEMENT (Gestão de Arquivos)**

### **O que são Files:**
Files representam arquivos de estruturas corporativas que foram aprovadas e finalizadas, servindo como registro permanente das estruturas implementadas.

### **Acesso:**
```
Django Admin → Corporate Relationship → Files
```

### **Campos do File:**

**Informações Básicas:**
- **Name**: Nome do arquivo/estrutura
- **Description**: Descrição detalhada
- **File Type**: Tipo de arquivo

**Relacionamentos:**
- **Related Structure**: Structure relacionada (se aplicável)
- **Related Parties**: Parties envolvidas

**Arquivo:**
- **File URL**: URL do arquivo
- **File Size**: Tamanho do arquivo
- **File Format**: Formato (PDF, DOC, etc.)

**Aprovação:**
- **Approved By**: Usuário que aprovou
- **Approval Date**: Data de aprovação
- **Approval Comments**: Comentários da aprovação

**Status:**
- **Status**: DRAFT, APPROVED, ARCHIVED
- **Is Active**: Ativo/inativo

**Metadados:**
- **Created Date**: Data de criação
- **Updated Date**: Última atualização
- **Version**: Versão do arquivo

### **Tipos de Arquivo (File Types):**

**STRUCTURE_DIAGRAM:**
- Diagrama da estrutura corporativa
- Organograma visual
- Fluxograma de ownership

**LEGAL_DOCUMENTATION:**
- Documentação legal completa
- Contratos e acordos
- Atos constitutivos

**COMPLIANCE_REPORT:**
- Relatórios de compliance
- Análises regulatórias
- Due diligence reports

**TAX_ANALYSIS:**
- Análises fiscais
- Estruturas de otimização
- Impactos tributários

**IMPLEMENTATION_GUIDE:**
- Guias de implementação
- Cronogramas de execução
- Checklists

**BOARD_RESOLUTION:**
- Resoluções de diretoria
- Atas de reunião
- Decisões corporativas

**FINANCIAL_STATEMENTS:**
- Demonstrações financeiras
- Balanços patrimoniais
- Relatórios financeiros

**OTHER:**
- Outros tipos de arquivo
- Documentos específicos
- Arquivos customizados

### **Status do File:**

**DRAFT** 📝
- Arquivo em elaboração
- Ainda não aprovado
- Sujeito a alterações

**APPROVED** ✅
- Arquivo aprovado
- Pronto para uso
- Versão final

**ARCHIVED** 📦
- Arquivo arquivado
- Versão antiga
- Mantido para histórico

### **Como Criar um File:**

**Passo 1 - Informações Básicas:**
1. Acesse `Corporate Relationship → Files`
2. Clique em **"Add File"**
3. Preencha **Name** descritivo
4. Adicione **Description** detalhada
5. Selecione **File Type**

**Passo 2 - Relacionamentos:**
1. Vincule **Related Structure** (se aplicável)
2. Adicione **Related Parties** envolvidas

**Passo 3 - Arquivo:**
1. Adicione **File URL**
2. Especifique **File Size** e **File Format**

**Passo 4 - Aprovação:**
1. **Approved By** será preenchido automaticamente
2. **Approval Date** será definida no salvamento
3. Adicione **Approval Comments**

**Passo 5 - Status:**
1. Defina **Status** (geralmente "APPROVED")
2. Marque **Is Active** = True
3. **Version** será incrementada automaticamente

### **Exemplo de File:**
```
Name: "International Holding Structure - Final Implementation"
Description: "Complete implementation package for John Smith's international holding structure including Delaware corporation, Brazilian subsidiary, and Cayman fund"
File Type: IMPLEMENTATION_GUIDE
Related Structure: International Holding Structure
Related Parties: [John Smith, Maria Silva]
File URL: "https://docs.sirius.com/structures/intl_holding_final.pdf"
File Size: 15.2 MB
File Format: PDF
Approved By: admin
Approval Date: 2025-01-09
Approval Comments: "Structure approved and ready for implementation. All compliance requirements met."
Status: APPROVED
Is Active: True
Version: 1.0
```

---

## 🔗 **RELATIONSHIP DOCUMENTATION**

### **Documentação de Relacionamentos:**
O sistema documenta automaticamente os relacionamentos entre Files, Structures, e Parties, criando um mapa completo de conexões.

### **Tipos de Relacionamentos:**

**File ↔ Structure:**
- Files vinculados a Structures específicas
- Histórico de documentação por estrutura
- Versões e atualizações

**File ↔ Parties:**
- Files relacionados a Parties específicas
- Documentação por cliente
- Histórico de relacionamentos

**Structure ↔ Parties:**
- Parties envolvidas em cada Structure
- Roles e responsabilidades
- Ownership relationships

### **Visualização de Relacionamentos:**

**Por Structure:**
```
International Holding Structure
├── Files:
│   ├── Structure Diagram (v1.2)
│   ├── Legal Documentation (v1.0)
│   └── Implementation Guide (v1.0)
├── Parties:
│   ├── John Smith (60% owner)
│   └── Maria Silva (40% owner)
└── Entities:
    ├── Delaware Holding Corp
    ├── Brazil Subsidiary Ltda
    └── Cayman Investment Fund
```

**Por Party:**
```
John Smith
├── Structures:
│   ├── International Holding Structure (60%)
│   └── Family Trust Structure (Settlor)
├── Files:
│   ├── KYC Documentation
│   ├── Tax Returns 2024
│   └── Passport Copy
└── Roles:
    ├── Director (Delaware Holding Corp)
    └── Authorized Signatory (Bank Accounts)
```

---

## 📋 **APPROVAL TRACKING**

### **Rastreamento de Aprovações:**
O sistema mantém histórico completo de todas as aprovações, incluindo quem aprovou, quando e por quê.

### **Campos de Tracking:**

**Aprovação Inicial:**
- **Approved By**: Usuário que aprovou
- **Approval Date**: Data da aprovação
- **Approval Comments**: Comentários

**Histórico de Versões:**
- **Version History**: Histórico de versões
- **Change Log**: Log de mudanças
- **Previous Versions**: Versões anteriores

**Workflow de Aprovação:**
- **Approval Workflow**: Fluxo de aprovação
- **Required Approvers**: Aprovadores necessários
- **Approval Status**: Status da aprovação

### **Processo de Aprovação:**

**Etapa 1 - Submissão:**
1. File criado com status DRAFT
2. Documentação anexada
3. Relacionamentos definidos

**Etapa 2 - Revisão:**
1. Revisão técnica
2. Validação de compliance
3. Verificação de completude

**Etapa 3 - Aprovação:**
1. Aprovação formal
2. Status mudado para APPROVED
3. Comentários de aprovação

**Etapa 4 - Arquivo:**
1. File disponível para uso
2. Notificações enviadas
3. Histórico registrado

---

## 📦 **ARCHIVE MANAGEMENT**

### **Gestão de Arquivos:**
Sistema de arquivamento para manter histórico de versões antigas e estruturas descontinuadas.

### **Processo de Arquivamento:**

**Arquivamento Automático:**
- Versões antigas automaticamente arquivadas
- Files inativos movidos para arquivo
- Limpeza periódica de drafts antigos

**Arquivamento Manual:**
- Estruturas descontinuadas
- Files obsoletos
- Documentação histórica

### **Retenção de Dados:**
- **Files ativos**: Mantidos indefinidamente
- **Files arquivados**: Mantidos por 7 anos
- **Drafts antigos**: Removidos após 1 ano
- **Logs de acesso**: Mantidos por 2 anos

---

## 🔍 **BUSCA E FILTROS**

### **Filtros Disponíveis:**

**Files:**
- Por File Type
- Por Status
- Por Approved By
- Por Approval Date
- Por Related Structure
- Por Related Parties

**Relacionamentos:**
- Por Structure
- Por Party
- Por Date Range
- Por File Type

### **Busca Textual:**
- **Files**: Por name, description, approval_comments
- **Relacionamentos**: Por structure name, party name

### **Busca Avançada:**
- **Combinação de filtros**
- **Busca por período**
- **Busca por aprovador**
- **Busca por tipo de relacionamento**

---

## 📊 **RELATÓRIOS**

### **Relatório de Files:**
- Lista completa de files por período
- Status de aprovação
- Distribuição por tipo
- Histórico de versões

### **Relatório de Relacionamentos:**
- Mapa de relacionamentos por Structure
- Files por Party
- Análise de conectividade
- Estruturas mais complexas

### **Relatório de Aprovações:**
- Histórico de aprovações por usuário
- Tempo médio de aprovação
- Files pendentes de aprovação
- Performance do processo

### **Relatório de Arquivos:**
- Files arquivados por período
- Espaço utilizado
- Files para limpeza
- Estatísticas de retenção

---

## 🔐 **CONTROLE DE ACESSO**

### **Níveis de Acesso:**

**READ_ONLY:**
- Visualização de files
- Acesso a relacionamentos
- Consulta de histórico

**EDITOR:**
- Criação de files
- Edição de drafts
- Definição de relacionamentos

**APPROVER:**
- Aprovação de files
- Mudança de status
- Comentários de aprovação

**ADMIN:**
- Acesso completo
- Gestão de arquivos
- Configuração do sistema

### **Controle por File Type:**
- **LEGAL_DOCUMENTATION**: Apenas advogados
- **TAX_ANALYSIS**: Apenas contadores
- **COMPLIANCE_REPORT**: Compliance officers
- **FINANCIAL_STATEMENTS**: Equipe financeira

---

## 🚨 **ALERTAS E NOTIFICAÇÕES**

### **Alertas Automáticos:**
- **File pendente** de aprovação > 5 dias
- **Draft antigo** > 30 dias sem atualização
- **File expirado** (se aplicável)
- **Relacionamento quebrado** (structure/party removida)

### **Notificações:**
- **Email**: Para aprovadores
- **Dashboard**: Alertas visuais
- **Relatórios**: Seção de pendências

---

## 🔧 **SOLUÇÃO DE PROBLEMAS**

### **Problema: "File URL não abre"**
**Soluções:**
1. Verifique se URL está correta
2. Confirme permissões de acesso
3. Teste URL em navegador
4. Verifique se arquivo ainda existe

### **Problema: "Relacionamento não aparece"**
**Soluções:**
1. Verifique se Structure/Party ainda existe
2. Confirme se relacionamento está ativo
3. Limpe cache do navegador
4. Recarregue a página

### **Problema: "Não consigo aprovar File"**
**Soluções:**
1. Verifique permissões de usuário
2. Confirme se File está em status DRAFT
3. Adicione comentários obrigatórios
4. Verifique workflow de aprovação

---

## 🏆 **MELHORES PRÁTICAS**

### **Gestão de Files:**
1. **Use nomes** descritivos e padronizados
2. **Mantenha** descriptions detalhadas
3. **Vincule** sempre a structures/parties
4. **Aprove** rapidamente para evitar atrasos

### **Documentação:**
1. **Documente** todas as decisões importantes
2. **Mantenha** histórico de versões
3. **Use** comentários de aprovação detalhados
4. **Organize** files por tipo e data

### **Relacionamentos:**
1. **Vincule** files a structures sempre que possível
2. **Mantenha** relacionamentos atualizados
3. **Documente** mudanças de relacionamento
4. **Monitore** relacionamentos quebrados

### **Arquivamento:**
1. **Archive** files obsoletos regularmente
2. **Mantenha** apenas versões necessárias
3. **Documente** motivos de arquivamento
4. **Revise** políticas de retenção

---

## 📈 **MÉTRICAS E KPIs**

### **Métricas de Files:**
- **Total de files** por período
- **Files aprovados** vs. rejeitados
- **Tempo médio** de aprovação
- **Distribuição** por tipo

### **Métricas de Relacionamentos:**
- **Structures** mais documentadas
- **Parties** com mais files
- **Complexidade** de relacionamentos
- **Conectividade** do sistema

### **Métricas de Performance:**
- **Tempo de aprovação** por tipo
- **Eficiência** do processo
- **Gargalos** identificados
- **Satisfação** dos usuários

---

## 🎯 **INTEGRAÇÃO COM OUTROS MÓDULOS**

### **Integração com Corporate:**
- **Structures** automaticamente vinculadas
- **Entities** referenciadas
- **Validation rules** aplicadas

### **Integração com Sales:**
- **Structure requests** vinculadas
- **Approvals** documentadas
- **Partners** referenciados

### **Integração com Parties:**
- **Parties** automaticamente vinculadas
- **Roles** documentados
- **Documents** referenciados

---

## 🎯 **RESUMO EXECUTIVO**

O App Corporate Relationships é essencial para:

1. **Documentar** estruturas aprovadas
2. **Manter** histórico completo
3. **Gerenciar** relacionamentos
4. **Controlar** aprovações
5. **Organizar** arquivos corporativos

**Resultado:** Repositório central organizado e seguro de todas as estruturas corporativas implementadas.

**🎉 Use este manual para dominar a gestão de relacionamentos corporativos no SIRIUS!**

