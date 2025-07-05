import type { LegalStructure, Template } from '@/types';

export const mockStructures: LegalStructure[] = [
  {
    id: 1,
    nome: "Bahamas DAO SAC",
    tipo: "BDAO_SAC",
    descricao: "Segregated Account Company in the Bahamas designed for DAO operations with enhanced privacy and asset protection.",
    custo_base: 15000,
    custo_manutencao: 5000,
    tempo_implementacao: 45,
    complexidade: 4,
    impacto_tributario_eua: "No US tax implications for non-US persons. US persons subject to controlled foreign corporation rules.",
    impacto_tributario_brasil: "Subject to Brazilian CFC rules. May require disclosure under Law 12.844/2013.",
    nivel_confidencialidade: 9,
    protecao_patrimonial: 8,
    impacto_privacidade: "High privacy protection with segregated accounts and nominee services available.",
    facilidade_banking: 7,
    documentacao_necessaria: "Articles of Association, Memorandum, Board Resolutions, KYC documentation",
    ativo: true,
    created_at: "2024-01-01T00:00:00Z",
    updated_at: "2024-01-01T00:00:00Z"
  },
  {
    id: 2,
    nome: "Wyoming DAO LLC",
    tipo: "WYOMING_DAO_LLC",
    descricao: "Limited Liability Company in Wyoming specifically designed for Decentralized Autonomous Organizations.",
    custo_base: 8000,
    custo_manutencao: 2000,
    tempo_implementacao: 21,
    complexidade: 3,
    impacto_tributario_eua: "Pass-through taxation. Members report income/losses on personal returns.",
    impacto_tributario_brasil: "Transparent entity for Brazilian tax purposes. Income attributed to Brazilian members.",
    nivel_confidencialidade: 6,
    protecao_patrimonial: 7,
    impacto_privacidade: "Moderate privacy with public filing requirements but member privacy protection.",
    facilidade_banking: 8,
    documentacao_necessaria: "Articles of Organization, Operating Agreement, Registered Agent appointment",
    ativo: true,
    created_at: "2024-01-01T00:00:00Z",
    updated_at: "2024-01-01T00:00:00Z"
  },
  {
    id: 3,
    nome: "BTS Vault",
    tipo: "BTS_VAULT",
    descricao: "Bitcoin Treasury Services vault solution for institutional-grade cryptocurrency storage and management.",
    custo_base: 25000,
    custo_manutencao: 8000,
    tempo_implementacao: 60,
    complexidade: 5,
    impacto_tributario_eua: "Subject to US tax on cryptocurrency gains. Requires detailed record keeping.",
    impacto_tributario_brasil: "Cryptocurrency gains subject to capital gains tax. Monthly reporting required.",
    nivel_confidencialidade: 10,
    protecao_patrimonial: 9,
    impacto_privacidade: "Maximum privacy with institutional-grade security and confidentiality.",
    facilidade_banking: 5,
    documentacao_necessaria: "Custody agreements, Security protocols, Insurance documentation, Compliance procedures",
    ativo: true,
    created_at: "2024-01-01T00:00:00Z",
    updated_at: "2024-01-01T00:00:00Z"
  },
  {
    id: 4,
    nome: "Wyoming Foundation",
    tipo: "WYOMING_FOUNDATION",
    descricao: "Private foundation in Wyoming for charitable, educational, or family purposes with perpetual existence.",
    custo_base: 12000,
    custo_manutencao: 4000,
    tempo_implementacao: 35,
    complexidade: 4,
    impacto_tributario_eua: "Tax-exempt if qualifying purposes. Subject to private foundation excise taxes.",
    impacto_tributario_brasil: "May qualify for tax exemption if charitable purposes. Requires specific documentation.",
    nivel_confidencialidade: 7,
    protecao_patrimonial: 8,
    impacto_privacidade: "Good privacy protection with limited public disclosure requirements.",
    facilidade_banking: 6,
    documentacao_necessaria: "Articles of Incorporation, Bylaws, IRS determination letter, Board resolutions",
    ativo: true,
    created_at: "2024-01-01T00:00:00Z",
    updated_at: "2024-01-01T00:00:00Z"
  },
  {
    id: 5,
    nome: "Wyoming Corporation",
    tipo: "WYOMING_CORP",
    descricao: "C-Corporation in Wyoming providing strong asset protection and business flexibility.",
    custo_base: 6000,
    custo_manutencao: 1500,
    tempo_implementacao: 14,
    complexidade: 2,
    impacto_tributario_eua: "Double taxation: corporate level and shareholder level on distributions.",
    impacto_tributario_brasil: "Subject to Brazilian CFC rules if controlled by Brazilian residents.",
    nivel_confidencialidade: 5,
    protecao_patrimonial: 8,
    impacto_privacidade: "Standard corporate privacy with public filing of basic information.",
    facilidade_banking: 9,
    documentacao_necessaria: "Articles of Incorporation, Bylaws, Stock certificates, Board resolutions",
    ativo: true,
    created_at: "2024-01-01T00:00:00Z",
    updated_at: "2024-01-01T00:00:00Z"
  },
  {
    id: 6,
    nome: "Nationalization Service",
    tipo: "NATIONALIZATION",
    descricao: "Process to obtain US tax residency for foreign corporations through effective management.",
    custo_base: 18000,
    custo_manutencao: 6000,
    tempo_implementacao: 90,
    complexidade: 5,
    impacto_tributario_eua: "Corporation becomes US tax resident. Subject to US corporate income tax.",
    impacto_tributario_brasil: "May trigger exit taxation. Requires careful planning and documentation.",
    nivel_confidencialidade: 4,
    protecao_patrimonial: 6,
    impacto_privacidade: "Reduced privacy due to US tax reporting requirements and transparency rules.",
    facilidade_banking: 9,
    documentacao_necessaria: "Management agreements, Tax residency documentation, Transfer pricing studies",
    ativo: true,
    created_at: "2024-01-01T00:00:00Z",
    updated_at: "2024-01-01T00:00:00Z"
  }
];

