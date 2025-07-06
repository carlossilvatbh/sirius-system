# PLANO DE MELHORIAS SIRIUS - DJANGO ADMIN
## Product Owner Implementation Plan

**Autor:** Manus AI  
**Data:** 06 de Janeiro de 2025  
**Versão:** 1.0  
**Projeto:** SIRIUS - Strategic Intelligence Relationship & Interactive Universal System  

---

## SUMÁRIO EXECUTIVO

Este documento apresenta um plano detalhado para implementação de melhorias no Django Admin do sistema SIRIUS, focando exclusivamente no backend sem alterações no frontend, arquitetura ou infraestrutura. O plano abrange a criação e refatoração de sete módulos principais: UBO (Ultimate Beneficial Owner), Successor, Products, Legal Structure, Personalized Products, Jurisdiction Alert e Service.

O SIRIUS é uma plataforma de corporate e financial services que permite a montagem de estruturas em jurisdições específicas para clientes, servindo ao time de backoffice e comercial para montar, entender impactos e custos das estruturas e gerar relatórios. As melhorias propostas visam expandir significativamente as funcionalidades do sistema, mantendo a estabilidade e retrocompatibilidade com o código existente.

### Objetivos Principais

1. **Implementar módulo UBO** para gestão de Ultimate Beneficial Owners como pessoas físicas proprietárias ou beneficiárias
2. **Criar módulo Successor** para gestão de sucessão com percentuais e condições
3. **Refatorar módulo Configuration Template** para **Products** com funcionalidades comerciais expandidas
4. **Expandir módulo Legal Structure** com conexões hierárquicas e templates de documentos
5. **Transformar módulo Saved Configurations** em **Personalized Products**
6. **Aprimorar módulo Jurisdiction Alert** com prazos e periodicidade
7. **Implementar módulo Service** para atividades relacionadas aos produtos personalizados

### Impacto Esperado

As melhorias permitirão ao SIRIUS oferecer uma gestão completa do ciclo de vida de estruturas corporativas, desde a configuração inicial até a sucessão, com controle hierárquico de propriedade, gestão de serviços associados e alertas de compliance jurisdicionais. O sistema manterá sua natureza de catálogo comercial enquanto adiciona capacidades de personalização e gestão de relacionamentos complexos entre entidades.




---

## ANÁLISE DA SITUAÇÃO ATUAL

### Estrutura Existente do SIRIUS

O sistema SIRIUS atualmente possui uma arquitetura Django bem estruturada com cinco módulos principais implementados no Django Admin. A análise do código revela uma base sólida que pode ser expandida sem comprometer a estabilidade existente.

#### Módulos Atuais

**1. Estrutura (Legal Structure)**
O módulo central do sistema gerencia estruturas legais com informações detalhadas sobre custos, implicações tributárias, proteção patrimonial e requisitos operacionais. Possui 7 tipos de estruturas pré-definidas (BDAO_SAC, WYOMING_DAO_LLC, BTS_VAULT, WYOMING_FOUNDATION, WYOMING_CORP, NATIONALIZATION, FUND_TOKEN) com campos abrangentes para análise de viabilidade e custos.

**2. RegraValidacao (Validation Rules)**
Sistema de regras que define relacionamentos entre estruturas, incluindo combinações obrigatórias, recomendadas, incompatíveis, condicionais e sinérgicas. Possui severidade configurável (ERROR, WARNING, INFO) e suporte a condições específicas via JSON.

**3. Template (Configuration Templates)**
Templates pré-configurados para setores específicos (Technology, Real Estate, Trading, Family Office, Investment, General) com diferentes níveis de complexidade. Armazena configurações completas em formato JSON e mantém estatísticas de uso.

**4. ConfiguracaoSalva (Saved Configurations)**
Permite salvar configurações de trabalho em progresso com estimativas de custo e tempo. Funciona como área de rascunho para configurações que não são templates formais.

**5. AlertaJurisdicao (Jurisdiction Alerts)**
Sistema de alertas específicos por jurisdição (US, BR, BS, WY, GLOBAL) com diferentes tipos (TAX, COMPLIANCE, REPORTING, DEADLINE, REGULATORY) e níveis de prioridade. Possui relacionamento many-to-many com estruturas aplicáveis.

### Pontos Fortes da Implementação Atual

A implementação atual demonstra várias qualidades que facilitarão a expansão proposta. O uso consistente de choices para campos categóricos garante integridade de dados e facilita manutenção. Os fieldsets organizados no Django Admin proporcionam uma interface limpa e intuitiva para administradores. O sistema de validação com diferentes severidades permite flexibilidade na aplicação de regras de negócio.

A estrutura de metadados com created_at e updated_at em todos os modelos facilita auditoria e rastreamento de mudanças. O uso de JSONField para configurações complexas permite flexibilidade sem comprometer a estrutura do banco de dados. Os métodos personalizados nos modelos (como get_custo_total_primeiro_ano) demonstram boa separação de responsabilidades.

### Limitações Identificadas

Apesar da base sólida, algumas limitações impedem o atendimento completo dos novos requisitos de negócio. A ausência de conceito de proprietário ou beneficiário (UBO) limita a personalização de estruturas para clientes específicos. Não há sistema de sucessão ou transferência de propriedade, essencial para planejamento patrimonial de longo prazo.

O módulo atual de templates não suporta adequadamente a natureza comercial de produtos vendidos pelo time comercial. A falta de hierarquia entre estruturas impede a modelagem de holdings complexas com múltiplos níveis. Os alertas jurisdicionais não possuem sistema de prazos ou periodicidade, limitando sua utilidade para compliance contínuo.

Não existe conceito de serviços associados às estruturas, impedindo a gestão completa do relacionamento com clientes. A ausência de relatórios específicos para produtos personalizados limita a capacidade de análise e acompanhamento comercial.

---

## REQUISITOS DETALHADOS

### Requisitos Funcionais

#### RF001 - Módulo UBO (Ultimate Beneficial Owner)
O sistema deve permitir o cadastro e gestão de Ultimate Beneficial Owners como pessoas físicas que são proprietárias ou beneficiárias de Products ou Legal Structures. Cada UBO deve ser identificado por nome completo, data de nascimento, nacionalidade e Tax Identification Number (TIN). O TIN é um número emitido pelo país de residência fiscal do UBO, sem necessidade de validação automática neste momento.

