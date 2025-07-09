# MANUAL DO APP PARTIES

**Data:** 9 de Janeiro de 2025  
**Objetivo:** Manual completo de uso do módulo Parties para gestão de UBOs e relacionamentos

---

## 🎯 **VISÃO GERAL DO APP PARTIES**

O App Parties é responsável pela gestão centralizada de todas as pessoas (físicas e jurídicas) que participam das estruturas corporativas, incluindo UBOs (Ultimate Beneficial Owners), seus roles, documentos e relacionamentos.

### **Funcionalidades Principais:**
- **Gestão de Parties** (pessoas físicas e jurídicas)
- **Party Roles** (múltiplos papéis e poderes)
- **Passports** (documentos de identidade)
- **Beneficiary Relations** (relacionamentos de beneficiários)
- **Document Attachments** (documentos anexos)

---

## 👤 **GESTÃO DE PARTIES**

### **O que são Parties:**
Parties representam qualquer pessoa física ou jurídica que pode participar de estruturas corporativas. Substituem o conceito antigo de "UBO" com funcionalidade expandida.

### **Acesso:**
```
Django Admin → Parties → Parties
```

### **Campos da Party:**

**Tipo de Pessoa:**
- **Person Type**: NATURAL_PERSON, JURIDICAL_PERSON

**Informações Básicas:**
- **Name**: Nome completo
- **Is Partner**: Se é parceiro comercial

**Pessoa Física (Natural Person):**
- **Birth Date**: Data de nascimento
- **Birth Place**: Local de nascimento
- **Gender**: Gênero
- **Marital Status**: Estado civil

**Nacionalidade e Residência:**
- **Nationality**: Nacionalidade
- **Country of Residence**: País de residência
- **Tax Residency**: Residência fiscal

**Informações Profissionais:**
- **Occupation**: Profissão
- **Employer**: Empregador
- **Annual Income**: Renda anual
- **Net Worth**: Patrimônio líquido

**Contato:**
- **Email**: Email principal
- **Phone**: Telefone
- **Address**: Endereço completo

**Compliance:**
- **Is PEP**: Pessoa Politicamente Exposta
- **PEP Details**: Detalhes se for PEP
- **Risk Level**: HIGH, MEDIUM, LOW
- **KYC Status**: Status do KYC
- **KYC Date**: Data do KYC

**Pessoa Jurídica (Juridical Person):**
- **Registration Number**: Número de registro
- **Registration Country**: País de registro
- **Legal Form**: Forma jurídica
- **Business Activity**: Atividade comercial

### **Tipos de Person Type:**

**NATURAL_PERSON:**
- Pessoas físicas (indivíduos)
- UBOs tradicionais
- Beneficiários finais
- Diretores e officers

**JURIDICAL_PERSON:**
- Pessoas jurídicas
- Empresas que podem ser UBOs
- Trusts e foundations
- Fundos de investimento

### **Como Criar uma Party:**

**Passo 1 - Tipo de Pessoa:**
1. Acesse `Parties → Parties`
2. Clique em **"Add Party"**
3. Selecione **Person Type**

**Passo 2 - Informações Básicas:**
1. Preencha **Name** completo
2. Marque **Is Partner** se aplicável

**Passo 3 - Para Pessoa Física:**
1. Preencha **Birth Date** e **Birth Place**
2. Selecione **Gender** e **Marital Status**
3. Configure **Nationality** e **Country of Residence**
4. Defina **Tax Residency**

**Passo 4 - Informações Profissionais:**
1. Especifique **Occupation** e **Employer**
2. Informe **Annual Income** e **Net Worth**

**Passo 5 - Contato:**
1. Adicione **Email** e **Phone**
2. Preencha **Address** completo

**Passo 6 - Compliance:**
1. Marque **Is PEP** se aplicável
2. Adicione **PEP Details** se necessário
3. Defina **Risk Level**
4. Configure **KYC Status** e **KYC Date**

**Passo 7 - Para Pessoa Jurídica:**
1. Preencha **Registration Number**
2. Defina **Registration Country**
3. Especifique **Legal Form**
4. Descreva **Business Activity**