export const mockTemplates: Template[] = [
  {
    id: 1,
    nome: "Tech Startup Structure",
    categoria: "TECH",
    complexidade_template: "INTERMEDIATE",
    descricao: "Optimized structure for technology startups with US operations and international founders.",
    configuracao: {
      nodes: [
        {
          id: "node-1",
          type: "structure",
          position: { x: 100, y: 100 },
          data: {
            structure: mockStructures[1], // Wyoming DAO LLC
            selected: false
          }
        },
        {
          id: "node-2", 
          type: "structure",
          position: { x: 300, y: 200 },
          data: {
            structure: mockStructures[4], // Wyoming Corp
            selected: false
          }
        }
      ],
      edges: [
        {
          id: "edge-1",
          source: "node-1",
          target: "node-2",
          type: "ownership",
          data: {
            connectionType: "ownership",
            label: "100% Ownership"
          }
        }
      ],
      metadata: {
        name: "Tech Startup Structure",
        description: "Standard structure for tech startups",
        created_at: "2024-01-01T00:00:00Z"
      }
    },
    custo_total: 14000,
    tempo_total_implementacao: 35,
    uso_count: 25,
    publico_alvo: "Technology startups, SaaS companies, blockchain projects",
    casos_uso: "Fundraising, IP protection, international expansion",
    created_at: "2024-01-01T00:00:00Z",
    updated_at: "2024-01-01T00:00:00Z",
    ativo: true
  },
  {
    id: 2,
    nome: "Crypto Investment Fund",
    categoria: "INVESTMENT",
    complexidade_template: "ADVANCED",
    descricao: "Sophisticated structure for cryptocurrency investment funds with maximum privacy and asset protection.",
    configuracao: {
      nodes: [
        {
          id: "node-1",
          type: "structure", 
          position: { x: 150, y: 50 },
          data: {
            structure: mockStructures[0], // BDAO SAC
            selected: false
          }
        },
        {
          id: "node-2",
          type: "structure",
          position: { x: 50, y: 200 },
          data: {
            structure: mockStructures[2], // BTS Vault
            selected: false
          }
        },
        {
          id: "node-3",
          type: "structure",
          position: { x: 250, y: 200 },
          data: {
            structure: mockStructures[1], // Wyoming DAO LLC
            selected: false
          }
        }
      ],
      edges: [
        {
          id: "edge-1",
          source: "node-1",
          target: "node-2", 
          type: "control",
          data: {
            connectionType: "control",
            label: "Asset Management"
          }
        },
        {
          id: "edge-2",
          source: "node-1",
          target: "node-3",
          type: "ownership", 
          data: {
            connectionType: "ownership",
            label: "Operating Entity"
          }
        }
      ],
      metadata: {
        name: "Crypto Investment Fund",
        description: "Advanced crypto fund structure",
        created_at: "2024-01-01T00:00:00Z"
      }
    },
    custo_total: 48000,
    tempo_total_implementacao: 105,
    uso_count: 12,
    publico_alvo: "Crypto funds, family offices, high-net-worth individuals",
    casos_uso: "Cryptocurrency investment, DeFi strategies, institutional trading",
    created_at: "2024-01-01T00:00:00Z",
    updated_at: "2024-01-01T00:00:00Z",
    ativo: true
  },
  {
    id: 3,
    nome: "Family Office Structure",
    categoria: "FAMILY_OFFICE",
    complexidade_template: "EXPERT",
    descricao: "Comprehensive family office structure with charitable giving and multi-generational planning.",
    configuracao: {
      nodes: [
        {
          id: "node-1",
          type: "structure",
          position: { x: 200, y: 50 },
          data: {
            structure: mockStructures[3], // Wyoming Foundation
            selected: false
          }
        },
        {
          id: "node-2",
          type: "structure", 
          position: { x: 100, y: 200 },
          data: {
            structure: mockStructures[4], // Wyoming Corp
            selected: false
          }
        },
        {
          id: "node-3",
          type: "structure",
          position: { x: 300, y: 200 },
          data: {
            structure: mockStructures[0], // BDAO SAC
            selected: false
          }
        }
      ],
      edges: [
        {
          id: "edge-1",
          source: "node-1",
          target: "node-2",
          type: "beneficiary",
          data: {
            connectionType: "beneficiary", 
            label: "Charitable Distributions"
          }
        },
        {
          id: "edge-2",
          source: "node-1",
          target: "node-3",
          type: "ownership",
          data: {
            connectionType: "ownership",
            label: "Investment Holdings"
          }
        }
      ],
      metadata: {
        name: "Family Office Structure",
        description: "Multi-generational family office",
        created_at: "2024-01-01T00:00:00Z"
      }
    },
    custo_total: 27000,
    tempo_total_implementacao: 80,
    uso_count: 8,
    publico_alvo: "Ultra-high-net-worth families, multi-generational wealth",
    casos_uso: "Estate planning, charitable giving, family governance",
    created_at: "2024-01-01T00:00:00Z", 
    updated_at: "2024-01-01T00:00:00Z",
    ativo: true
  }
];