Um mesmo UBO pode estar associado a múltiplos Products/Legal Structures simultaneamente, refletindo a realidade de clientes que possuem estruturas diversificadas. O sistema deve manter a integridade referencial e permitir consultas eficientes sobre todas as estruturas associadas a um UBO específico.

#### RF002 - Módulo Successor
O sistema deve implementar funcionalidade de sucessão onde uma ou mais pessoas físicas podem receber Products ou Legal Structures de um UBO. Cada sucessor deve receber um percentual específico de 0 a 100% do Product ou Legal Structure, com validação automática para garantir que a soma dos percentuais de todos os sucessores seja exatamente 100%.

Todo sucessor automaticamente se torna um UBO quando recebe a sucessão, permitindo que defina seus próprios sucessores e criando cadeias de sucessão (pai → filho → neto). O módulo sucessor deve funcionar exclusivamente dentro de Personalized Products, não sendo aplicável a Products genéricos.

#### RF003 - Módulo Products (Refatoração de Configuration Template)
O módulo Configuration Template deve ser refatorado para Products, expandindo significativamente sua funcionalidade e propósito. Products representa produtos comerciais com Commercial Name (texto livre) que conectam duas ou mais Legal Structures em arranjos hierárquicos.

O sistema deve permitir conexões hierárquicas ilimitadas entre Legal Structures, onde uma estrutura pode ser proprietária de outras, com múltiplos níveis hierárquicos e múltiplas estruturas em cada nível. Cada Product deve ter custo automaticamente calculado pela soma dos custos das Legal Structures componentes.

Cada Product deve ter um tipo de Master Agreement representado por URL para documento externo. Quando um Product se conecta a um ou mais UBOs, ele se torna um Personalized Product, mantendo todas as características do Product original mas adicionando informações específicas do cliente.

#### RF004 - Expansão do Módulo Legal Structure
O módulo Legal Structure deve ser expandido para suportar conexões permitidas entre diferentes tipos de estruturas. Por exemplo, Legal Structure A pode ser proprietária das Legal Structures B, C, D, mas Legal Structure B pode ser proprietária apenas da Legal Structure C, não da A. Essas regras devem ser configuráveis manualmente pelo usuário, utilizando lógica similar ao campo Applicability dos Jurisdiction Alerts.

Cada tipo de Legal Structure deve suportar múltiplos templates de documentos, armazenados como URLs externas. Quando uma Legal Structure se conecta a um ou mais UBOs, ela se torna um Personalized Product, similar ao comportamento dos Products.

#### RF005 - Módulo Personalized Products (Refatoração de Saved Configurations)
O módulo Saved Configurations deve ser transformado em Personalized Products, representando Products ou Legal Structures associadas a um ou mais UBOs. Esta transformação implica ampliação significativa de funcionalidades além da simples mudança de nome.

Personalized Products devem manter todas as informações do Product ou Legal Structure original, adicionando informações específicas dos UBOs associados, sucessores definidos, e histórico de modificações. Sempre que houver mudança nos UBOs, sucessores ou conexões hierárquicas, deve ser gerado um novo Personalized Product, mantendo versionamento implícito.

#### RF006 - Aprimoramento do Módulo Jurisdiction Alert
O módulo Jurisdiction Alert deve ser expandido com campo de prazo que pode ser data única ou evento repetível periodicamente (mensal, trimestral, semestral ou anual). Deve incluir campo para link de template (URL externa) que pode ser utilizado para cumprimento da obrigação.

Deve ser adicionado campo para link onde a obrigação deve ser cumprida (URL externa) e opção de conexão com Services. O sistema deve manter a flexibilidade atual de aplicabilidade a estruturas específicas.

#### RF007 - Módulo Service
Novo módulo para gestão de atividades desempenhadas para Personalized Products. Cada Service pode ser associado a uma Legal Structure ou Product, e quando associado, transforma-se em um Personalized Product. Services devem ter descrição em campo livre para máxima flexibilidade.

Services associados devem herdar características do Product/Legal Structure original, tornando-se instâncias específicas com informações adicionais sobre a atividade prestada.

### Requisitos Não Funcionais

#### RNF001 - Retrocompatibilidade
Todas as alterações devem manter 100% de retrocompatibilidade com o código existente. Nenhuma funcionalidade atual deve ser quebrada ou removida. Migrações de banco de dados devem ser seguras e reversíveis.

#### RNF002 - Performance
As novas funcionalidades devem manter ou melhorar a performance atual do sistema. Consultas complexas envolvendo hierarquias devem ser otimizadas com select_related e prefetch_related apropriados.

#### RNF003 - Usabilidade do Django Admin
A interface do Django Admin deve permanecer intuitiva e organizada. Novos campos e relacionamentos devem seguir os padrões estabelecidos de fieldsets e organização visual.

#### RNF004 - Integridade de Dados
O sistema deve garantir integridade referencial em todos os relacionamentos. Validações de percentuais de sucessão devem ser implementadas tanto no modelo quanto no admin.

#### RNF005 - Escalabilidade
A estrutura deve suportar crescimento significativo no número de UBOs, Products e relacionamentos sem degradação de performance.


---

## ARQUITETURA E DESIGN DOS MÓDULOS

### Módulo UBO (Ultimate Beneficial Owner)

#### Estrutura do Model

O modelo UBO deve ser implementado como uma entidade independente com campos específicos para identificação de pessoas físicas. A estrutura proposta inclui campos obrigatórios para nome_completo (CharField com max_length=200), data_nascimento (DateField), nacionalidade (CharField com choices pré-definidas dos principais países), e tin (CharField para Tax Identification Number).

Campos adicionais incluem endereco_residencia_fiscal (TextField), telefone (CharField opcional), email (EmailField opcional), e observacoes (TextField opcional para informações complementares). Metadados padrão incluem created_at, updated_at e ativo (BooleanField).

#### Relacionamentos

O modelo UBO deve ter relacionamento many-to-many com Products e Legal Structures através de modelos intermediários que permitam armazenar informações específicas da associação, como percentual de propriedade e data de início da associação.

#### Django Admin Configuration

O admin deve incluir list_display com nome_completo, nacionalidade, tin, data_nascimento e ativo. Filtros por nacionalidade e status ativo. Busca por nome_completo, tin e email. Fieldsets organizados em "Informações Pessoais", "Informações Fiscais", "Contato" e "Metadados".

### Módulo Successor

#### Estrutura do Model