### **Exemplo de Party (Pessoa Física):**
```
Person Type: NATURAL_PERSON
Name: John Smith
Is Partner: True
Birth Date: 1980-01-15
Birth Place: New York, USA
Gender: MALE
Marital Status: MARRIED
Nationality: US
Country of Residence: US
Tax Residency: US
Occupation: Investment Manager
Employer: Smith Capital Management
Annual Income: 500,000.00
Net Worth: 2,500,000.00
Email: john.smith@email.com
Phone: +1 (555) 123-4567
Address: 123 Park Avenue, New York, NY 10001
Is PEP: False
Risk Level: LOW
KYC Status: COMPLETED
KYC Date: 2025-01-01
```

---

## 🎭 **PARTY ROLES (Papéis e Poderes)**

### **O que são Party Roles:**
Party Roles definem os diferentes papéis e poderes que uma Party pode exercer em estruturas corporativas, permitindo múltiplos roles por pessoa.

### **Acesso:**
```
Django Admin → Parties → Party Roles
```

### **Campos do Party Role:**

**Relacionamento:**
- **Party**: Party que exerce o role

**Role Definition:**
- **Role Type**: Tipo de papel (veja lista abaixo)
- **Role Description**: Descrição específica
- **Scope**: Escopo do papel

**Poderes:**
- **Powers**: Poderes específicos
- **Limitations**: Limitações do papel

**Validade:**
- **Start Date**: Data de início
- **End Date**: Data de fim (opcional)
- **Is Active**: Ativo/inativo

### **Tipos de Role (Role Types):**

**DIRECTOR:**
- Diretor de empresa
- Poderes de gestão
- Responsabilidades fiduciárias

**OFFICER:**
- Officer corporativo (CEO, CFO, etc.)
- Poderes executivos
- Representação da empresa

**SHAREHOLDER:**
- Acionista/quotista
- Direitos de propriedade
- Direitos de voto

**BENEFICIARY:**
- Beneficiário de trust/foundation
- Direitos de benefício
- Distribuições

**SETTLOR:**
- Settlor de trust
- Poderes de constituição
- Direitos de modificação

**PROTECTOR:**
- Protector de trust
- Poderes de supervisão
- Veto sobre decisões

**NOMINEE:**
- Nominee director/shareholder
- Representação nominal
- Poderes limitados

**AUTHORIZED_SIGNATORY:**
- Signatário autorizado
- Poderes bancários
- Representação limitada

**POWER_OF_ATTORNEY:**
- Procurador
- Poderes específicos
- Representação legal

**OTHER:**
- Outros papéis específicos
- Definição customizada

### **Como Criar um Party Role:**

**Passo 1 - Selecionar Party:**
1. Acesse `Parties → Party Roles`
2. Clique em **"Add Party Role"**
3. Selecione **Party** correspondente

**Passo 2 - Definir Role:**
1. Selecione **Role Type**
2. Adicione **Role Description** específica
3. Defina **Scope** do papel

**Passo 3 - Configurar Poderes:**
1. Especifique **Powers** detalhados
2. Adicione **Limitations** se aplicável

**Passo 4 - Validade:**
1. Defina **Start Date**
2. Configure **End Date** (se temporário)
3. Marque **Is Active** = True

### **Exemplo de Party Roles para John Smith:**
```
Role 1:
- Party: John Smith
- Role Type: DIRECTOR
- Role Description: "Director of Delaware Holding Corp"
- Scope: "Delaware Holding Corp"
- Powers: "General management, strategic decisions, board resolutions"
- Limitations: "Cannot exceed $100K without board approval"
- Start Date: 2025-01-01
- Is Active: True

Role 2:
- Party: John Smith
- Role Type: AUTHORIZED_SIGNATORY
- Role Description: "Authorized signatory for bank accounts"
- Scope: "All corporate bank accounts"
- Powers: "Banking transactions, wire transfers up to $50K"
- Limitations: "Requires dual signature for amounts > $50K"
- Start Date: 2025-01-01
- Is Active: True
```

---

## 📄 **PASSPORTS (Documentos de Identidade)**

### **O que são Passports:**
Passports são documentos de identidade das Parties, com controle de validade e alertas de expiração.

### **Acesso:**
```
Django Admin → Parties → Passports
```

### **Campos do Passport:**

**Relacionamento:**
- **Party**: Party proprietária do passport

