import type { LegalStructure, SiriusNode, SiriusEdge } from './index';

export interface ValidationEngine {
  validateConfiguration(config: ValidationConfig): Promise<ValidationResult>;
  validateConnection(source: string, target: string, type: string): Promise<ConnectionValidation>;
  validateStructure(structure: LegalStructure, context: ValidationContext): Promise<StructureValidation>;
  getJurisdictionAlerts(jurisdiction: string, structures: LegalStructure[]): Promise<JurisdictionAlert[]>;
}

export interface ValidationConfig {
  nodes: SiriusNode[];
  edges: SiriusEdge[];
  context: ValidationContext;
}

export interface ValidationContext {
  jurisdiction?: string;
  userType?: 'individual' | 'business';
  clientProfile?: ClientProfile;
  complianceLevel?: 'basic' | 'standard' | 'strict';
}

export interface ClientProfile {
  residency: string[];
  citizenship: string[];
  businessType?: string;
  assetValue?: number;
  riskTolerance?: 'low' | 'medium' | 'high';
}

export interface ValidationResult {
  isValid: boolean;
  score: number; // 0-100
  errors: ValidationIssue[];
  warnings: ValidationIssue[];
  suggestions: ValidationIssue[];
  recommendations: Recommendation[];
}

export interface ValidationIssue {
  id: string;
  type: 'error' | 'warning' | 'suggestion';
  severity: 'critical' | 'high' | 'medium' | 'low';
  title: string;
  description: string;
  affectedNodes: string[];
  affectedEdges: string[];
  rule: ValidationRule;
  solution?: string;
  learnMoreUrl?: string;
}

export interface Recommendation {
  id: string;
  title: string;
  description: string;
  type: 'structure' | 'connection' | 'optimization';
  priority: 'high' | 'medium' | 'low';
  suggestedStructures?: LegalStructure[];
  estimatedBenefit?: string;
  implementationComplexity?: 'low' | 'medium' | 'high';
}

export interface ConnectionValidation {
  isValid: boolean;
  issues: ValidationIssue[];
  suggestedAlternatives?: ConnectionAlternative[];
}

export interface ConnectionAlternative {
  type: string;
  description: string;
  benefits: string[];
  drawbacks: string[];
}

export interface StructureValidation {
  isValid: boolean;
  issues: ValidationIssue[];
  compatibleStructures: LegalStructure[];
  incompatibleStructures: LegalStructure[];
}

export interface ValidationRule {
  id: string;
  name: string;
  description: string;
  category: ValidationCategory;
  severity: 'critical' | 'high' | 'medium' | 'low';
  jurisdiction?: string;
  applicableStructures: string[];
  conditions: ValidationCondition[];
  message: string;
  solution?: string;
  learnMoreUrl?: string;
}

export type ValidationCategory = 
  | 'compatibility'
  | 'tax_optimization'
  | 'compliance'
  | 'asset_protection'
  | 'operational'
  | 'regulatory';

export interface ValidationCondition {
  field: string;
  operator: 'equals' | 'not_equals' | 'contains' | 'not_contains' | 'greater_than' | 'less_than';
  value: any;
  logic?: 'AND' | 'OR';
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
  resources: AlertResource[];
}

export interface AlertResource {
  type: 'form' | 'guide' | 'regulation' | 'contact';
  title: string;
  url: string;
  description?: string;
}

export interface ValidationStats {
  totalRules: number;
  passedRules: number;
  failedRules: number;
  warningRules: number;
  score: number;
  lastValidated: string;
}

export interface RealTimeValidation {
  enabled: boolean;
  debounceMs: number;
  validateOnChange: boolean;
  validateOnConnection: boolean;
  showInlineErrors: boolean;
  showTooltips: boolean;
}

// Validation rule presets for common scenarios
export const VALIDATION_PRESETS = {
  US_RESIDENT: {
    name: 'US Resident',
    description: 'Validation rules for US tax residents',
    jurisdiction: 'US',
    strictness: 'high'
  },
  BRAZILIAN_RESIDENT: {
    name: 'Brazilian Resident',
    description: 'Validation rules for Brazilian tax residents',
    jurisdiction: 'BR',
    strictness: 'high'
  },
  INTERNATIONAL: {
    name: 'International',
    description: 'General international validation rules',
    jurisdiction: 'GLOBAL',
    strictness: 'medium'
  }
} as const;