O modelo Successor deve implementar relacionamento entre UBO (proprietário atual) e sucessor (pessoa que receberá), com campos para percentual (DecimalField com validação 0-100), data_definicao (DateTimeField auto_now_add), data_efetivacao (DateField opcional para quando a sucessão deve ocorrer), e condicoes (TextField opcional para condições específicas).

O modelo deve incluir validação customizada para garantir que a soma dos percentuais de todos os sucessores de um UBO específico seja exatamente 100%. Esta validação deve ser implementada tanto no modelo (método clean) quanto no admin (form validation).

#### Relacionamentos

Relacionamento ForeignKey com UBO (como proprietário atual), ForeignKey com UBO (como sucessor), e relacionamento opcional com PersonalizedProduct para indicar qual produto específico está sendo transferido.

#### Lógica de Negócio

Quando uma sucessão é efetivada, o sistema deve automaticamente criar um novo registro UBO se o sucessor ainda não existir como UBO, e criar um novo PersonalizedProduct refletindo a nova propriedade. O UBO original mantém seus registros históricos, mas o PersonalizedProduct ativo passa a referenciar o novo proprietário.

### Módulo Products (Refatoração de Configuration Template)

#### Estrutura do Model Refatorado

O modelo Template existente deve ser refatorado para Product, mantendo compatibilidade com dados existentes através de migração cuidadosa. Novos campos incluem commercial_name (CharField para nome comercial), master_agreement_url (URLField para documento de Master Agreement), e custo_automatico (BooleanField para indicar se o custo é calculado automaticamente).

O campo configuracao deve ser expandido para suportar estrutura hierárquica de Legal Structures, incluindo informações sobre relacionamentos pai-filho e percentuais de propriedade entre estruturas.

#### Hierarquia de Legal Structures

A implementação de hierarquia deve utilizar modelo auxiliar ProductStructureHierarchy com campos product (ForeignKey), parent_structure (ForeignKey para Estrutura, nullable), child_structure (ForeignKey para Estrutura), ownership_percentage (DecimalField), e hierarchy_level (IntegerField para facilitar consultas).

Este design permite consultas eficientes de hierarquia usando select_related e prefetch_related, mantendo performance mesmo com estruturas complexas de múltiplos níveis.

#### Cálculo Automático de Custos

Método get_custo_total_calculado deve percorrer todas as Legal Structures associadas ao Product e somar seus custos base e manutenção. O cálculo deve considerar percentuais de propriedade quando aplicável e permitir override manual quando necessário.

### Módulo Legal Structure (Expansão)

#### Conexões Permitidas

Novo modelo LegalStructureConnection deve definir quais tipos de estruturas podem ser proprietárias de outras. Campos incluem parent_structure_type (CharField com choices dos tipos existentes), child_structure_type (CharField com choices), allowed (BooleanField), e restriction_reason (TextField opcional).

A validação de conexões deve ser implementada em método customizado que verifica se uma conexão específica é permitida antes de criar relacionamentos hierárquicos.

#### Templates de Documentos

Modelo DocumentTemplate deve armazenar templates específicos por tipo de Legal Structure. Campos incluem structure_type (CharField), template_name (CharField), template_url (URLField), document_category (CharField com choices como "Formation", "Compliance", "Tax"), e description (TextField).

Relacionamento one-to-many com Estrutura permite múltiplos templates por tipo de estrutura, organizados por categoria para facilitar localização.

### Módulo Personalized Products

#### Estrutura do Model Refatorado

O modelo ConfiguracaoSalva deve ser refatorado para PersonalizedProduct, expandindo significativamente sua funcionalidade. Novos campos incluem base_product (ForeignKey para Product, nullable), base_structure (ForeignKey para Estrutura, nullable), status (CharField com choices como "Active", "Pending", "Transferred"), e version_number (IntegerField para controle de versão).

Relacionamento many-to-many com UBO através de modelo intermediário PersonalizedProductOwnership que armazena percentual de propriedade e data de início.

#### Versionamento Automático

Sempre que houver mudança em UBOs, sucessores ou conexões hierárquicas, o sistema deve criar nova versão do PersonalizedProduct. Método create_new_version deve copiar todas as informações relevantes, incrementar version_number, e marcar a versão anterior como "Historical".

#### Relatórios Integrados

Método get_complete_report deve gerar relatório completo com todas as informações do PersonalizedProduct, incluindo UBOs associados, estruturas hierárquicas, custos detalhados, sucessores definidos, e serviços associados. Este relatório atende ao requisito principal do time de backoffice.

### Módulo Jurisdiction Alert (Aprimoramento)

#### Campos de Prazo e Periodicidade

Novos campos incluem deadline_type (CharField com choices "Single", "Recurring"), single_deadline (DateField opcional), recurrence_pattern (CharField com choices "Monthly", "Quarterly", "Semiannual", "Annual"), next_deadline (DateField calculado automaticamente), e last_completed (DateField opcional).

#### Templates e Links

Campos template_url (URLField opcional) e compliance_url (URLField opcional) para armazenar links externos. Campo service_connection (ForeignKey opcional para Service) permite associar alertas a serviços específicos.

#### Cálculo Automático de Próximos Prazos

Método calculate_next_deadline deve calcular automaticamente a próxima data de vencimento baseada no padrão de recorrência. Para alertas mensais, adiciona 1 mês à última data; para trimestrais, 3 meses; e assim por diante.

### Módulo Service

#### Estrutura do Model

Novo modelo Service com campos service_name (CharField), description (TextField), service_type (CharField com choices como "Legal", "Tax", "Compliance", "Administrative"), cost (DecimalField opcional), e estimated_duration (IntegerField em dias).

Relacionamentos opcionais com Product e Estrutura através de campos associated_product (ForeignKey opcional) e associated_structure (ForeignKey opcional). Quando associado, o Service se torna específico para aquele produto/estrutura.

#### Transformação em Personalized Product

Quando um Service é associado a Product ou Legal Structure, método create_personalized_service deve criar novo PersonalizedProduct que herda características do produto/estrutura original e adiciona informações específicas do serviço.

#### Gestão de Atividades

Modelo ServiceActivity para rastrear atividades específicas realizadas dentro de um Service. Campos incluem service (ForeignKey), activity_description (TextField), start_date (DateField), completion_date (DateField opcional), status (CharField), e responsible_person (CharField).

---

## RELACIONAMENTOS E INTEGRAÇÕES

### Diagrama de Relacionamentos