**Documento:**
- **Document Type**: PASSPORT, ID_CARD, DRIVER_LICENSE, OTHER
- **Document Number**: Número do documento
- **Issuing Country**: País emissor
- **Issuing Authority**: Autoridade emissora

**Validade:**
- **Issue Date**: Data de emissão
- **Expiry Date**: Data de expiração
- **Is Valid**: Válido/inválido

**Arquivo:**
- **Document File**: Arquivo do documento (upload)

### **Tipos de Documento:**

**PASSPORT:**
- Passaporte oficial
- Documento de viagem
- Identificação internacional

**ID_CARD:**
- Carteira de identidade
- RG, CNH, etc.
- Identificação nacional

**DRIVER_LICENSE:**
- Carteira de motorista
- Identificação com foto
- Comprovante de endereço

**OTHER:**
- Outros documentos
- Certificados específicos
- Documentos customizados

### **Validação de Expiração:**

**Alertas Automáticos:**
- **30 dias**: Alerta amarelo
- **15 dias**: Alerta laranja
- **Expirado**: Alerta vermelho

**Notificações:**
- Email para responsáveis
- Dashboard alerts
- Relatórios de compliance

### **Como Criar um Passport:**

**Passo 1 - Selecionar Party:**
1. Acesse `Parties → Passports`
2. Clique em **"Add Passport"**
3. Selecione **Party** correspondente

**Passo 2 - Informações do Documento:**
1. Selecione **Document Type**
2. Preencha **Document Number**
3. Defina **Issuing Country** e **Issuing Authority**

**Passo 3 - Validade:**
1. Configure **Issue Date**
2. Defina **Expiry Date**
3. Confirme **Is Valid** = True

**Passo 4 - Upload:**
1. Faça upload do **Document File**
2. Clique em **"Save"**

### **Exemplo de Passport:**
```
Party: John Smith
Document Type: PASSPORT
Document Number: 123456789
Issuing Country: US
Issuing Authority: U.S. Department of State
Issue Date: 2020-01-15
Expiry Date: 2030-01-15
Is Valid: True
Document File: john_smith_passport.pdf
```

---

## 👨‍👩‍👧‍👦 **BENEFICIARY RELATIONS (Relacionamentos)**

### **O que são Beneficiary Relations:**
Beneficiary Relations definem relacionamentos entre Parties, especialmente para sucessão e benefícios, com validação de 100% de distribuição.

### **Acesso:**
```
Django Admin → Parties → Beneficiary Relations
```

### **Campos da Beneficiary Relation:**

**Relacionamento:**
- **Benefactor**: Party que concede benefício
- **Beneficiary**: Party que recebe benefício

**Tipo de Relacionamento:**
- **Relationship Type**: HEIR, SPOUSE, CHILD, PARENT, SIBLING, OTHER
- **Relationship Description**: Descrição específica

**Benefício:**
- **Benefit Percentage**: Percentual do benefício
- **Benefit Type**: INHERITANCE, TRUST_DISTRIBUTION, INSURANCE, OTHER
- **Benefit Description**: Descrição do benefício

**Condições:**
- **Conditions**: Condições para o benefício
- **Vesting Schedule**: Cronograma de aquisição

**Status:**
- **Is Active**: Ativo/inativo
- **Start Date**: Data de início
- **End Date**: Data de fim (opcional)

### **Tipos de Relacionamento:**

**HEIR:**
- Herdeiro legal
- Sucessão automática
- Direitos hereditários

**SPOUSE:**
- Cônjuge
- Direitos matrimoniais
- Benefícios conjugais

**CHILD:**
- Filho/filha
- Sucessão familiar
- Benefícios filiais

**PARENT:**
- Pai/mãe
- Relacionamento ascendente
- Benefícios parentais

**SIBLING:**
- Irmão/irmã
- Relacionamento fraternal
- Benefícios entre irmãos

**OTHER:**
- Outros relacionamentos
- Definição específica
- Benefícios customizados

### **Validação de 100%:**
- Sistema verifica se total de Benefit Percentage = 100%
- Alerta se distribuição incompleta
- Bloqueia salvamento se inválido

### **Como Criar uma Beneficiary Relation:**

**Passo 1 - Definir Relacionamento:**
1. Acesse `Parties → Beneficiary Relations`
2. Clique em **"Add Beneficiary Relation"**
3. Selecione **Benefactor** e **Beneficiary**

