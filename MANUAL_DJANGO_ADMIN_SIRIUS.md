# Manual de Uso do Django Admin - Sistema Sirius

**Versão:** 1.0  
**Data:** Julho 2025  
**Autor:** Manus AI  
**Sistema:** Sirius Corporate Structure Management  

## Índice

1. [Introdução](#introdução)
2. [Acesso ao Sistema](#acesso-ao-sistema)
3. [Visão Geral da Interface](#visão-geral-da-interface)
4. [Módulo Corporate](#módulo-corporate)
5. [Módulo Sales](#módulo-sales)
6. [Módulo Estruturas (Legado)](#módulo-estruturas-legado)
7. [Funcionalidades Avançadas](#funcionalidades-avançadas)
8. [Fluxos de Trabalho Recomendados](#fluxos-de-trabalho-recomendados)
9. [Troubleshooting](#troubleshooting)
10. [Referências](#referências)

---

## Introdução

O Sistema Sirius é uma plataforma Django desenvolvida para gerenciar estruturas corporativas, beneficiários finais (UBOs), produtos comerciais e serviços relacionados ao planejamento patrimonial e estruturação empresarial. Este manual fornece instruções detalhadas para utilização da interface administrativa Django, destinada à equipe interna para gerenciamento completo dos dados do sistema.

O Django Admin do Sistema Sirius foi customizado para atender às necessidades específicas do negócio, incluindo gestão de jurisdições internacionais, classificações fiscais, alertas de compliance e estruturas hierárquicas complexas. A interface administrativa permite operações CRUD (Create, Read, Update, Delete) em todos os modelos do sistema, com funcionalidades avançadas como filtros, buscas, validações customizadas e relatórios integrados.

### Arquitetura do Sistema

O Sistema Sirius é estruturado em três aplicações Django principais:

**Corporate App**: Contém os modelos principais para gestão de estruturas corporativas, incluindo classificações fiscais, UBOs, regras de validação, alertas de jurisdição, sucessores e serviços. Esta é a aplicação central do sistema e onde a maior parte das operações administrativas são realizadas.

**Sales App**: Responsável pela gestão comercial, incluindo produtos, hierarquias de produtos, produtos personalizados e relacionamentos com UBOs. Esta aplicação permite a criação de ofertas comerciais baseadas nas estruturas disponíveis no sistema.

**Estruturas App (Legado)**: Mantida para compatibilidade com versões anteriores do sistema. Contém funcionalidades similares ao Corporate App, mas com estrutura de dados mais simples. Recomenda-se utilizar o Corporate App para novas implementações.

### Público-Alvo

Este manual é destinado a:
- Administradores do sistema
- Analistas de estruturas corporativas
- Equipe de compliance
- Consultores especializados
- Gerentes de produto
- Equipe de suporte técnico

### Pré-requisitos

Para utilizar efetivamente o Django Admin do Sistema Sirius, é necessário:
- Conhecimento básico de estruturas corporativas e planejamento patrimonial
- Familiaridade com interfaces web administrativas
- Compreensão de jurisdições internacionais e suas implicações fiscais
- Acesso autorizado ao sistema com permissões adequadas



## Acesso ao Sistema

### URL de Acesso

O Django Admin do Sistema Sirius está disponível através da URL:
```
https://[dominio-do-sistema]/admin/
```

Durante o desenvolvimento local, o acesso é realizado através de:
```
http://localhost:8000/admin/
```

### Autenticação

O sistema utiliza o sistema de autenticação padrão do Django com as seguintes características:

**Credenciais de Acesso**: O acesso é controlado através de usuários Django com permissões específicas. Cada usuário deve possuir credenciais válidas (username/email e senha) cadastradas no sistema.

**Níveis de Permissão**: O sistema implementa controle granular de permissões baseado no modelo de grupos e permissões do Django. As permissões são organizadas por aplicação e modelo, permitindo controle específico sobre operações de criação, leitura, atualização e exclusão.

**Grupos de Usuários**: Recomenda-se a criação de grupos específicos para diferentes funções:
- **Administradores**: Acesso completo a todos os módulos
- **Analistas de Estruturas**: Acesso aos módulos Corporate e Estruturas
- **Equipe Comercial**: Acesso ao módulo Sales e visualização de estruturas
- **Compliance**: Acesso a alertas, validações e relatórios
- **Consultores**: Acesso de leitura com permissões limitadas de edição

### Processo de Login

1. Acesse a URL do admin
2. Insira suas credenciais de usuário
3. Clique em "Log in"
4. Após autenticação bem-sucedida, você será redirecionado para o painel principal

### Recuperação de Senha

O sistema utiliza o mecanismo padrão de recuperação de senha do Django. Em caso de esquecimento da senha, entre em contato com o administrador do sistema para reset manual ou configuração de recuperação por email.

## Visão Geral da Interface

### Layout Principal

A interface do Django Admin do Sistema Sirius segue o padrão visual do Django com customizações específicas para o negócio. O layout é organizado em:

**Header**: Contém o nome do sistema, informações do usuário logado e opções de logout. O header também exibe links para a documentação e suporte quando disponíveis.

**Sidebar de Navegação**: Lista todas as aplicações disponíveis (Corporate, Sales, Estruturas App) com seus respectivos modelos. A navegação é organizada hierarquicamente, facilitando o acesso rápido às diferentes seções do sistema.

**Área Principal de Conteúdo**: Exibe as listas de registros, formulários de edição e páginas de detalhes. Esta área é responsiva e se adapta a diferentes tamanhos de tela.

**Footer**: Contém informações de versão e links para documentação técnica.

### Navegação Entre Módulos

O sistema está organizado em três módulos principais visíveis na sidebar:

**CORPORATE**: Módulo principal contendo:
- Tax Classifications (Classificações Fiscais)
- Structures (Estruturas)
- UBOs (Ultimate Beneficial Owners)
- Validation Rules (Regras de Validação)
- Jurisdiction Alerts (Alertas de Jurisdição)
- Successors (Sucessores)
- Services (Serviços)
- Service Activities (Atividades de Serviços)

**SALES**: Módulo comercial contendo:
- Products (Produtos)
- Product Hierarchies (Hierarquias de Produtos)
- Personalized Products (Produtos Personalizados)
- Personalized Product UBOs (UBOs de Produtos Personalizados)

**ESTRUTURAS_APP**: Módulo legado contendo:
- Estruturas (compatibilidade com versão anterior)

### Funcionalidades Comuns da Interface

**Listas de Registros**: Cada modelo apresenta uma lista paginada com colunas configuráveis, filtros laterais, campo de busca e ações em lote. As listas são otimizadas para exibir as informações mais relevantes de cada registro.

**Formulários de Edição**: Os formulários são organizados em fieldsets lógicos, facilitando a inserção e edição de dados. Campos relacionados são agrupados e validações são aplicadas em tempo real.

**Filtros e Busca**: Cada lista possui filtros específicos baseados nos campos mais utilizados para consulta. O sistema de busca permite localização rápida de registros através de múltiplos campos.

**Ações em Lote**: Operações que podem ser aplicadas a múltiplos registros simultaneamente, como ativação/desativação em massa ou exportação de dados.

### Convenções de Interface

**Status Ativo/Inativo**: A maioria dos modelos possui um campo "ativo" que controla a visibilidade do registro no sistema. Registros inativos são mantidos para histórico mas não aparecem em seleções padrão.

**Timestamps**: Todos os registros incluem campos de criação (created_at) e última atualização (updated_at) para auditoria e controle de versão.

**Relacionamentos**: Campos de relacionamento utilizam widgets específicos como select boxes, filtros horizontais ou inlines para facilitar a associação entre registros.

**Validações**: O sistema implementa validações tanto no frontend quanto no backend, exibindo mensagens claras em caso de erro ou inconsistência nos dados.


## Módulo Corporate

O módulo Corporate é o núcleo do Sistema Sirius, responsável por gerenciar todas as estruturas corporativas, beneficiários finais, classificações fiscais e serviços relacionados. Este módulo foi projetado para atender às complexidades do planejamento patrimonial internacional e estruturação empresarial.

### Tax Classifications (Classificações Fiscais)

As classificações fiscais são elementos fundamentais que definem o tratamento tributário das estruturas corporativas. O sistema suporta múltiplas classificações por estrutura, permitindo flexibilidade na configuração fiscal.

**Campos Principais:**
- **Name**: Tipo de classificação fiscal selecionado de uma lista predefinida
- **Description**: Descrição detalhada da classificação e suas implicações
- **Created At**: Data de criação do registro
- **Updated At**: Data da última modificação

**Classificações Disponíveis:**
- **Trust**: Estruturas fiduciárias tradicionais
- **Foreign Trust**: Trusts estrangeiros com implicações fiscais específicas
- **Fund**: Fundos de investimento e estruturas similares
- **US Corp**: Corporações americanas
- **Offshore Corp**: Corporações offshore
- **LLC Disregarded Entity**: LLCs tratadas como entidades desconsideradas
- **LLC Partnership**: LLCs com tratamento de partnership
- **Virtual Asset**: Estruturas para ativos virtuais e criptomoedas

**Funcionalidades da Interface:**
A lista de classificações fiscais exibe nome, descrição e data de criação em colunas organizadas. Os filtros laterais permitem busca por nome e data de criação, facilitando a localização de classificações específicas. O campo de busca permite pesquisa tanto no nome quanto na descrição da classificação.

**Processo de Cadastro:**
1. Acesse Corporate > Tax Classifications
2. Clique em "Add Tax Classification"
3. Selecione o tipo de classificação no campo Name
4. Insira uma descrição detalhada explicando as características e implicações fiscais
5. Salve o registro

**Relacionamentos:**
As classificações fiscais são utilizadas pelas estruturas através de relacionamento many-to-many, permitindo que uma estrutura tenha múltiplas classificações fiscais simultâneas.

### Structures (Estruturas)

As estruturas representam as entidades legais disponíveis no sistema, cada uma com características específicas de custo, implementação, privacidade e compliance. Este é o modelo mais complexo do sistema, contendo informações detalhadas sobre cada tipo de estrutura oferecida.

**Informações Básicas:**
- **Nome**: Denominação da estrutura (ex: "Delaware LLC", "Cayman Islands Company")
- **Tax Classifications**: Classificações fiscais aplicáveis (relacionamento many-to-many)
- **Descrição**: Descrição detalhada da estrutura, suas características e aplicações

**Informações de Jurisdição:**
- **Jurisdição**: País ou território principal (US, Bahamas, Brasil, Belize, BVI, Cayman, Panama)
- **Estado US**: Estado americano específico (quando jurisdição for US)
- **Estado BR**: Estado brasileiro específico (quando jurisdição for Brasil)

**Informações de Custo:**
- **Custo Base**: Valor inicial para implementação da estrutura em USD
- **Custo Manutenção**: Valor anual de manutenção em USD

**Scores e Avaliações:**
- **Privacidade Score**: Pontuação de 0 a 100 indicando o nível de privacidade oferecido
- **Compliance Score**: Pontuação de 0 a 100 indicando o nível de compliance necessário

**Detalhes de Implementação:**
- **Tempo Implementação**: Prazo em dias úteis para implementação completa
- **Documentos Necessários**: Lista detalhada da documentação requerida

**Status:**
- **Ativo**: Indica se a estrutura está disponível para comercialização

**Funcionalidades da Interface:**
A lista de estruturas apresenta uma visão consolidada com nome, classificações fiscais, jurisdição, custos e status. Os filtros laterais incluem classificações fiscais, jurisdição e status ativo, permitindo segmentação eficiente dos dados. O campo de busca abrange nome e descrição da estrutura.

O formulário de edição é organizado em fieldsets lógicos:
- **Basic Information**: Dados fundamentais da estrutura
- **Jurisdiction**: Informações de jurisdição e localização
- **Costs**: Valores financeiros
- **Scores**: Avaliações de privacidade e compliance
- **Implementation**: Detalhes de implementação
- **Status**: Controle de ativação

**Processo de Cadastro de Estrutura:**
1. Acesse Corporate > Structures
2. Clique em "Add Structure"
3. Preencha as informações básicas (nome, descrição)
4. Selecione as classificações fiscais aplicáveis usando o filtro horizontal
5. Configure a jurisdição e estados específicos se aplicável
6. Insira os custos base e de manutenção
7. Defina os scores de privacidade e compliance (0-100)
8. Especifique o tempo de implementação em dias úteis
9. Liste os documentos necessários
10. Defina o status ativo
11. Salve o registro

**Validações Importantes:**
- Estados US só devem ser preenchidos quando jurisdição for "US"
- Estados BR só devem ser preenchidos quando jurisdição for "BR"
- Scores devem estar entre 0 e 100
- Custos devem ser valores positivos
- Tempo de implementação deve ser um número inteiro positivo

### UBOs (Ultimate Beneficial Owners)

O módulo UBO gerencia informações sobre beneficiários finais, tanto pessoas físicas quanto jurídicas, incluindo dados pessoais, contatos, endereços e documentação de identificação.

**Informações Básicas:**
- **Nome**: Nome completo do UBO
- **Tipo Pessoa**: Física ou Jurídica

**Informações de Contato:**
- **Email**: Endereço de email principal
- **Telefone**: Número de telefone com código do país

**Informações de Endereço:**
- **Endereço**: Logradouro completo
- **Cidade**: Cidade de residência
- **Estado**: Estado ou província
- **País**: País de residência
- **CEP**: Código postal

**Documentação:**
- **Documento Identidade**: Número do documento principal
- **Tipo Documento**: Tipo de documento (passaporte, RG, etc.)

**Informações Adicionais:**
- **Nacionalidade**: Nacionalidade do UBO
- **Data Nascimento**: Data de nascimento (para pessoas físicas)

**Status:**
- **Ativo**: Controla se o UBO está ativo no sistema

**Funcionalidades da Interface:**
A lista de UBOs exibe nome, tipo de pessoa, email, telefone, país e status em formato tabular. Os filtros incluem tipo de pessoa, país, status ativo e data de criação. A busca abrange nome, email e documento de identidade.

O formulário é organizado em seções lógicas:
- **Basic Information**: Nome e tipo de pessoa
- **Contact Information**: Email e telefone
- **Address Information**: Endereço completo
- **Identification**: Documentação
- **Additional Information**: Nacionalidade e data de nascimento
- **Status**: Controle de ativação

**Processo de Cadastro de UBO:**
1. Acesse Corporate > UBOs
2. Clique em "Add UBO"
3. Insira o nome completo
4. Selecione o tipo de pessoa (Física/Jurídica)
5. Preencha as informações de contato
6. Complete o endereço
7. Insira a documentação de identificação
8. Adicione informações complementares
9. Defina o status ativo
10. Salve o registro

### Validation Rules (Regras de Validação)

As regras de validação definem relacionamentos e restrições entre diferentes estruturas, permitindo controle de compatibilidade e compliance automático.

**Campos Principais:**
- **Estrutura A**: Primeira estrutura do relacionamento
- **Estrutura B**: Segunda estrutura do relacionamento
- **Tipo Relacionamento**: Natureza do relacionamento entre as estruturas
- **Severidade**: Nível de importância da regra
- **Descrição**: Explicação detalhada da regra
- **Ativo**: Status da regra

**Funcionalidades da Interface:**
A lista exibe as estruturas relacionadas, tipo de relacionamento, severidade e status. Os filtros incluem tipo de relacionamento, severidade e status ativo. A busca abrange nomes das estruturas e descrição da regra.

**Processo de Configuração:**
1. Acesse Corporate > Validation Rules
2. Clique em "Add Validation Rule"
3. Selecione a primeira estrutura (Estrutura A)
4. Selecione a segunda estrutura (Estrutura B)
5. Defina o tipo de relacionamento
6. Configure a severidade
7. Descreva a regra detalhadamente
8. Ative a regra
9. Salve o registro

### Jurisdiction Alerts (Alertas de Jurisdição)

O sistema de alertas gerencia notificações e deadlines específicos por jurisdição, essencial para compliance e manutenção de estruturas internacionais.

**Informações Básicas:**
- **Título**: Nome do alerta
- **Descrição**: Descrição detalhada do alerta
- **Jurisdição**: Jurisdição aplicável
- **Tipo Alerta**: Categoria do alerta

**Aplicabilidade:**
- **Estruturas Aplicáveis**: Estruturas afetadas pelo alerta (many-to-many)
- **UBOs Aplicáveis**: UBOs afetados pelo alerta (many-to-many)

**Configuração de Deadlines:**
- **Deadline Type**: Tipo de deadline (único ou recorrente)
- **Single Deadline**: Data específica para deadlines únicos
- **Recurrence Pattern**: Padrão de recorrência
- **Next Deadline**: Próximo deadline calculado
- **Last Completed**: Data da última conclusão

**Configurações Avançadas:**
- **Advance Notice Days**: Dias de antecedência para notificação
- **Auto Calculate Next**: Cálculo automático do próximo deadline
- **Custom Recurrence Config**: Configuração customizada de recorrência

**Prioridade e Status:**
- **Prioridade**: Nível de prioridade do alerta
- **Ativo**: Status do alerta

**Funcionalidades da Interface:**
A lista apresenta título, jurisdição, tipo de alerta, tipo de deadline, próximo deadline, prioridade e status. Os filtros incluem jurisdição, tipo de alerta, tipo de deadline, prioridade e status ativo. A busca abrange título e descrição.

O formulário utiliza filtros horizontais para seleção de estruturas e UBOs aplicáveis, facilitando a configuração de alertas que afetam múltiplas entidades.

**Processo de Configuração de Alerta:**
1. Acesse Corporate > Jurisdiction Alerts
2. Clique em "Add Jurisdiction Alert"
3. Insira título e descrição
4. Selecione jurisdição e tipo de alerta
5. Configure estruturas e UBOs aplicáveis usando filtros horizontais
6. Defina o tipo de deadline e configurações específicas
7. Configure notificações antecipadas
8. Defina prioridade e status
9. Salve o registro

### Successors (Sucessores)

O módulo de sucessores gerencia a definição de sucessão entre UBOs, incluindo percentuais e status de efetivação.

**Campos Principais:**
- **UBO Proprietário**: UBO atual
- **UBO Sucessor**: UBO que receberá a sucessão
- **Percentual**: Percentual da sucessão
- **Data Definição**: Data em que a sucessão foi definida
- **Ativo**: Status da definição de sucessão
- **Efetivado**: Indica se a sucessão foi efetivada

**Funcionalidades da Interface:**
A lista exibe UBO proprietário, UBO sucessor, percentual, status ativo e efetivado. Os filtros incluem status ativo, efetivado e data de criação. A busca abrange nomes dos UBOs envolvidos.

**Processo de Configuração:**
1. Acesse Corporate > Successors
2. Clique em "Add Successor"
3. Selecione o UBO proprietário
4. Selecione o UBO sucessor
5. Defina o percentual de sucessão
6. Configure status ativo e efetivado
7. Salve o registro

### Services (Serviços)

O módulo de serviços gerencia os serviços oferecidos pela empresa, incluindo custos, durações e estruturas associadas.

**Informações Básicas:**
- **Service Name**: Nome do serviço
- **Description**: Descrição detalhada
- **Service Type**: Tipo de serviço

**Custo e Duração:**
- **Cost**: Custo do serviço
- **Estimated Duration**: Duração estimada

**Associações:**
- **Associated Structure**: Estrutura associada ao serviço

**Configuração:**
- **Requirements**: Requisitos para o serviço
- **Deliverables**: Entregáveis do serviço

**Status:**
- **Status**: Status atual do serviço
- **Ativo**: Controle de ativação

**Funcionalidades da Interface:**
A lista exibe nome do serviço, tipo, status, estrutura associada, custo e status ativo. Os filtros incluem tipo de serviço, status e ativo. A busca abrange nome e descrição do serviço.

O formulário inclui um inline para Service Activities, permitindo gerenciar atividades relacionadas diretamente na tela do serviço.

### Service Activities (Atividades de Serviços)

As atividades de serviços representam tarefas específicas dentro de um serviço, com controle de prazos, responsáveis e prioridades.

**Campos Principais:**
- **Activity Title**: Título da atividade
- **Service**: Serviço relacionado
- **Activity Description**: Descrição da atividade
- **Status**: Status atual da atividade
- **Priority**: Prioridade da atividade
- **Start Date**: Data de início
- **Due Date**: Data de vencimento
- **Responsible Person**: Pessoa responsável
- **Ativo**: Status de ativação

**Funcionalidades da Interface:**
A lista exibe título da atividade, serviço, status, prioridade, datas e responsável. Os filtros incluem status, prioridade, tipo de serviço e ativo. A busca abrange título, descrição, nome do serviço e responsável.

As atividades podem ser gerenciadas tanto individualmente quanto através do inline no formulário de serviços, proporcionando flexibilidade na gestão.


## Módulo Sales

O módulo Sales é responsável pela gestão comercial do Sistema Sirius, incluindo produtos, hierarquias de estruturas e personalizações para clientes específicos. Este módulo permite a criação de ofertas comerciais baseadas nas estruturas disponíveis no sistema.

### Products (Produtos)

Os produtos representam ofertas comerciais que combinam múltiplas estruturas em pacotes organizados hierarquicamente. Cada produto pode ter custos automáticos (calculados) ou manuais (fixos).

**Informações Básicas:**
- **Nome**: Nome interno do produto
- **Commercial Name**: Nome comercial para apresentação ao cliente
- **Complexidade Template**: Nível de complexidade do produto
- **Descrição**: Descrição detalhada do produto e suas características

**Detalhes Comerciais:**
- **Master Agreement URL**: Link para o contrato principal
- **Público Alvo**: Descrição do público-alvo do produto
- **Casos Uso**: Casos de uso típicos do produto

**Configuração de Custos:**
- **Custo Automático**: Custo calculado automaticamente baseado nas estruturas
- **Custo Manual**: Custo fixo definido manualmente

**Implementação:**
- **Tempo Total Implementação**: Tempo total estimado para implementação

**Status:**
- **Ativo**: Controla se o produto está disponível para venda
- **Uso Count**: Contador de quantas vezes o produto foi utilizado

**Funcionalidades da Interface:**
A lista de produtos exibe nome, nome comercial, complexidade template, contador de uso e status ativo. Os filtros incluem complexidade template, status ativo e data de criação. A busca abrange nome, nome comercial e descrição.

O formulário inclui um inline para Product Hierarchy, permitindo definir a sequência de estruturas que compõem o produto diretamente na tela de edição.

**Processo de Cadastro de Produto:**
1. Acesse Sales > Products
2. Clique em "Add Product"
3. Insira nome interno e nome comercial
4. Selecione a complexidade template
5. Preencha a descrição detalhada
6. Configure detalhes comerciais (URL do contrato, público-alvo, casos de uso)
7. Defina custos (automático ou manual)
8. Especifique tempo de implementação
9. Configure hierarquia de estruturas no inline
10. Ative o produto
11. Salve o registro

### Product Hierarchy (Hierarquia de Produtos)

A hierarquia de produtos define a sequência e configuração das estruturas que compõem um produto comercial.

**Campos Principais:**
- **Product**: Produto ao qual a hierarquia pertence
- **Structure**: Estrutura incluída na hierarquia
- **Order**: Ordem da estrutura na sequência de implementação
- **Custom Cost**: Custo customizado para esta estrutura no contexto do produto
- **Notes**: Observações específicas sobre a estrutura neste produto

**Funcionalidades da Interface:**
A lista exibe produto, estrutura, ordem e custo customizado. Os filtros incluem produto, estrutura e data de criação. A busca abrange nome do produto e nome da estrutura.

A hierarquia é gerenciada principalmente através do inline no formulário de produtos, mas também pode ser editada individualmente quando necessário.

**Processo de Configuração:**
1. No formulário de produto, utilize o inline Product Hierarchy
2. Para cada estrutura do produto:
   - Selecione a estrutura
   - Defina a ordem de implementação
   - Configure custo customizado se necessário
   - Adicione observações específicas
3. Salve o produto com sua hierarquia completa

### Personalized Products (Produtos Personalizados)

Os produtos personalizados são versões customizadas de produtos base ou estruturas, adaptadas para necessidades específicas de clientes.

**Informações Básicas:**
- **Nome**: Nome do produto personalizado
- **Descrição**: Descrição das personalizações aplicadas
- **Status**: Status atual do produto personalizado

**Configuração Base:**
- **Base Product**: Produto base utilizado como referência
- **Base Structure**: Estrutura base (alternativa ao produto base)

**Versionamento:**
- **Version Number**: Número da versão do produto personalizado
- **Parent Version**: Versão pai (para controle de evolução)

**Personalização:**
- **Configuração Personalizada**: Detalhes das customizações aplicadas
- **Custo Personalizado**: Custo específico do produto personalizado
- **Observações**: Observações adicionais sobre a personalização

**Status:**
- **Ativo**: Controla se o produto personalizado está ativo

**Funcionalidades da Interface:**
A lista exibe nome, tipo base, status, número da versão, percentual total de UBOs e status ativo. Os filtros incluem status, número da versão, ativo e data de criação. A busca abrange nome, descrição, nome do produto base e nome da estrutura base.

O formulário inclui um inline para Personalized Product UBO, permitindo associar UBOs específicos ao produto personalizado com seus respectivos percentuais.

**Métodos Customizados:**
- **get_base_type()**: Retorna se o produto é baseado em produto ou estrutura
- **get_total_percentage()**: Calcula o percentual total dos UBOs associados

**Processo de Criação de Produto Personalizado:**
1. Acesse Sales > Personalized Products
2. Clique em "Add Personalized Product"
3. Insira nome e descrição das personalizações
4. Selecione produto base OU estrutura base
5. Configure versionamento
6. Detalhe as personalizações aplicadas
7. Defina custo personalizado
8. Associe UBOs com percentuais no inline
9. Ative o produto
10. Salve o registro

### Personalized Product UBO

Este modelo gerencia a associação entre produtos personalizados e UBOs, incluindo percentuais de participação.

**Campos Principais:**
- **Personalized Product**: Produto personalizado relacionado
- **UBO**: UBO associado ao produto
- **Percentage**: Percentual de participação do UBO

**Funcionalidades da Interface:**
A lista exibe produto personalizado, UBO e percentual. Os filtros incluem produto personalizado, UBO e data de criação. A busca abrange nome do produto personalizado e nome do UBO.

A gestão é realizada principalmente através do inline no formulário de produtos personalizados, mas registros individuais podem ser editados quando necessário.

**Validações:**
- O percentual deve ser um valor válido entre 0 e 100
- A soma dos percentuais de todos os UBOs de um produto deve ser monitorada

## Módulo Estruturas (Legado)

O módulo Estruturas App é mantido para compatibilidade com versões anteriores do Sistema Sirius. Embora funcional, recomenda-se utilizar o módulo Corporate para novas implementações, pois oferece funcionalidades mais avançadas e melhor organização dos dados.

### Estrutura (Modelo Legado)

O modelo Estrutura contém funcionalidades similares ao modelo Structure do módulo Corporate, mas com estrutura de dados mais simples e menos flexibilidade.

**Campos Principais:**
- **Nome**: Nome da estrutura
- **Tipo**: Tipo de estrutura legal
- **Descrição**: Descrição detalhada
- **Jurisdição**: Jurisdição principal
- **Estado US/BR**: Estados específicos quando aplicável
- **Custo Base/Manutenção**: Custos associados
- **Tempo Implementação**: Prazo de implementação
- **Complexidade**: Nível de complexidade (1-5)
- **Documentação Necessária**: Lista de documentos requeridos

**Campos de Impacto:**
- **Impacto Tributário EUA/Brasil/Outros**: Descrição dos impactos fiscais
- **Nível Confidencialidade**: Nível de privacidade oferecido
- **Proteção Patrimonial**: Nível de proteção patrimonial
- **Impacto Privacidade**: Descrição do impacto na privacidade

**Campos Operacionais:**
- **Facilidade Banking**: Facilidade para abertura de contas bancárias
- **URL Documentos**: Link para documentação adicional
- **Formulários Obrigatórios**: Formulários requeridos por jurisdição

**Funcionalidades Específicas da Interface:**

**Formatação Customizada**: O admin implementa métodos customizados para formatação:
- **custo_base_formatted()**: Formata o custo base como moeda USD
- **custo_manutencao_formatted()**: Formata o custo de manutenção como moeda USD
- **complexidade_display()**: Exibe a complexidade com codificação por cores

**Organização por Fieldsets**: O formulário é organizado em seções colapsáveis:
- **Basic Information**: Informações fundamentais
- **Jurisdiction**: Dados de jurisdição
- **Cost Information**: Informações de custo (colapsável)
- **Implementation Details**: Detalhes de implementação (colapsável)
- **Tax Impact**: Impactos tributários (colapsável)
- **Privacy and Protection**: Privacidade e proteção (colapsável)
- **Operational**: Aspectos operacionais (colapsável)
- **Compliance**: Conformidade (colapsável)
- **Metadata**: Metadados do sistema (colapsável)

**Campos Readonly**: Os campos created_at e updated_at são somente leitura para preservar a integridade dos metadados.

**Codificação por Cores da Complexidade**:
- **Nível 1**: Verde (#28a745) - Baixa complexidade
- **Nível 2**: Cinza (#6c757d) - Complexidade baixa-média
- **Nível 3**: Amarelo (#ffc107) - Complexidade média
- **Nível 4**: Laranja (#fd7e14) - Complexidade média-alta
- **Nível 5**: Vermelho (#dc3545) - Alta complexidade

**Processo de Migração:**
Para organizações utilizando o módulo legado, recomenda-se:
1. Avaliar dados existentes no modelo Estrutura
2. Mapear campos para o novo modelo Structure do módulo Corporate
3. Migrar dados preservando relacionamentos
4. Atualizar processos para utilizar o novo módulo
5. Manter o módulo legado temporariamente para transição suave

**Limitações do Módulo Legado:**
- Estrutura de dados menos flexível
- Ausência de classificações fiscais múltiplas
- Menor integração com outros módulos
- Funcionalidades de alerta e validação limitadas
- Interface menos otimizada para operações em lote

**Compatibilidade:**
O módulo legado permanece funcional e pode ser utilizado em paralelo com o módulo Corporate durante períodos de transição. No entanto, novos desenvolvimentos e funcionalidades são implementados exclusivamente no módulo Corporate.


## Funcionalidades Avançadas

O Django Admin do Sistema Sirius implementa diversas funcionalidades avançadas que otimizam a experiência do usuário e aumentam a eficiência operacional.

### Inlines (Edição em Linha)

Os inlines permitem editar registros relacionados diretamente na tela do registro principal, eliminando a necessidade de navegação entre telas.

**ServiceActivityInline**: Disponível no formulário de Services, permite gerenciar atividades de serviço diretamente na tela do serviço. Os campos disponíveis incluem título da atividade, status, prioridade, datas de início e vencimento, e pessoa responsável. A ordenação padrão é por data de início decrescente.

**ProductHierarchyInline**: Integrado ao formulário de Products, facilita a definição da sequência de estruturas que compõem um produto. Permite configurar estrutura, ordem, custo customizado e observações específicas. A ordenação é por campo order, mantendo a sequência lógica de implementação.

**PersonalizedProductUBOInline**: Disponível no formulário de Personalized Products, gerencia a associação de UBOs com seus respectivos percentuais de participação. Essencial para produtos personalizados que requerem distribuição específica entre beneficiários.

**Configuração de Inlines**: Todos os inlines são configurados com extra=1, adicionando automaticamente uma linha em branco para novos registros. Os campos são otimizados para exibir apenas informações essenciais, mantendo a interface limpa e funcional.

### Fieldsets Organizados

A organização em fieldsets melhora significativamente a usabilidade dos formulários, agrupando campos relacionados logicamente.

**Padrão de Organização**: Os fieldsets seguem um padrão consistente em todo o sistema:
- **Basic Information**: Campos fundamentais sempre visíveis
- **Categoria Específica**: Agrupamentos por função (Jurisdiction, Costs, etc.)
- **Advanced Settings**: Configurações avançadas frequentemente colapsáveis
- **Status**: Controles de ativação sempre ao final

**Fieldsets Colapsáveis**: Seções menos utilizadas são configuradas como colapsáveis usando a classe CSS 'collapse', reduzindo a sobrecarga visual e focando nos campos mais importantes.

**Descrições Contextuais**: Fieldsets incluem descrições quando necessário, como "Select state only if jurisdiction is US or Brazil" no fieldset de Jurisdiction das estruturas.

### Filtros Horizontais

Os filtros horizontais são utilizados para relacionamentos many-to-many, proporcionando interface intuitiva para seleção múltipla.

**TaxClassifications em Structures**: Permite seleção múltipla de classificações fiscais para cada estrutura, com interface de arrastar e soltar entre listas "Available" e "Chosen".

**Estruturas e UBOs em JurisdictionAlerts**: Facilita a aplicação de alertas a múltiplas estruturas e UBOs simultaneamente, essencial para alertas que afetam várias entidades.

**Funcionalidades**: Os filtros horizontais incluem busca integrada, permitindo localização rápida de itens em listas extensas. A interface é responsiva e funciona adequadamente em diferentes tamanhos de tela.

### Métodos Customizados de Display

O sistema implementa métodos customizados para melhorar a apresentação de dados nas listas administrativas.

**Formatação de Moeda**: Métodos como custo_base_formatted() e custo_manutencao_formatted() formatam valores monetários com separadores de milhares e símbolo de moeda, melhorando a legibilidade.

**Display com Cores**: O método complexidade_display() utiliza format_html() para aplicar cores específicas baseadas no nível de complexidade, proporcionando identificação visual rápida.

**Concatenação de Informações**: Métodos como get_full_jurisdiction_display() combinam múltiplos campos para criar displays informativos e concisos.

**Cálculos Dinâmicos**: Métodos como get_total_percentage() realizam cálculos em tempo real para exibir informações derivadas.

**Configuração de Métodos**: Todos os métodos customizados incluem:
- **short_description**: Título da coluna na lista
- **admin_order_field**: Campo para ordenação quando aplicável
- **boolean**: Indicação se o campo é booleano para ícones apropriados

### Campos Readonly

Campos readonly preservam a integridade de dados críticos enquanto mantêm visibilidade para auditoria.

**Timestamps**: Campos created_at e updated_at são configurados como readonly para preservar metadados de auditoria. Estes campos são agrupados em fieldsets específicos, frequentemente colapsáveis.

**Campos Calculados**: Campos que são calculados automaticamente pelo sistema são configurados como readonly para evitar inconsistências.

**Metadados do Sistema**: Informações geradas automaticamente pelo sistema são protegidas contra edição acidental.

### Validações Customizadas

O sistema implementa validações tanto no nível do modelo quanto no admin para garantir integridade dos dados.

**Validações de Relacionamento**: ValidationRules implementa validações para evitar relacionamentos inconsistentes entre estruturas.

**Validações de Percentual**: Sucessores e PersonalizedProductUBO incluem validações para garantir que percentuais estejam dentro de faixas válidas.

**Validações de Jurisdição**: Estruturas incluem validações para garantir que estados sejam preenchidos apenas quando a jurisdição correspondente for selecionada.

**Validações de Data**: JurisdictionAlerts implementa validações para garantir consistência entre diferentes tipos de deadline e suas configurações.

### Ações em Lote

Embora não explicitamente customizadas no código analisado, o sistema herda as ações padrão do Django Admin, incluindo exclusão em lote e possibilidade de implementação de ações customizadas.

**Ações Padrão**: Todas as listas incluem a ação de exclusão em lote, permitindo operações eficientes em múltiplos registros.

**Potencial para Ações Customizadas**: A arquitetura permite implementação de ações específicas como:
- Ativação/desativação em lote
- Exportação de dados selecionados
- Aplicação de alterações em massa
- Geração de relatórios para registros selecionados

## Fluxos de Trabalho Recomendados

Esta seção apresenta fluxos de trabalho otimizados para operações comuns no Sistema Sirius, baseados nas funcionalidades disponíveis e melhores práticas identificadas.

### Fluxo de Cadastro de Nova Estrutura

**Preparação**:
1. Colete todas as informações necessárias sobre a estrutura
2. Identifique as classificações fiscais aplicáveis
3. Pesquise custos atualizados e tempos de implementação
4. Prepare documentação de referência

**Execução**:
1. Acesse Corporate > Tax Classifications e verifique se as classificações necessárias existem
2. Se necessário, cadastre novas classificações fiscais
3. Acesse Corporate > Structures e clique em "Add Structure"
4. Preencha informações básicas (nome, descrição)
5. Selecione classificações fiscais usando filtro horizontal
6. Configure jurisdição e estados específicos
7. Insira custos e scores de avaliação
8. Defina tempo de implementação e documentação necessária
9. Ative a estrutura
10. Salve e revise os dados inseridos

**Validação**:
1. Verifique se a estrutura aparece corretamente nas listas
2. Teste filtros e busca para localizar a nova estrutura
3. Confirme relacionamentos com classificações fiscais
4. Valide cálculos de custos se aplicável

### Fluxo de Criação de Produto Comercial

**Planejamento**:
1. Defina o público-alvo e casos de uso do produto
2. Selecione estruturas que comporão o produto
3. Determine a sequência de implementação
4. Calcule custos e tempos totais

**Implementação**:
1. Acesse Sales > Products e clique em "Add Product"
2. Configure informações básicas e comerciais
3. No inline Product Hierarchy, adicione estruturas na ordem correta
4. Configure custos customizados se necessário
5. Adicione observações específicas para cada estrutura
6. Defina tempo total de implementação
7. Ative o produto
8. Salve e teste a configuração

**Personalização (se necessário)**:
1. Acesse Sales > Personalized Products
2. Crie versão personalizada baseada no produto
3. Configure UBOs e percentuais no inline
4. Documente personalizações aplicadas
5. Valide soma de percentuais dos UBOs

### Fluxo de Gestão de Alertas de Compliance

**Configuração Inicial**:
1. Identifique requisitos de compliance por jurisdição
2. Determine estruturas e UBOs afetados
3. Configure padrões de recorrência apropriados
4. Defina prioridades e antecedências

**Implementação**:
1. Acesse Corporate > Jurisdiction Alerts
2. Crie alerta com título e descrição claros
3. Selecione jurisdição e tipo de alerta
4. Configure estruturas e UBOs aplicáveis usando filtros horizontais
5. Defina configurações de deadline (único ou recorrente)
6. Configure notificações antecipadas
7. Defina prioridade apropriada
8. Ative o alerta

**Monitoramento**:
1. Revise regularmente alertas próximos ao vencimento
2. Atualize status de conclusão quando aplicável
3. Monitore cálculo automático de próximos deadlines
4. Ajuste configurações conforme necessário

### Fluxo de Gestão de UBOs e Sucessão

**Cadastro de UBO**:
1. Colete documentação completa do UBO
2. Verifique se UBO já existe no sistema
3. Cadastre informações pessoais e de contato
4. Configure documentação de identificação
5. Valide dados inseridos

**Configuração de Sucessão**:
1. Identifique relacionamentos de sucessão
2. Acesse Corporate > Successors
3. Configure UBO proprietário e sucessor
4. Defina percentuais apropriados
5. Documente data de definição
6. Monitore status de efetivação

**Manutenção**:
1. Atualize informações de contato regularmente
2. Revise relacionamentos de sucessão periodicamente
3. Mantenha documentação atualizada
4. Monitore status ativo dos UBOs

### Fluxo de Gestão de Serviços

**Planejamento de Serviço**:
1. Defina escopo e entregáveis do serviço
2. Identifique estruturas associadas
3. Estime custos e duração
4. Planeje atividades necessárias

**Configuração**:
1. Acesse Corporate > Services
2. Configure informações básicas do serviço
3. Associe estrutura relacionada
4. Defina custos e duração estimada
5. No inline Service Activities, adicione atividades específicas
6. Configure responsáveis e prazos para cada atividade
7. Defina prioridades apropriadas

**Execução e Monitoramento**:
1. Monitore progresso das atividades
2. Atualize status conforme execução
3. Ajuste prazos quando necessário
4. Documente conclusões e resultados

## Troubleshooting

Esta seção aborda problemas comuns e suas soluções no uso do Django Admin do Sistema Sirius.

### Problemas de Acesso e Autenticação

**Problema**: Não consigo acessar o admin
**Soluções**:
1. Verifique se a URL está correta (/admin/)
2. Confirme se o usuário possui permissões de staff
3. Verifique se o usuário está ativo no sistema
4. Confirme credenciais de login
5. Verifique logs do servidor para erros específicos

**Problema**: Usuário logado mas sem acesso a módulos específicos
**Soluções**:
1. Verifique permissões do usuário ou grupo
2. Confirme se o usuário pertence aos grupos apropriados
3. Verifique se os modelos estão registrados no admin
4. Confirme configurações de permissão por modelo

### Problemas de Performance

**Problema**: Listas carregam lentamente
**Soluções**:
1. Verifique se há muitos registros na lista
2. Utilize filtros para reduzir conjunto de dados
3. Considere paginação adequada
4. Verifique queries N+1 em relacionamentos
5. Otimize métodos customizados de display

**Problema**: Formulários demoram para carregar
**Soluções**:
1. Verifique relacionamentos complexos
2. Otimize queries em filtros horizontais
3. Considere lazy loading para campos pesados
4. Revise validações customizadas

### Problemas de Dados

**Problema**: Erro ao salvar estrutura com estado
**Soluções**:
1. Verifique se estado corresponde à jurisdição selecionada
2. Confirme se estado é obrigatório para a jurisdição
3. Valide formato do código do estado
4. Verifique validações customizadas do modelo

**Problema**: Percentuais de UBO não somam 100%
**Soluções**:
1. Revise todos os UBOs associados ao produto
2. Verifique cálculos de percentual
3. Confirme se todos os UBOs estão ativos
4. Valide entrada de dados numéricos

**Problema**: Alertas não calculam próximo deadline
**Soluções**:
1. Verifique configuração de recorrência
2. Confirme se auto_calculate_next está ativo
3. Valide padrão de recorrência configurado
4. Verifique se last_completed está preenchido

### Problemas de Interface

**Problema**: Filtros horizontais não funcionam
**Soluções**:
1. Verifique se JavaScript está habilitado
2. Confirme se arquivos estáticos estão carregando
3. Verifique console do navegador para erros
4. Teste em navegador diferente

**Problema**: Inlines não aparecem
**Soluções**:
1. Verifique se relacionamento está configurado corretamente
2. Confirme se inline está registrado no admin
3. Verifique permissões para o modelo relacionado
4. Confirme se há registros relacionados

**Problema**: Formatação customizada não aparece
**Soluções**:
1. Verifique se método está definido corretamente
2. Confirme se método está listado em list_display
3. Valide se short_description está configurado
4. Verifique se há erros no método customizado

### Problemas de Validação

**Problema**: Validações customizadas não funcionam
**Soluções**:
1. Verifique se validação está no método clean() do modelo
2. Confirme se validação está sendo chamada
3. Valide lógica da validação
4. Teste validação isoladamente

**Problema**: Relacionamentos inválidos são aceitos
**Soluções**:
1. Verifique ValidationRules configuradas
2. Confirme se regras estão ativas
3. Valide lógica das regras de validação
4. Teste cenários específicos

### Problemas de Busca e Filtros

**Problema**: Busca não encontra registros existentes
**Soluções**:
1. Verifique se campos estão em search_fields
2. Confirme se busca é case-sensitive
3. Teste termos de busca diferentes
4. Verifique se registros estão ativos

**Problema**: Filtros não mostram opções esperadas
**Soluções**:
1. Verifique se há dados para filtrar
2. Confirme se campos estão em list_filter
3. Valide se relacionamentos estão corretos
4. Verifique permissões de visualização

### Procedimentos de Diagnóstico

**Verificação de Logs**:
1. Acesse logs do Django para erros específicos
2. Verifique logs do servidor web
3. Monitore logs de banco de dados
4. Analise logs de JavaScript no navegador

**Teste de Funcionalidades**:
1. Teste em ambiente de desenvolvimento
2. Valide com dados de teste
3. Confirme em navegadores diferentes
4. Teste com usuários de permissões diferentes

**Backup e Recuperação**:
1. Mantenha backups regulares do banco de dados
2. Documente alterações antes de implementar
3. Teste restaurações em ambiente separado
4. Mantenha histórico de versões do código

### Contatos para Suporte

Para problemas não resolvidos com este manual:
1. Consulte documentação técnica do Django
2. Verifique logs detalhados do sistema
3. Entre em contato com a equipe de desenvolvimento
4. Documente problemas para futuras referências


## Referências

### Documentação Técnica

**Django Admin Documentation**: A documentação oficial do Django Admin fornece informações detalhadas sobre funcionalidades padrão, customizações e melhores práticas. Disponível em: https://docs.djangoproject.com/en/4.2/ref/contrib/admin/

**Django Models Documentation**: Documentação completa sobre modelos Django, relacionamentos e validações. Essencial para compreender a estrutura de dados do Sistema Sirius. Disponível em: https://docs.djangoproject.com/en/4.2/topics/db/models/

**Django Forms Documentation**: Informações sobre formulários Django, fieldsets e widgets utilizados no admin. Disponível em: https://docs.djangoproject.com/en/4.2/topics/forms/

### Arquivos de Referência do Sistema

**Settings.py**: Configurações principais do Django incluindo apps instalados, middleware e configurações de banco de dados. Localização: `sirius_project/settings.py`

**URLs.py**: Configuração de rotas do sistema incluindo acesso ao admin. Localização: `sirius_project/urls.py`

**Models.py**: Definições de modelos para cada aplicação:
- Corporate: `corporate/models.py`
- Sales: `sales/models.py`
- Estruturas: `estruturas_app/models.py`

**Admin.py**: Configurações do Django Admin para cada aplicação:
- Corporate: `corporate/admin.py`
- Sales: `sales/admin.py`
- Estruturas: `estruturas_app/admin.py`

### Recursos Adicionais

**Requirements.txt**: Lista de dependências do projeto incluindo versões específicas. Localização: `requirements.txt`

**README.md**: Documentação geral do projeto com instruções de instalação e configuração. Localização: `README.md`

**ESPECIFICACOES_TECNICAS.md**: Especificações técnicas detalhadas do sistema. Localização: `ESPECIFICACOES_TECNICAS.md`

**USER_MANUAL.md**: Manual do usuário para interface frontend. Localização: `USER_MANUAL.md`

### Contatos e Suporte

**Equipe de Desenvolvimento**: Para questões técnicas relacionadas ao código e arquitetura do sistema.

**Administrador do Sistema**: Para questões de acesso, permissões e configurações de usuário.

**Equipe de Compliance**: Para questões relacionadas a alertas de jurisdição, validações e requisitos regulatórios.

**Suporte Técnico**: Para problemas operacionais e troubleshooting geral.

---

## Conclusão

Este manual fornece uma visão abrangente do Django Admin do Sistema Sirius, cobrindo desde funcionalidades básicas até recursos avançados e fluxos de trabalho otimizados. O sistema foi projetado para atender às complexidades do planejamento patrimonial internacional e estruturação empresarial, oferecendo ferramentas robustas para gestão de estruturas corporativas, UBOs, produtos comerciais e compliance.

A interface administrativa permite operações eficientes através de funcionalidades como inlines, filtros horizontais, métodos customizados de display e validações automáticas. Os fluxos de trabalho recomendados neste manual foram desenvolvidos com base na análise das funcionalidades disponíveis e melhores práticas identificadas no código.

Para maximizar a eficiência no uso do sistema, recomenda-se:
- Familiarização com os três módulos principais (Corporate, Sales, Estruturas)
- Utilização dos fluxos de trabalho documentados
- Aproveitamento das funcionalidades avançadas como inlines e filtros
- Monitoramento regular de alertas de compliance
- Manutenção adequada de dados de UBOs e estruturas

Este manual deve ser atualizado conforme evoluções do sistema e feedback dos usuários. A documentação técnica complementar disponível no repositório fornece informações adicionais sobre aspectos específicos do desenvolvimento e manutenção do sistema.

**Versão do Manual**: 1.0  
**Data de Criação**: Julho 2025  
**Próxima Revisão**: A ser definida conforme atualizações do sistema