A nova arquitetura cria uma rede complexa de relacionamentos que deve ser cuidadosamente gerenciada para manter performance e integridade. O UBO se torna o centro da arquitetura, conectando-se a Products, Legal Structures e Services através de PersonalizedProducts.

Products mantêm relacionamento hierárquico com Legal Structures através de ProductStructureHierarchy, permitindo modelagem de holdings complexas. Successors criam relacionamentos temporais entre UBOs, permitindo planejamento de sucessão de longo prazo.

Services podem se conectar tanto a Products quanto a Legal Structures, criando instâncias específicas através de PersonalizedProducts. Jurisdiction Alerts mantêm relacionamentos com estruturas específicas e podem se conectar a Services para alertas de atividades.

### Integridade Referencial

Todas as foreign keys devem usar on_delete=models.PROTECT para evitar deleções acidentais que quebrem relacionamentos críticos. Exceções incluem relacionamentos com PersonalizedProduct onde on_delete=models.CASCADE é apropriado para manter limpeza de dados.

Constraints de banco de dados devem garantir que percentuais de sucessão somem 100% e que hierarquias não criem loops (uma estrutura não pode ser proprietária de si mesma direta ou indiretamente).

### Performance e Otimização

Consultas complexas envolvendo hierarquias devem usar select_related para relacionamentos diretos e prefetch_related para relacionamentos many-to-many. Índices de banco de dados devem ser criados em campos frequentemente consultados como UBO.tin, Product.commercial_name, e PersonalizedProduct.status.

Métodos de modelo que realizam cálculos complexos (como custo total de hierarquias) devem implementar cache quando apropriado, especialmente para Products com muitas Legal Structures associadas.


---

## PLANO DE IMPLEMENTAÇÃO

### Estratégia de Implementação

A implementação das melhorias do SIRIUS deve seguir uma abordagem incremental e modular, priorizando estabilidade e retrocompatibilidade. A estratégia proposta divide o trabalho em cinco fases principais, cada uma focada em um conjunto específico de funcionalidades que podem ser desenvolvidas, testadas e implantadas independentemente.

Esta abordagem permite validação contínua das funcionalidades implementadas, reduz riscos de introdução de bugs, e possibilita feedback iterativo do time de usuários. Cada fase inclui desenvolvimento de modelos, configuração do Django Admin, testes unitários, e documentação específica.

### Fase 1: Implementação do Módulo UBO (Semanas 1-2)

#### Objetivos da Fase
Estabelecer a base fundamental do sistema expandido através da implementação completa do módulo UBO. Esta fase é crítica pois o UBO se torna o centro da nova arquitetura, sendo referenciado por todos os outros módulos subsequentes.

#### Atividades Detalhadas

**Semana 1: Desenvolvimento do Model e Migrações**
Criação do modelo UBO com todos os campos especificados, incluindo validações customizadas para TIN e nacionalidade. Implementação de métodos auxiliares para formatação de dados e consultas otimizadas. Criação de migração inicial com dados de teste para validação.

Desenvolvimento de testes unitários abrangentes cobrindo validações de modelo, métodos customizados, e cenários de edge cases. Implementação de fixtures para facilitar testes e desenvolvimento futuro.

**Semana 2: Configuração do Django Admin e Integração**
Configuração completa do UBOAdmin com fieldsets organizados, filtros apropriados, e funcionalidades de busca otimizadas. Implementação de métodos de display customizados para melhor visualização de dados no admin.

Criação de relacionamentos iniciais com modelos existentes (Estrutura) através de modelos intermediários que serão expandidos nas fases subsequentes. Testes de integração para garantir que a adição do módulo UBO não afeta funcionalidades existentes.

#### Entregáveis da Fase
- Modelo UBO completamente implementado e testado
- Configuração Django Admin funcional e intuitiva
- Migrações de banco de dados seguras e reversíveis
- Documentação técnica do módulo
- Suite de testes unitários com cobertura mínima de 90%

#### Critérios de Aceitação
- Todos os campos do UBO funcionam conforme especificado
- Interface admin permite CRUD completo de UBOs
- Validações impedem criação de UBOs com dados inválidos
- Performance de consultas mantém padrões existentes
- Nenhuma funcionalidade existente é afetada

### Fase 2: Implementação do Módulo Successor (Semanas 3-4)

#### Objetivos da Fase
Implementar sistema completo de sucessão que permite definição de sucessores para UBOs com validação de percentuais e suporte a cadeias de sucessão. Esta fase estabelece a base para planejamento patrimonial de longo prazo.

#### Atividades Detalhadas

**Semana 3: Desenvolvimento do Sistema de Sucessão**
Criação do modelo Successor com relacionamentos apropriados para UBO proprietário e sucessor. Implementação de validação complexa para garantir que soma de percentuais seja exatamente 100% por UBO. Desenvolvimento de métodos para cálculo automático de percentuais disponíveis e validação de cadeias de sucessão.

Implementação de lógica para transformação automática de sucessores em UBOs quando apropriado. Criação de métodos para visualização de árvores de sucessão e detecção de conflitos potenciais.

**Semana 4: Interface Admin e Validações Avançadas**
Configuração do SuccessorAdmin com validações em tempo real de percentuais. Implementação de interface intuitiva para definição de múltiplos sucessores com feedback visual sobre percentuais restantes.

Desenvolvimento de relatórios de sucessão que mostram cadeias completas e potenciais problemas. Integração com módulo UBO para mostrar sucessões definidas na interface de cada UBO.

#### Entregáveis da Fase
- Modelo Successor com validações complexas
- Interface admin com validação em tempo real
- Relatórios de cadeia de sucessão
- Integração completa com módulo UBO
- Testes abrangentes de cenários de sucessão

#### Critérios de Aceitação
- Validação de 100% de percentuais funciona corretamente
- Cadeias de sucessão são criadas automaticamente
- Interface admin previne configurações inválidas
- Relatórios mostram informações precisas e completas
- Performance mantém-se adequada mesmo com sucessões complexas

### Fase 3: Refatoração para Módulo Products (Semanas 5-7)

#### Objetivos da Fase
Transformar o módulo Configuration Template em Products com funcionalidades comerciais expandidas, incluindo hierarquias de Legal Structures e cálculo automático de custos. Esta é a fase mais complexa devido à necessidade de migração de dados existentes.

#### Atividades Detalhadas