**Passo 2 - Tipo de Relacionamento:**
1. Selecione **Relationship Type**
2. Adicione **Relationship Description**

**Passo 3 - Benefício:**
1. Defina **Benefit Percentage**
2. Selecione **Benefit Type**
3. Adicione **Benefit Description**

**Passo 4 - Condições:**
1. Especifique **Conditions** (se aplicável)
2. Configure **Vesting Schedule**

**Passo 5 - Status:**
1. Marque **Is Active** = True
2. Defina **Start Date**
3. Configure **End Date** (se temporário)

### **Exemplo de Beneficiary Relations para John Smith:**
```
Relation 1:
- Benefactor: John Smith
- Beneficiary: Mary Smith (spouse)
- Relationship Type: SPOUSE
- Relationship Description: "Legal spouse"
- Benefit Percentage: 60.00
- Benefit Type: INHERITANCE
- Benefit Description: "Inheritance rights"
- Conditions: "Upon death of benefactor"
- Is Active: True

Relation 2:
- Benefactor: John Smith
- Beneficiary: John Smith Jr. (son)
- Relationship Type: CHILD
- Relationship Description: "Biological son"
- Benefit Percentage: 40.00
- Benefit Type: INHERITANCE
- Benefit Description: "Inheritance rights"
- Conditions: "Upon death of benefactor, minimum age 25"
- Vesting Schedule: "25% at age 25, 75% at age 30"
- Is Active: True

Total: 100% ✅
```

---

## 📎 **DOCUMENT ATTACHMENTS (Documentos Anexos)**

### **O que são Document Attachments:**
Document Attachments são documentos diversos anexados às Parties, organizados por categoria e acessíveis via URL.

### **Acesso:**
```
Django Admin → Parties → Document Attachments
```

### **Campos do Document Attachment:**

**Relacionamento:**
- **Party**: Party proprietária do documento

**Documento:**
- **Document Name**: Nome do documento
- **Document Category**: Categoria (veja lista abaixo)
- **Document Type**: Tipo específico

**Acesso:**
- **Document URL**: URL do documento
- **Access Level**: PUBLIC, RESTRICTED, CONFIDENTIAL

**Metadados:**
- **Upload Date**: Data de upload
- **File Size**: Tamanho do arquivo
- **File Format**: Formato (PDF, JPG, etc.)

**Validade:**
- **Expiry Date**: Data de expiração (opcional)
- **Is Valid**: Válido/inválido

### **Categorias de Documento:**

**IDENTITY:**
- Documentos de identidade
- Passaportes, RG, CNH
- Comprovação de identidade

**ADDRESS:**
- Comprovantes de endereço
- Contas de utilidades
- Extratos bancários

**INCOME:**
- Comprovantes de renda
- Declaração de IR
- Contracheques

**FINANCIAL:**
- Documentos financeiros
- Extratos bancários
- Demonstrações financeiras

**LEGAL:**
- Documentos legais
- Contratos, procurações
- Certidões

**CORPORATE:**
- Documentos corporativos
- Atas, estatutos
- Certificados

**COMPLIANCE:**
- Documentos de compliance
- KYC, AML
- Due diligence

**OTHER:**
- Outros documentos
- Documentos específicos
- Arquivos diversos

### **Níveis de Acesso:**

**PUBLIC:**
- Acesso público
- Sem restrições
- Documentos gerais

**RESTRICTED:**
- Acesso restrito
- Usuários autorizados
- Documentos sensíveis

**CONFIDENTIAL:**
- Acesso confidencial
- Usuários específicos
- Documentos críticos

### **Como Criar um Document Attachment:**

**Passo 1 - Selecionar Party:**
1. Acesse `Parties → Document Attachments`
2. Clique em **"Add Document Attachment"**
3. Selecione **Party** correspondente

**Passo 2 - Informações do Documento:**
1. Preencha **Document Name**
2. Selecione **Document Category**
3. Especifique **Document Type**

**Passo 3 - Acesso:**
1. Adicione **Document URL**
2. Defina **Access Level**

**Passo 4 - Metadados:**
1. **Upload Date** será preenchido automaticamente
2. Configure **File Size** e **File Format**

**Passo 5 - Validade:**
1. Defina **Expiry Date** (se aplicável)
2. Confirme **Is Valid** = True

