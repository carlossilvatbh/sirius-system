// API Service Types
export interface ApiService {
  // Structures
  getStructures(filters?: StructureFilters): Promise<LegalStructure[]>;
  getStructure(id: number): Promise<LegalStructure>;
  
  // Validation
  validateConfiguration(config: Configuration): Promise<ValidationResult>;
  getValidationRules(): Promise<ValidationRule[]>;
  
  // Templates
  getTemplates(filters?: TemplateFilters): Promise<Template[]>;
  getTemplate(id: number): Promise<Template>;
  saveTemplate(template: CreateTemplateRequest): Promise<Template>;
  updateTemplate(id: number, updates: UpdateTemplateRequest): Promise<Template>;
  deleteTemplate(id: number): Promise<void>;
  
  // Configurations
  saveConfiguration(config: SaveConfigurationRequest): Promise<SavedConfiguration>;
  loadConfiguration(id: number): Promise<SavedConfiguration>;
  
  // Reports
  generatePDF(config: Configuration, options?: PDFOptions): Promise<Blob>;
  generateReport(config: Configuration, type: ReportType): Promise<Report>;
  
  // Jurisdiction Alerts
  getJurisdictionAlerts(jurisdiction?: string): Promise<JurisdictionAlert[]>;
}

export interface ApiClient {
  get<T>(url: string, params?: Record<string, any>): Promise<ApiResponse<T>>;
  post<T>(url: string, data?: any): Promise<ApiResponse<T>>;
  put<T>(url: string, data?: any): Promise<ApiResponse<T>>;
  delete<T>(url: string): Promise<ApiResponse<T>>;
}

export interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
  errors?: ApiError[];
}

export interface ApiError {
  field?: string;
  message: string;
  code?: string;
}

export interface PaginatedApiResponse<T> extends ApiResponse<T[]> {
  pagination: {
    count: number;
    page: number;
    pages: number;
    pageSize: number;
    hasNext: boolean;
    hasPrevious: boolean;
  };
}

// Request/Response Types
export interface CreateTemplateRequest {
  nome: string;
  categoria: TemplateCategory;
  complexidade_template: TemplateComplexity;
  descricao: string;
  configuracao: Configuration;
  publico_alvo?: string;
  casos_uso?: string;
}

export interface UpdateTemplateRequest extends Partial<CreateTemplateRequest> {}

export interface SaveConfigurationRequest {
  nome: string;
  descricao?: string;
  configuracao: Configuration;
}

export interface SavedConfiguration {
  id: number;
  nome: string;
  descricao?: string;
  configuracao: Configuration;
  custo_estimado?: number;
  tempo_estimado?: number;
  created_at: string;
  updated_at: string;
}

export interface PDFOptions {
  format?: 'A4' | 'Letter';
  orientation?: 'portrait' | 'landscape';
  includeDetails?: boolean;
  includeCosts?: boolean;
  includeValidation?: boolean;
  template?: 'standard' | 'detailed' | 'executive';
}

export interface Report {
  id: string;
  type: ReportType;
  title: string;
  content: ReportSection[];
  metadata: ReportMetadata;
  generatedAt: string;
}

export type ReportType = 
  | 'structure_analysis'
  | 'tax_implications'
  | 'compliance_checklist'
  | 'cost_breakdown'
  | 'implementation_plan';

export interface ReportSection {
  id: string;
  title: string;
  content: string;
  type: 'text' | 'table' | 'chart' | 'list';
  data?: any;
}

export interface ReportMetadata {
  author: string;
  version: string;
  jurisdiction?: string;
  structures: string[];
  totalCost: number;
  implementationTime: number;
}

// Cache Types
export interface CacheEntry<T> {
  data: T;
  timestamp: number;
  ttl: number;
  key: string;
}

export interface CacheConfig {
  defaultTTL: number;
  maxSize: number;
  enablePersistence: boolean;
  storageKey: string;
}

// Error Types
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string,
    public field?: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export class ValidationError extends Error {
  constructor(
    message: string,
    public errors: ValidationIssue[]
  ) {
    super(message);
    this.name = 'ValidationError';
  }
}

export class NetworkError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'NetworkError';
  }
}

// HTTP Status Codes
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  CONFLICT: 409,
  UNPROCESSABLE_ENTITY: 422,
  INTERNAL_SERVER_ERROR: 500,
  SERVICE_UNAVAILABLE: 503
} as const;

// API Endpoints
export const API_ENDPOINTS = {
  STRUCTURES: '/api/estruturas/',
  STRUCTURE_DETAIL: (id: number) => `/api/estruturas/${id}/`,
  VALIDATE: '/api/validar/',
  VALIDATION_RULES: '/api/regras-validacao/',
  TEMPLATES: '/api/templates/',
  TEMPLATE_DETAIL: (id: number) => `/api/templates/${id}/`,
  CONFIGURATIONS: '/api/configuracoes/',
  CONFIGURATION_DETAIL: (id: number) => `/api/configuracoes/${id}/`,
  GENERATE_PDF: '/api/gerar-pdf/',
  GENERATE_REPORT: '/api/gerar-relatorio/',
  JURISDICTION_ALERTS: '/api/alertas-jurisdicao/'
} as const;

// Import types from other files
import type { 
  LegalStructure, 
  StructureFilters, 
  ValidationResult, 
  ValidationRule, 
  Template, 
  TemplateFilters, 
  TemplateCategory, 
  TemplateComplexity, 
  Configuration, 
  JurisdictionAlert,
  ValidationIssue
} from './index';