**Semana 5: Planejamento e Migração de Dados**
Análise detalhada dos dados existentes em Template para planejamento de migração segura. Desenvolvimento de scripts de migração que preservam todas as informações existentes enquanto adicionam novos campos e funcionalidades.

Criação de modelos auxiliares para hierarquia de estruturas (ProductStructureHierarchy) com otimizações para consultas eficientes. Implementação de validações para prevenir loops hierárquicos e garantir integridade de relacionamentos.

**Semana 6: Implementação de Funcionalidades Comerciais**
Desenvolvimento de funcionalidades específicas para produtos comerciais, incluindo commercial_name, master_agreement_url, e integração com sistema de custos automáticos. Implementação de métodos para cálculo de custo total baseado em hierarquia de estruturas.

Criação de interface para definição de hierarquias complexas com múltiplos níveis. Desenvolvimento de visualizações que mostram estrutura hierárquica de forma intuitiva no Django Admin.

**Semana 7: Integração e Otimização**
Integração completa com módulos UBO e Successor para criação de Personalized Products. Otimização de consultas para hierarquias complexas usando select_related e prefetch_related apropriados.

Implementação de cache para cálculos complexos de custo e validação de performance com datasets grandes. Criação de relatórios específicos para produtos comerciais.

#### Entregáveis da Fase
- Modelo Product refatorado com funcionalidades expandidas
- Sistema de hierarquia de Legal Structures
- Migração segura de dados existentes
- Interface admin otimizada para produtos comerciais
- Relatórios de hierarquia e custos

#### Critérios de Aceitação
- Todos os dados existentes são migrados sem perda
- Hierarquias funcionam corretamente em múltiplos níveis
- Cálculo automático de custos é preciso
- Performance é mantida ou melhorada
- Interface admin é intuitiva para usuários existentes

### Fase 4: Expansão de Legal Structure e Personalized Products (Semanas 8-10)

#### Objetivos da Fase
Expandir o módulo Legal Structure com conexões permitidas e templates de documentos, e transformar Saved Configurations em Personalized Products com funcionalidades completas de versionamento e relatórios.

#### Atividades Detalhadas

**Semana 8: Expansão de Legal Structure**
Implementação do sistema de conexões permitidas entre tipos de Legal Structures. Criação de interface administrativa para configuração de regras de conexão com validação em tempo real.

Desenvolvimento do sistema de templates de documentos com categorização e URLs externas. Integração com sistema de hierarquias para validação automática de conexões permitidas.

**Semana 9: Refatoração para Personalized Products**
Transformação completa do modelo ConfiguracaoSalva em PersonalizedProduct com funcionalidades expandidas. Implementação de sistema de versionamento automático que cria novas versões quando há mudanças em UBOs ou sucessores.

Desenvolvimento de relacionamentos complexos com UBO, Products, e Legal Structures. Criação de métodos para geração de relatórios completos conforme especificado pelos requisitos.

**Semana 10: Integração e Relatórios**
Integração completa entre todos os módulos implementados até o momento. Desenvolvimento do relatório principal que contém todos os campos do Personalized Product conforme solicitado pelo time de backoffice.

Otimização de consultas para relatórios complexos e implementação de cache quando apropriado. Testes de integração abrangentes para garantir que todos os módulos funcionam harmoniosamente.

#### Entregáveis da Fase
- Legal Structure expandido com conexões e templates
- PersonalizedProduct completamente funcional
- Sistema de versionamento automático
- Relatório principal para backoffice
- Integração completa entre módulos

#### Critérios de Aceitação
- Conexões entre Legal Structures funcionam conforme regras
- Templates de documentos são acessíveis e organizados
- Versionamento automático funciona corretamente
- Relatório principal contém todas as informações necessárias
- Performance é adequada para operações complexas

### Fase 5: Jurisdiction Alert e Service (Semanas 11-12)

#### Objetivos da Fase
Finalizar a implementação com aprimoramentos no módulo Jurisdiction Alert e criação completa do módulo Service, estabelecendo todas as integrações finais e otimizações de sistema.

#### Atividades Detalhadas

**Semana 11: Aprimoramento de Jurisdiction Alert**
Implementação de campos de prazo e periodicidade com cálculo automático de próximas datas. Desenvolvimento de sistema de recorrência que suporta padrões mensais, trimestrais, semestrais e anuais.

Adição de campos para templates e links de compliance. Integração com módulo Service para alertas associados a atividades específicas.

**Semana 12: Implementação do Módulo Service**
Criação completa do módulo Service com funcionalidades para gestão de atividades relacionadas a Personalized Products. Implementação de transformação automática em Personalized Product quando Service é associado a Product ou Legal Structure.

Desenvolvimento de sistema de rastreamento de atividades com status e responsáveis. Integração final com todos os outros módulos e otimização geral do sistema.

#### Entregáveis da Fase
- Jurisdiction Alert com funcionalidades de prazo e periodicidade
- Módulo Service completamente implementado
- Integração final entre todos os módulos
- Otimizações de performance do sistema completo
- Documentação final e manual de usuário

#### Critérios de Aceitação
- Alertas com periodicidade funcionam automaticamente
- Services são criados e gerenciados corretamente
- Todas as integrações funcionam harmoniosamente
- Performance geral do sistema é adequada
- Documentação está completa e atualizada

---

## ESTRATÉGIA DE MIGRAÇÃO DE DADOS

### Análise de Impacto nos Dados Existentes

A migração de dados existentes requer cuidado especial para garantir que nenhuma informação seja perdida e que o sistema continue funcionando durante e após a migração. A análise dos modelos atuais revela que Template e ConfiguracaoSalva são os únicos que requerem migração significativa de dados.

O modelo Template possui dados valiosos em formato JSON no campo configuracao que devem ser preservados e expandidos para suportar as novas funcionalidades de Products. O modelo ConfiguracaoSalva contém configurações de usuários que devem ser transformadas em PersonalizedProducts mantendo todas as informações existentes.

### Estratégia de Migração Incremental

**Fase 1: Preparação e Backup**
Antes de qualquer migração, deve ser criado backup completo do banco de dados. Scripts de validação devem verificar integridade dos dados existentes e identificar possíveis inconsistências que precisam ser corrigidas antes da migração.

**Fase 2: Migração de Template para Product**
A migração deve criar novos registros Product baseados nos Templates existentes, preservando todos os campos compatíveis. Novos campos como commercial_name devem ser populados com valores padrão baseados no nome existente, permitindo edição posterior pelos usuários.