### **Exemplo de Document Attachments para John Smith:**
```
Document 1:
- Party: John Smith
- Document Name: "US Passport"
- Document Category: IDENTITY
- Document Type: "Passport"
- Document URL: "https://docs.sirius.com/john_smith_passport.pdf"
- Access Level: RESTRICTED
- File Size: 2.5 MB
- File Format: PDF
- Is Valid: True

Document 2:
- Party: John Smith
- Document Name: "2024 Tax Return"
- Document Category: INCOME
- Document Type: "Tax Return"
- Document URL: "https://docs.sirius.com/john_smith_tax_2024.pdf"
- Access Level: CONFIDENTIAL
- File Size: 1.8 MB
- File Format: PDF
- Expiry Date: 2025-12-31
- Is Valid: True
```

---

## 🔍 **BUSCA E FILTROS**

### **Filtros Disponíveis:**

**Parties:**
- Por Person Type
- Por Nationality
- Por Risk Level
- Por KYC Status
- Por Is Partner

**Party Roles:**
- Por Role Type
- Por Is Active
- Por Start Date

**Passports:**
- Por Document Type
- Por Issuing Country
- Por Is Valid
- Por Expiry Date

**Beneficiary Relations:**
- Por Relationship Type
- Por Benefit Type
- Por Is Active

**Document Attachments:**
- Por Document Category
- Por Access Level
- Por Is Valid

### **Busca Textual:**
- **Parties**: Por name, email, occupation
- **Party Roles**: Por role_description, powers
- **Passports**: Por document_number
- **Document Attachments**: Por document_name

---

## 📊 **RELATÓRIOS DE PARTIES**

### **Relatório de Compliance:**
- Status de KYC por Party
- Documentos expirados/expirando
- Parties de alto risco
- PEPs identificadas

### **Relatório de Relacionamentos:**
- Mapa de beneficiary relations
- Validação de 100% distribuição
- Conflitos de interesse
- Estruturas familiares

### **Relatório de Documentos:**
- Documentos por categoria
- Status de validade
- Níveis de acesso
- Documentos faltantes

---

## 🚨 **ALERTAS E COMPLIANCE**

### **Alertas Automáticos:**
- **Documentos expirando** (30, 15, 0 dias)
- **KYC vencido** (> 1 ano)
- **PEP identificada** (revisão necessária)
- **Alto risco** (monitoramento)

### **Compliance Checks:**
- **Validação de dados** obrigatórios
- **Verificação de documentos**
- **Análise de risco**
- **Monitoramento PEP**

---

## 🔧 **SOLUÇÃO DE PROBLEMAS**

### **Problema: "Beneficiary Relations não soma 100%"**
**Soluções:**
1. Verifique todas as relations do mesmo Benefactor
2. Some os percentuais manualmente
3. Ajuste percentuais para totalizar 100%

### **Problema: "Passport aparece como expirado"**
**Soluções:**
1. Verifique Expiry Date
2. Atualize documento se necessário
3. Marque Is Valid = False se expirado

### **Problema: "Document URL não abre"**
**Soluções:**
1. Verifique se URL está correta
2. Confirme permissões de acesso
3. Teste URL em navegador

---

## 🏆 **MELHORES PRÁTICAS**

### **Gestão de Parties:**
1. **Mantenha** dados atualizados
2. **Monitore** status de compliance
3. **Revise** documentos periodicamente
4. **Documente** mudanças importantes

### **Compliance:**
1. **Execute** KYC regularmente
2. **Monitore** PEPs
3. **Atualize** documentos
4. **Mantenha** registros completos

### **Relacionamentos:**
1. **Valide** beneficiary relations
2. **Documente** mudanças familiares
3. **Monitore** conflitos
4. **Mantenha** 100% distribuição

---

## 🎯 **RESUMO EXECUTIVO**

O App Parties é fundamental para:

1. **Gerenciar** todas as pessoas envolvidas
2. **Controlar** compliance e KYC
3. **Documentar** relacionamentos
4. **Manter** registros atualizados
5. **Garantir** conformidade regulatória

**Resultado:** Gestão completa e segura de todas as parties envolvidas nas estruturas corporativas.

**🎉 Use este manual para dominar a gestão de Parties no SIRIUS!**

