# Plano de Refatoração e Melhoria de Usabilidade do Frontend Sirius

**Autor:** Engenheiro de Frontend e Especialista em Usabilidade  
**Data:** 06 de Julho de 2025  
**Foco:** Refatoração da arquitetura frontend e aprimoramento radical da usabilidade da interface de Canvas para desktop.

---

## 1. Análise do Estado Atual e Diagnóstico

Após uma análise da base de código existente (`static/`, `templates/`, `frontend-new/`) e dos artefatos de documentação, foram identificados os seguintes problemas críticos que comprometem a manutenibilidade, a performance e, principalmente, a experiência do usuário.

### 1.1. Problemas Arquiteturais e de Código

*   **Arquitetura Fragmentada:** Múltiplas implementações de canvas (`canvas-clean.js`, `canvas-advanced.js`, etc.) e templates HTML (`canvas.html`, `canvas_clean.html`) coexistem, gerando duplicação de código, inconsistências e dificultando a manutenção.
*   **Dependências Instáveis:** O uso de Vue.js e Tailwind CSS via CDN em vez de um gerenciador de pacotes (como npm) torna a aplicação vulnerável a falhas de rede, dificulta o controle de versão e impede otimizações de build (como *tree-shaking*).
*   **Falta de um Sistema de Build Moderno:** A ausência de uma ferramenta de build consolidada (como Vite ou Webpack) para os arquivos legados resulta em código não otimizado, bundles grandes e um processo de desenvolvimento lento e manual.
*   **Ausência de Gerenciamento de Estado:** O estado da aplicação (elementos no canvas, conexões, etc.) é gerenciado de forma manual e descentralizada, levando a bugs de sincronização e perda de dados do usuário ao recarregar a página.

### 1.2. Problemas Críticos de Usabilidade (UX/UI) - Foco no Canvas

*   **Interação de Arrastar e Soltar (Drag-and-Drop) Primitiva:** A funcionalidade é inconsistente e carece de feedback visual claro. O usuário não sabe *onde* pode soltar um elemento nem o que acontecerá em seguida.
*   **Conexão entre Elementos Inexistente ou Contra-intuitiva:** Não há um mecanismo claro para criar, visualizar e gerenciar as relações (conexões) entre as estruturas legais no canvas, que é uma funcionalidade central da ferramenta.
*   **Falta de Feedback Visual e Contextual:** A interface não informa o usuário sobre o estado do sistema. Faltam indicadores de carregamento, sucesso, erro e validação em tempo real. Um nó com problema de conformidade, por exemplo, não se diferencia de um nó válido.
*   **Manipulação de Elementos Limitada:** Funcionalidades essenciais para uma ferramenta de diagramação estão ausentes: seleção múltipla, duplicação, alinhamento, zoom e pan eficientes.
*   **Interface Não Otimizada para Produtividade:** A ausência de um painel de propriedades, de uma barra de ferramentas com ações rápidas e de atalhos de teclado torna o processo de criação de estruturas lento e repetitivo.

## 2. Visão Estratégica e Arquitetura Proposta

O objetivo é transformar o frontend do Sirius em uma **Single-Page Application (SPA)** moderna, reativa e altamente performática, utilizando as melhores práticas de desenvolvimento e usabilidade.

### 2.1. Stack Tecnológica Recomendada

*   **Framework:** **Vue 3 com Composition API** para criar componentes reativos e bem estruturados.
*   **Build Tool:** **Vite** para um desenvolvimento ultrarrápido (Hot Module Replacement) e builds otimizados.
*   **Gerenciamento de Estado:** **Pinia** como a store centralizada, garantindo um fluxo de dados previsível e persistente.
*   **Estilização:** **Tailwind CSS** (instalado via npm) para uma UI consistente e customizável, compilado com PostCSS para remover estilos não utilizados.
*   **Linguagem:** **TypeScript** para adicionar segurança de tipo, melhorar o autocompletar e reduzir bugs em tempo de execução.

### 2.2. Nova Estrutura de Projeto (Dentro de `frontend-new/`)

```
/frontend-new
├── src/
│   ├── App.vue             # Componente raiz
│   ├── main.ts             # Ponto de entrada da aplicação
│   ├── components/
│   │   ├── canvas/
│   │   │   ├── SiriusCanvas.vue      # O componente principal do canvas
│   │   │   ├── StructureNode.vue     # Componente para cada nó/estrutura
│   │   │   ├── ConnectionEdge.vue    # Componente para as linhas de conexão
│   │   │   └── CanvasMinimap.vue     # (Opcional) Minimapa para navegação
│   │   ├── layout/
│   │   │   ├── AppHeader.vue
│   │   │   ├── AppSidebar.vue        # Barra lateral com a lista de estruturas
│   │   │   └── PropertiesPanel.vue   # Painel para editar detalhes do nó selecionado
│   │   └── ui/                   # Componentes de UI genéricos (Botão, Modal, etc.)
│   ├── stores/
│   │   ├── canvas.ts           # Store Pinia para gerenciar o estado do canvas
│   │   └── structures.ts       # Store para as estruturas disponíveis
│   ├── services/
│   │   └── api.ts              # Módulo para comunicação com o backend Django
│   ├── types/
│   │   └── index.ts            # Definições de tipos (TypeScript)
│   └── styles/
│       └── main.css            # Estilos globais
└── package.json
```