O campo configuracao JSON deve ser analisado e expandido para incluir informações de hierarquia quando aplicável. Templates que já contêm estruturas múltiplas devem ter suas hierarquias inferidas e criadas automaticamente.

**Fase 3: Migração de ConfiguracaoSalva para PersonalizedProduct**
Configurações salvas devem ser transformadas em PersonalizedProducts com version_number inicial 1. Como não há UBOs associados inicialmente, estes registros devem ser marcados com status especial "Legacy" até que sejam associados a UBOs específicos.

**Fase 4: Validação e Limpeza**
Após cada migração, scripts de validação devem verificar que todos os dados foram migrados corretamente. Comparações entre dados originais e migrados devem confirmar integridade. Dados temporários e tabelas de backup devem ser mantidos por período de segurança antes da limpeza final.

### Scripts de Migração Reversível

Todos os scripts de migração devem incluir funcionalidade de reversão que permite retornar ao estado anterior em caso de problemas. Migrações Django devem usar RunPython com reverse_code apropriado para garantir reversibilidade completa.

Scripts de validação devem ser executados antes e após cada migração para confirmar que o estado do banco de dados permanece consistente. Logs detalhados devem registrar todas as operações realizadas para facilitar debugging se necessário.

---

## TESTES E VALIDAÇÃO

### Estratégia de Testes

A estratégia de testes deve garantir que todas as funcionalidades novas funcionem corretamente e que nenhuma funcionalidade existente seja quebrada. Testes devem cobrir modelos, validações, Django Admin, e integrações entre módulos.

#### Testes Unitários

Cada modelo deve ter testes unitários abrangentes cobrindo validações, métodos customizados, e relacionamentos. Testes devem incluir casos de sucesso, casos de erro, e edge cases específicos do domínio de negócio.

Validações complexas como soma de percentuais de sucessão devem ter testes específicos cobrindo múltiplos cenários. Métodos de cálculo como custo total de hierarquias devem ser testados com estruturas de diferentes complexidades.

#### Testes de Integração

Testes de integração devem verificar que módulos funcionam corretamente em conjunto. Cenários complexos como criação de PersonalizedProduct com UBO, sucessores, e hierarquia de estruturas devem ser testados end-to-end.

Migrações de dados devem ter testes específicos que verificam integridade antes e após a migração. Testes devem usar datasets realistas para identificar problemas que podem não aparecer com dados de teste simples.

#### Testes de Performance

Consultas complexas envolvendo hierarquias e relacionamentos múltiplos devem ser testadas para garantir performance adequada. Testes devem simular datasets grandes para identificar gargalos potenciais.

Operações que podem ser executadas frequentemente, como cálculo de custos e geração de relatórios, devem ter benchmarks estabelecidos para monitoramento contínuo de performance.

### Validação com Usuários

Cada fase deve incluir validação com usuários reais do sistema para garantir que as funcionalidades atendem às necessidades práticas. Feedback deve ser coletado sistematicamente e incorporado nas fases subsequentes.

Treinamento específico deve ser fornecido para novas funcionalidades, especialmente aquelas que alteram workflows existentes. Documentação de usuário deve ser atualizada continuamente durante o desenvolvimento.


---

## ANÁLISE DE RISCOS E MITIGAÇÃO

### Riscos Técnicos

#### Risco Alto: Complexidade de Migração de Dados
A migração de dados existentes, especialmente do modelo Template para Product, apresenta risco significativo devido à complexidade das configurações JSON existentes. Dados malformados ou inconsistentes podem causar falhas na migração ou perda de informações críticas.

**Mitigação:** Implementação de scripts de validação pré-migração que identificam e corrigem inconsistências. Criação de ambiente de teste idêntico ao produção para validação completa da migração. Backup completo antes de qualquer alteração e scripts de rollback testados.

#### Risco Médio: Performance com Hierarquias Complexas
Consultas envolvendo múltiplos níveis hierárquicos podem degradar performance significativamente, especialmente com crescimento do volume de dados. Relacionamentos complexos entre UBO, Products, e Legal Structures podem criar consultas N+1 inadvertidamente.

**Mitigação:** Implementação de índices apropriados no banco de dados. Uso consistente de select_related e prefetch_related em todas as consultas. Implementação de cache para cálculos complexos frequentemente executados. Monitoramento contínuo de performance com alertas automáticos.

#### Risco Médio: Validações Complexas de Percentuais
A validação de que percentuais de sucessão somem exatamente 100% pode ser complexa em cenários com múltiplos sucessores e edições simultâneas. Race conditions podem permitir estados inconsistentes temporariamente.

**Mitigação:** Implementação de validações tanto no modelo quanto no admin. Uso de transações de banco de dados para operações que afetam múltiplos sucessores. Implementação de locks otimistas para prevenir edições simultâneas conflitantes.

### Riscos de Negócio

#### Risco Alto: Interrupção de Operações Durante Migração
A migração de dados críticos pode requerer downtime do sistema, impactando operações do time de backoffice e comercial. Falhas durante a migração podem deixar o sistema em estado inconsistente.

**Mitigação:** Planejamento de janela de manutenção em horário de menor impacto. Implementação de migração incremental que permite rollback rápido. Comunicação clara com usuários sobre cronograma e impactos esperados.

#### Risco Médio: Curva de Aprendizado para Novas Funcionalidades
Usuários existentes podem ter dificuldade para adaptar-se às novas funcionalidades, especialmente mudanças na interface do Django Admin. Resistência à mudança pode reduzir adoção das melhorias.

**Mitigação:** Treinamento estruturado para usuários antes do lançamento. Documentação clara e acessível para todas as novas funcionalidades. Implementação gradual com período de suporte intensivo inicial.

#### Risco Baixo: Incompatibilidade com Workflows Existentes
Mudanças na estrutura de dados podem impactar workflows existentes ou integrações não documentadas. Relatórios ou processos manuais podem quebrar com as alterações.

**Mitigação:** Análise detalhada de workflows existentes antes da implementação. Manutenção de compatibilidade com interfaces existentes sempre que possível. Período de transição com suporte a formatos antigos e novos.

### Estratégias de Mitigação Geral

**Implementação Incremental:** Divisão do projeto em fases pequenas e independentes permite validação contínua e reduz impacto de problemas. Cada fase pode ser revertida independentemente se necessário.

**Testes Abrangentes:** Suite de testes automatizados garante que mudanças não quebrem funcionalidades existentes. Testes de integração validam que módulos funcionam corretamente em conjunto.

