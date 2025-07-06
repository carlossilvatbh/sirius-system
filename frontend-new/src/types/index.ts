// Legal Structure Types
export interface LegalStructure {
  id: number;
  nome: string;
  tipo: StructureType;
  descricao: string;
  custo_base: number;
  custo_manutencao: number;
  tempo_implementacao: number;
  complexidade: number;
  impacto_tributario_eua: string;
  impacto_tributario_brasil: string;
  impacto_tributario_outros?: string;
  nivel_confidencialidade: number;
  protecao_patrimonial: number;
  impacto_privacidade: string;
  facilidade_banking: number;
  documentacao_necessaria: string;
  formularios_obrigatorios_eua?: string;
  formularios_obrigatorios_brasil?: string;
  ativo: boolean;
  created_at: string;
  updated_at: string;
}

export type StructureType = 
  | 'BDAO_SAC'
  | 'WYOMING_DAO_LLC'
  | 'BTS_VAULT'
  | 'WYOMING_FOUNDATION'
  | 'WYOMING_CORP'
  | 'NATIONALIZATION'
  | 'FUND_TOKEN';

// Canvas Types
export interface CanvasNode {
  id: string;
  type: 'structure';
  position: Position;
  data: {
    structure: LegalStructure;
    selected?: boolean;
  };
}

export interface Position {
  x: number;
  y: number;
}

export interface CanvasEdge {
  id: string;
  source: string;
  target: string;
  type: ConnectionType;
  data?: {
    label?: string;
    connectionType?: ConnectionType;
  };
}

export type ConnectionType = 'ownership' | 'control' | 'beneficiary';

// Validation Types
export interface ValidationRule {
  id: string;
  name: string;
  description: string;
  category: string;
  severity: SeverityLevel;
  jurisdiction?: string;
  applicableStructures?: string[];
  estrutura_a?: number;
  estrutura_b?: number;
  tipo_relacionamento?: RelationshipType;
  descricao?: string;
  condicoes?: Record<string, any>;
  jurisdicao_aplicavel?: string;
  ativo?: boolean;
  solution?: string;
}

export type RelationshipType = 
  | 'REQUIRED'
  | 'RECOMMENDED'
  | 'INCOMPATIBLE'
  | 'CONDITIONAL'
  | 'SYNERGISTIC';

export type SeverityLevel = 'ERROR' | 'WARNING' | 'INFO';

export interface ValidationResult {
  isValid: boolean;
  score: number; // 0-100 validation score
  errors: ValidationError[];
  warnings: ValidationWarning[];
  suggestions: ValidationSuggestion[];
}

export interface ValidationError {
  id: string;
  message: string;
  structureIds: string[];
  severity: 'ERROR';
}

export interface ValidationWarning {
  id: string;
  message: string;
  structureIds: string[];
  severity: 'WARNING';
}

export interface ValidationSuggestion {
  id: string;
  message: string;
  structureIds: string[];
  severity: 'INFO';
}

// Template Types
export interface Template {
  id: number;
  nome: string;
  categoria: TemplateCategory;
  complexidade_template: TemplateComplexity;
  descricao: string;
  configuracao: Configuration;
  custo_total: number;
  tempo_total_implementacao: number;
  uso_count: number;
  publico_alvo?: string;
  casos_uso?: string;
  created_at: string;
  updated_at: string;
  ativo: boolean;
}

export type TemplateCategory = 
  | 'TECH'
  | 'REAL_ESTATE'
  | 'TRADING'
  | 'FAMILY_OFFICE'
  | 'INVESTMENT'
  | 'GENERAL';

export type TemplateComplexity = 
  | 'BASIC'
  | 'INTERMEDIATE'
  | 'ADVANCED'
  | 'EXPERT';

// Configuration Types
export interface Configuration {
  nodes: CanvasNode[];
  edges: CanvasEdge[];
  metadata?: {
    name?: string;
    description?: string;
    created_at?: string;
    updated_at?: string;
  };
}

// Pricing Types
export interface PricingScenario {
  id: string;
  name: string;
  multiplier: number;
  description: string;
}

export interface CostBreakdown {
  setup_cost: number;
  maintenance_cost: number;
  total_first_year: number;
  annual_cost: number;
  scenario_multiplier: number;
  final_cost: number;
}

// API Response Types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: 'success' | 'error';
}

export interface PaginatedResponse<T> {
  results: T[];
  count: number;
  next?: string;
  previous?: string;
}

// Filter Types
export interface StructureFilters {
  tipo?: StructureType;
  complexidade?: number;
  custo_max?: number;
  search?: string;
}

export interface TemplateFilters {
  categoria?: TemplateCategory;
  complexidade?: TemplateComplexity;
  search?: string;
}

// User Context Types
export interface UserContext {
  jurisdiction?: string;
  user_type?: 'individual' | 'business';
  preferences?: UserPreferences;
}

export interface UserPreferences {
  default_currency?: string;
  language?: string;
  theme?: 'light' | 'dark';
}

export interface JurisdictionAlert {
  id: string;
  jurisdiction: string;
  type: 'tax' | 'compliance' | 'reporting' | 'deadline' | 'regulatory';
  priority: 'critical' | 'high' | 'medium' | 'low';
  title: string;
  description: string;
  deadline?: string;
  affectedStructures: string[];
  actionRequired: boolean;
  // Legacy fields for backward compatibility
  jurisdicao?: string;
  tipo_alerta?: AlertType;
  titulo?: string;
  descricao?: string;
  estruturas_aplicaveis?: number[];
  prioridade?: number;
  ativo?: boolean;
  created_at?: string;
  updated_at?: string;
}

export type AlertType = 
  | 'TAX'
  | 'COMPLIANCE'
  | 'REPORTING'
  | 'DEADLINE'
  | 'REGULATORY';

// UI State Types
export interface UIState {
  loading: boolean;
  error?: string;
  selectedStructure?: LegalStructure;
  selectedNode?: string;
  sidebarOpen: boolean;
  mobileMenuOpen: boolean;
}

// Export all types
export * from './canvas';
export * from './validation';
export * from './api';

