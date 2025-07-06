import type { 
  ValidationEngine, 
  ValidationConfig, 
  ValidationResult as ValidationServiceResult,
  ValidationContext,
  ConnectionValidation,
  StructureValidation,
  ValidationIssue,
  JurisdictionAlert,
  ValidationRule 
} from '@/types/validation';
import type { 
  LegalStructure, 
  ValidationResult 
} from '@/types/index';

export class ValidationService implements ValidationEngine {
  private rules: ValidationRule[] = [];
  private jurisdictionRules = new Map<string, ValidationRule[]>();

  constructor() {
    this.loadDefaultRules();
    this.buildJurisdictionMaps();
  }

  private buildJurisdictionMaps(): void {
    this.jurisdictionRules.clear();
    
    for (const rule of this.rules) {
      if (rule.jurisdiction) {
        if (!this.jurisdictionRules.has(rule.jurisdiction)) {
          this.jurisdictionRules.set(rule.jurisdiction, []);
        }
        this.jurisdictionRules.get(rule.jurisdiction)!.push(rule);
      }
    }
  }

  private loadDefaultRules(): void {
    // Default validation rules for common scenarios
    this.rules = [
      {
        id: 'incompatible-dao-foundation',
        name: 'DAO and Foundation Incompatibility',
        description: 'Wyoming DAO LLC and Wyoming Foundation cannot be used together',
        category: 'compatibility',
        severity: 'high',
        jurisdiction: 'wyoming',
        applicableStructures: ['WYOMING_DAO_LLC', 'WYOMING_FOUNDATION'],
        conditions: [],
        message: 'Wyoming DAO LLC and Wyoming Foundation are incompatible structures',
        solution: 'Choose either a Wyoming DAO LLC or Wyoming Foundation, not both'
      },
      {
        id: 'required-bdao-wyoming',
        name: 'BDAO requires Wyoming structure',
        description: 'BDAO SAC requires at least one Wyoming-based structure',
        category: 'compliance',
        severity: 'high',
        jurisdiction: 'wyoming',
        applicableStructures: ['BDAO_SAC'],
        conditions: [],
        message: 'BDAO SAC requires a Wyoming-based structure for compliance',
        solution: 'Add a Wyoming DAO LLC or Wyoming Foundation'
      },
      {
        id: 'nationalization-requires-corp',
        name: 'Nationalization requires Corporation',
        description: 'Nationalization process requires a Wyoming Corporation',
        category: 'operational',
        severity: 'medium',
        jurisdiction: 'wyoming',
        applicableStructures: ['NATIONALIZATION'],
        conditions: [],
        message: 'Nationalization requires a Wyoming Corporation',
        solution: 'Add a Wyoming Corporation before nationalization'
      }
    ];
  }

  async validateConfiguration(config: ValidationConfig): Promise<ValidationServiceResult> {
    // Mock the API call and return the ValidationResult from validation.ts
    const result: ValidationServiceResult = {
      isValid: true,
      score: 100,
      errors: [],
      warnings: [],
      suggestions: [],
      recommendations: []
    };

    // Basic validation logic
    if (config.nodes.length === 0) {
      result.isValid = false;
      result.errors.push({
        id: 'no-structures',
        type: 'error',
        severity: 'critical',
        title: 'No Structures',
        description: 'At least one structure is required',
        affectedNodes: [],
        affectedEdges: [],
        rule: this.rules[0], // Placeholder
        solution: 'Add at least one legal structure to your configuration'
      });
    }

    // Run validation rules
    for (const rule of this.rules) {
      const applicable = config.nodes.some(node => 
        rule.applicableStructures?.includes(node.data.structure.tipo)
      );
      
      if (applicable) {
        const issue = this.checkRule(rule, config);
        if (issue) {
          if (rule.severity === 'high') {
            result.errors.push(issue);
          } else if (rule.severity === 'medium') {
            result.warnings.push(issue);
          } else {
            result.suggestions.push(issue);
          }
        }
      }
    }

    result.isValid = result.errors.length === 0;
    result.score = this.calculateScore(result);
    
    return result;
  }

  private checkRule(rule: ValidationRule, config: ValidationConfig): ValidationIssue | null {
    // Simple rule checking logic
    if (rule.id === 'incompatible-dao-foundation') {
      const hasDAO = config.nodes.some(node => node.data.structure.tipo === 'WYOMING_DAO_LLC');
      const hasFoundation = config.nodes.some(node => node.data.structure.tipo === 'WYOMING_FOUNDATION');
      
      if (hasDAO && hasFoundation) {
        return {
          id: rule.id,
          type: 'error',
          severity: 'high',
          title: rule.name,
          description: rule.description,
          affectedNodes: config.nodes
            .filter(node => ['WYOMING_DAO_LLC', 'WYOMING_FOUNDATION'].includes(node.data.structure.tipo))
            .map(node => node.id),
          affectedEdges: [],
          rule,
          solution: rule.solution
        };
      }
    }

    return null;
  }

  private calculateScore(result: ValidationServiceResult): number {
    let score = 100;
    score -= result.errors.length * 20;
    score -= result.warnings.length * 10;
    score -= result.suggestions.length * 5;
    return Math.max(0, score);
  }

  async validateConnection(_source: string, _target: string, _type: string): Promise<ConnectionValidation> {
    return {
      isValid: true,
      issues: []
    };
  }

  async validateStructure(_structure: LegalStructure, _context: ValidationContext): Promise<StructureValidation> {
    return {
      isValid: true,
      issues: [],
      compatibleStructures: [],
      incompatibleStructures: []
    };
  }

  async getJurisdictionAlerts(_jurisdiction: string, _structures: LegalStructure[]): Promise<JurisdictionAlert[]> {
    return [];
  }
}

export const validationService = new ValidationService();