**Monitoramento Contínuo:** Implementação de logging detalhado e monitoramento de performance permite identificação rápida de problemas. Alertas automáticos notificam sobre degradação de performance ou erros.

**Comunicação Proativa:** Comunicação regular com stakeholders sobre progresso, riscos identificados, e mudanças de cronograma. Feedback contínuo dos usuários permite ajustes rápidos quando necessário.

---

## CONSIDERAÇÕES TÉCNICAS ESPECÍFICAS

### Otimização de Performance

#### Estratégias de Consulta
Implementação de consultas otimizadas é crucial para manter performance adequada com a complexidade adicional dos novos módulos. Relacionamentos hierárquicos requerem atenção especial para evitar consultas N+1 que podem degradar performance exponencialmente.

Uso de select_related deve ser implementado para relacionamentos ForeignKey diretos, especialmente em consultas que acessam dados de UBO, Product, e Legal Structure simultaneamente. Prefetch_related deve ser usado para relacionamentos many-to-many e reverse foreign keys, particularmente para sucessores e estruturas hierárquicas.

#### Indexação de Banco de Dados
Índices específicos devem ser criados para campos frequentemente consultados. UBO.tin, Product.commercial_name, e PersonalizedProduct.status são candidatos principais para indexação. Índices compostos podem ser necessários para consultas que filtram por múltiplos campos simultaneamente.

Índices para campos de data como Successor.data_efetivacao e AlertaJurisdicao.next_deadline são essenciais para consultas de relatórios temporais. Análise de query plans deve ser realizada regularmente para identificar oportunidades de otimização.

#### Cache e Armazenamento
Cálculos complexos como custo total de hierarquias devem implementar cache inteligente que invalida automaticamente quando dados subjacentes mudam. Django cache framework pode ser usado para armazenar resultados de cálculos caros por períodos apropriados.

Relatórios complexos que agregam dados de múltiplos módulos devem considerar cache de longo prazo com invalidação baseada em mudanças de dados. Implementação de cache warming pode pré-calcular relatórios frequentemente acessados.

### Segurança e Integridade

#### Validação de Dados
Validações robustas devem ser implementadas tanto no nível de modelo quanto no Django Admin. Validações de modelo garantem integridade independente da interface de acesso, enquanto validações de admin proporcionam feedback imediato aos usuários.

Validação de percentuais de sucessão deve incluir verificação de precisão decimal para evitar problemas de arredondamento. Validação de hierarquias deve prevenir loops e estruturas inválidas que podem causar problemas de performance ou lógica.

#### Controle de Acesso
Embora o sistema seja usado apenas por administradores internos, diferentes níveis de acesso podem ser necessários para diferentes tipos de usuários. Implementação de grupos de usuários Django pode controlar acesso a funcionalidades específicas.

Auditoria de mudanças críticas como alterações em UBOs ou sucessores pode ser implementada através de Django signals ou bibliotecas especializadas como django-simple-history.

### Escalabilidade

#### Crescimento de Dados
O sistema deve ser projetado para suportar crescimento significativo no número de UBOs, Products, e relacionamentos. Estruturas de dados devem ser eficientes mesmo com milhares de registros e relacionamentos complexos.

Particionamento de dados pode ser considerado para tabelas que crescem rapidamente, especialmente logs de atividades e histórico de mudanças. Arquivamento de dados antigos deve ser planejado para manter performance de consultas ativas.

#### Arquitetura Modular
Implementação modular permite expansão futura sem impacto em funcionalidades existentes. Cada módulo deve ter interfaces bem definidas que facilitam manutenção e extensão.

Separação clara de responsabilidades entre modelos, views, e lógica de negócio facilita manutenção e permite otimizações específicas por área. Uso de Django apps separados para cada módulo principal mantém organização e facilita desenvolvimento paralelo.

---

## CRONOGRAMA DETALHADO

### Visão Geral do Cronograma

O projeto está estruturado em 12 semanas de desenvolvimento intensivo, divididas em 5 fases principais. Cada fase tem objetivos específicos e entregáveis claramente definidos, permitindo validação incremental e ajustes conforme necessário.

| Fase | Duração | Semanas | Foco Principal |
|------|---------|---------|----------------|
| 1 | 2 semanas | 1-2 | Módulo UBO |
| 2 | 2 semanas | 3-4 | Módulo Successor |
| 3 | 3 semanas | 5-7 | Refatoração Products |
| 4 | 3 semanas | 8-10 | Legal Structure e Personalized Products |
| 5 | 2 semanas | 11-12 | Jurisdiction Alert e Service |

### Cronograma Detalhado por Semana

#### Semana 1: Fundação UBO
**Dias 1-2:** Análise detalhada de requisitos e design do modelo UBO. Criação de especificações técnicas detalhadas e validação com stakeholders.

**Dias 3-4:** Implementação do modelo UBO com todos os campos e validações. Criação de migrações iniciais e testes unitários básicos.

**Dia 5:** Configuração inicial do Django Admin para UBO. Testes de integração com sistema existente.

#### Semana 2: Finalização UBO
**Dias 1-2:** Refinamento da interface Django Admin com fieldsets, filtros, e funcionalidades de busca. Implementação de métodos de display customizados.

**Dias 3-4:** Testes abrangentes incluindo edge cases e validação de performance. Criação de fixtures e dados de teste.

**Dia 5:** Documentação técnica e validação final da fase. Preparação para demonstração aos usuários.

#### Semana 3: Base do Successor
**Dias 1-2:** Design e implementação do modelo Successor com relacionamentos complexos. Desenvolvimento de validações de percentual.

**Dias 3-4:** Implementação de lógica de negócio para cadeias de sucessão. Criação de métodos para validação automática de consistência.

**Dia 5:** Testes unitários para validações complexas e cenários de sucessão múltipla.

#### Semana 4: Interface Successor
**Dias 1-2:** Configuração avançada do Django Admin para Successor com validação em tempo real. Implementação de interface intuitiva para múltiplos sucessores.

**Dias 3-4:** Desenvolvimento de relatórios de sucessão e integração com módulo UBO. Testes de usabilidade com usuários.

**Dia 5:** Finalização e documentação da fase. Validação de todos os requisitos de sucessão.

#### Semana 5: Planejamento Products
**Dias 1-2:** Análise detalhada de dados existentes em Template. Desenvolvimento de estratégia de migração segura.