## 3. Plano de Refatoração Detalhado (Por Fases)

### Fase 1: Fundação e Consolidação (2 Semanas)

O objetivo desta fase é construir a base sólida para a nova aplicação, eliminando o código legado.

1.  **Setup do Projeto:** Configurar o projeto em `frontend-new/` com Vite, Vue 3, TypeScript, Pinia e Tailwind CSS.
2.  **Consolidação de Lógica:** Migrar toda a lógica de busca de dados (`fetch`) para o `services/api.ts` e o estado das estruturas para a store `stores/structures.ts`.
3.  **Componente de Layout Básico:** Criar os componentes de layout (`AppHeader`, `AppSidebar`) e renderizar a lista de estruturas a partir da store Pinia, tornando-as arrastáveis.
4.  **Criação do Canvas Básico:** Implementar o componente `SiriusCanvas.vue` como uma área de "drop" que recebe os elementos da sidebar. A store `stores/canvas.ts` deve ser capaz de adicionar e armazenar a posição dos nós soltos no canvas.
5.  **Remoção do Legado:** Após a funcionalidade básica ser recriada, remover os arquivos .js e .html legados de `static/` e `templates/` para evitar confusão.

### Fase 2: Overhaul da Usabilidade do Canvas (3 Semanas)

Esta é a fase mais crítica, focada em transformar a experiência de interação.

1.  **Drag-and-Drop Aprimorado:**
    *   **Feedback Visual:** O nó sendo arrastado deve ter uma aparência distinta (ex: semi-transparente). O canvas deve indicar visualmente que é uma área de drop válida.
    *   **Snap-to-Grid:** Implementar um grid invisível para que os nós se alinhem facilmente, trazendo ordem à diagramação.
2.  **Sistema de Conexões Intuitivo:**
    *   **Pontos de Conexão:** Cada `StructureNode.vue` exibirá "pontos de conexão" ao ser selecionado ou ao passar o mouse.
    *   **Criação de Conexão:** O usuário poderá clicar e arrastar de um ponto de conexão a outro para criar uma `ConnectionEdge.vue`.
    *   **Validação Visual:** Enquanto arrasta uma conexão, os pontos de conexão compatíveis em outros nós devem ser destacados. Pontos incompatíveis devem ser desabilitados visualmente.
3.  **Manipulação Avançada de Nós:**
    *   **Seleção:** Implementar seleção de um único nó com um clique. O nó selecionado deve ter um destaque claro (ex: borda azul).
    *   **Painel de Propriedades:** Ao selecionar um nó, o `PropertiesPanel.vue` deve exibir suas informações (nome, jurisdição, custo) e permitir edições.
    *   **Zoom e Pan:** Implementar zoom com o scroll do mouse (ou botões na UI) e pan ao clicar e arrastar o fundo do canvas (ex: com o botão do meio do mouse ou segurando a barra de espaço).
4.  **Barra de Ferramentas (`CanvasToolbar.vue`):**
    *   Adicionar uma barra de ferramentas flutuante ou fixa com ações comuns: Zoom In/Out, Fit to Screen, Limpar Canvas, Salvar Configuração.

### Fase 3: Integração de Lógica de Negócio e Polimento (2 Semanas)

O objetivo é conectar a UI aprimorada com as regras de negócio do backend.

1.  **Validação em Tempo Real:**
    *   A store do canvas (`canvas.ts`) chamará a API de validação do Django sempre que uma mudança ocorrer (nó adicionado, conexão criada).
    *   Nós ou conexões com problemas de conformidade devem mudar de cor (ex: borda vermelha) e exibir um ícone de alerta. Passar o mouse sobre o ícone deve mostrar uma tooltip com o erro.
2.  **Cálculo de Custos Dinâmico:**
    *   Um painel de "Resumo de Custos" na UI será atualizado em tempo real, buscando os dados da API de cálculo de custos conforme a estrutura é montada.
3.  **Atalhos de Teclado:**
    *   Implementar atalhos para produtividade: `Delete` para remover o nó selecionado, `Ctrl/Cmd + Z` para desfazer, `Ctrl/Cmd + S` para salvar.
4.  **Persistência de Estado:**
    *   Salvar o estado do canvas (nós, posições, conexões) no `localStorage` do navegador. Assim, se o usuário recarregar a página, seu trabalho não será perdido.

## 4. Métricas de Sucesso

O sucesso da refatoração será medido por:

*   **Métricas Técnicas:**
    *   **Lighthouse Performance Score:** Atingir uma pontuação > 90.
    *   **Tamanho do Bundle:** Redução de pelo menos 50% no tamanho total do JavaScript carregado.
    *   **Tempo de Carregamento Inicial (LCP):** Abaixo de 2.5 segundos.
*   **Métricas de Usabilidade:**
    *   **Redução de Cliques:** Diminuir em 40% o número de cliques para criar uma estrutura complexa.
    *   **Taxa de Erro de Tarefa:** Reduzir a frequência com que os usuários criam configurações inválidas.
    *   **Feedback Qualitativo:** Pesquisas de satisfação com usuários-chave para validar a nova experiência.

Este plano fornece um caminho claro para transformar o frontend do Sirius, resultando em um produto robusto, agradável de usar e fácil de manter.