**Dias 3-4:** Criação de scripts de migração e validação. Implementação de modelos auxiliares para hierarquia.

**Dia 5:** Testes de migração em ambiente de desenvolvimento. Refinamento de scripts baseado em resultados.

#### Semana 6: Implementação Products
**Dias 1-2:** Refatoração do modelo Template para Product com novos campos. Implementação de funcionalidades comerciais.

**Dias 3-4:** Desenvolvimento de sistema de hierarquia de Legal Structures. Criação de interface admin para hierarquias.

**Dia 5:** Testes de funcionalidades básicas de Products. Validação de cálculos automáticos de custo.

#### Semana 7: Otimização Products
**Dias 1-2:** Otimização de consultas para hierarquias complexas. Implementação de cache para cálculos caros.

**Dias 3-4:** Integração com módulos UBO e Successor. Testes de integração abrangentes.

**Dia 5:** Finalização da migração de dados e validação completa. Documentação de funcionalidades de Products.

#### Semana 8: Expansão Legal Structure
**Dias 1-2:** Implementação de sistema de conexões permitidas. Criação de interface para configuração de regras.

**Dias 3-4:** Desenvolvimento de sistema de templates de documentos. Integração com hierarquias existentes.

**Dia 5:** Testes de validação de conexões e funcionalidades de templates.

#### Semana 9: Base Personalized Products
**Dias 1-2:** Refatoração de ConfiguracaoSalva para PersonalizedProduct. Implementação de sistema de versionamento.

**Dias 3-4:** Desenvolvimento de relacionamentos complexos com todos os módulos. Criação de métodos para relatórios.

**Dia 5:** Testes de versionamento automático e integridade de dados.

#### Semana 10: Integração Completa
**Dias 1-2:** Integração final entre todos os módulos implementados. Desenvolvimento do relatório principal.

**Dias 3-4:** Otimização de performance para operações complexas. Testes de stress com dados grandes.

**Dia 5:** Validação completa de todos os requisitos de PersonalizedProduct. Preparação para fase final.

#### Semana 11: Jurisdiction Alert Avançado
**Dias 1-2:** Implementação de campos de prazo e periodicidade. Desenvolvimento de cálculo automático de datas.

**Dias 3-4:** Adição de templates e links de compliance. Integração com módulo Service.

**Dia 5:** Testes de funcionalidades de periodicidade e alertas automáticos.

#### Semana 12: Finalização Service
**Dias 1-2:** Implementação completa do módulo Service. Desenvolvimento de transformação em PersonalizedProduct.

**Dias 3-4:** Integração final com todos os módulos. Otimização geral do sistema.

**Dia 5:** Testes finais, documentação completa, e preparação para entrega.

### Marcos e Entregas

**Marco 1 (Semana 2):** Módulo UBO completamente funcional
**Marco 2 (Semana 4):** Sistema de sucessão operacional
**Marco 3 (Semana 7):** Products refatorado com hierarquias
**Marco 4 (Semana 10):** PersonalizedProducts com relatórios
**Marco 5 (Semana 12):** Sistema completo com todos os módulos

### Recursos Necessários

**Desenvolvimento:** 1 desenvolvedor Django sênior em tempo integral
**Testes:** Acesso a ambiente de teste idêntico ao produção
**Validação:** Disponibilidade de usuários para feedback em cada fase
**Infraestrutura:** Backup completo do sistema antes de cada fase crítica

---

## CONCLUSÃO E PRÓXIMOS PASSOS

### Resumo do Plano

Este plano de implementação apresenta uma estratégia abrangente e detalhada para expandir significativamente as funcionalidades do SIRIUS através de melhorias focadas no Django Admin. A abordagem incremental de 5 fases garante estabilidade e permite validação contínua, enquanto mantém total retrocompatibilidade com o sistema existente.

As melhorias propostas transformarão o SIRIUS de um sistema de configuração de estruturas em uma plataforma completa de gestão de relacionamentos corporativos, incluindo proprietários beneficiários, sucessão patrimonial, hierarquias complexas, e gestão de serviços associados. Esta expansão posicionará o SIRIUS como uma ferramenta ainda mais valiosa para o time de backoffice e comercial.

### Benefícios Esperados

**Para o Negócio:** Capacidade de oferecer serviços mais sofisticados aos clientes, incluindo planejamento de sucessão e gestão de estruturas hierárquicas complexas. Relatórios mais detalhados facilitarão análise de rentabilidade e identificação de oportunidades comerciais.

**Para os Usuários:** Interface mais intuitiva e funcional no Django Admin, com relatórios abrangentes que consolidam todas as informações necessárias em um local central. Automação de cálculos e validações reduzirá erros manuais e aumentará eficiência operacional.

**Para o Sistema:** Arquitetura mais robusta e escalável que suporta crescimento futuro. Modularidade aprimorada facilita manutenção e permite expansões futuras sem impacto em funcionalidades existentes.

### Próximos Passos Imediatos

1. **Aprovação do Plano:** Revisão detalhada com stakeholders e aprovação formal para início da implementação.

2. **Preparação do Ambiente:** Configuração de ambiente de desenvolvimento e teste idêntico ao produção. Criação de backup completo do sistema atual.

3. **Início da Fase 1:** Implementação do módulo UBO conforme cronograma detalhado, começando com análise de requisitos e design do modelo.

4. **Comunicação com Usuários:** Informação aos usuários sobre cronograma de melhorias e impactos esperados. Planejamento de sessões de treinamento para novas funcionalidades.

### Considerações para o Futuro

Este plano estabelece uma base sólida para expansões futuras do SIRIUS. A arquitetura modular implementada facilitará adição de novos módulos ou funcionalidades conforme necessidades do negócio evoluem. Integração com sistemas externos, APIs para clientes, ou funcionalidades de workflow podem ser consideradas em fases futuras.

O sistema de relatórios implementado pode ser expandido para incluir dashboards interativos ou integração com ferramentas de business intelligence. Funcionalidades de auditoria e compliance podem ser aprimoradas conforme requisitos regulatórios evoluem.

A implementação bem-sucedida deste plano posicionará o SIRIUS como uma plataforma robusta e escalável, capaz de suportar o crescimento e evolução contínua do negócio de corporate e financial services.

---

**Documento preparado por:** Manus AI  
**Data de criação:** 06 de Janeiro de 2025  
**Versão:** 1.0  
**Status:** Pronto para Implementação

