import type {
  ValidationEngine,
  ValidationConfig,
  ValidationResult,
  ValidationContext,
  ValidationRule,
  ValidationIssue,
  Recommendation,
  ConnectionValidation,
  StructureValidation,
  LegalStructure,
  SiriusNode,
  SiriusEdge,
  JurisdictionAlert
} from '@/types';
import { apiService } from './api';

class ValidationService implements ValidationEngine {
  private rules: ValidationRule[] = [];
  private jurisdictionRules: Map<string, ValidationRule[]> = new Map();
  private ruleCache: Map<string, ValidationResult> = new Map();

  constructor() {
    this.loadValidationRules();
  }

  private async loadValidationRules(): Promise<void> {
    try {
      const rules = await apiService.getValidationRules();
      this.rules = rules;
      this.organizeRulesByJurisdiction();
    } catch (error) {
      console.error('Failed to load validation rules:', error);
      // Use default rules as fallback
      this.loadDefaultRules();
    }
  }

  private organizeRulesByJurisdiction(): void {
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
        applicableStructures: ['WYOMING_DAO_LLC', 'WYOMING_FOUNDATION'],
        conditions: [
          { field: 'tipo', operator: 'equals', value: 'WYOMING_DAO_LLC' },
          { field: 'tipo', operator: 'equals', value: 'WYOMING_FOUNDATION', logic: 'AND' }
        ],
        message: 'Wyoming DAO LLC and Wyoming Foundation have conflicting legal structures',
        solution: 'Choose either DAO LLC or Foundation, not both'
      },
      {
        id: 'required-bdao-wyoming',
        name: 'BDAO SAC requires Wyoming structure',
        description: 'Bahamas DAO SAC requires a Wyoming structure for US operations',
        category: 'compatibility',
        severity: 'medium',
        applicableStructures: ['BDAO_SAC'],
        conditions: [
          { field: 'tipo', operator: 'equals', value: 'BDAO_SAC' }
        ],
        message: 'BDAO SAC should be paired with a Wyoming structure for optimal tax efficiency',
        solution: 'Add Wyoming DAO LLC or Wyoming Corporation'
      },
      {
        id: 'nationalization-requires-corp',
        name: 'Nationalization requires Corporation',
        description: 'Nationalization can only be applied to corporations',
        category: 'operational',
        severity: 'critical',
        applicableStructures: ['NATIONALIZATION'],
        conditions: [
          { field: 'tipo', operator: 'equals', value: 'NATIONALIZATION' }
        ],
        message: 'Nationalization can only be applied to Wyoming Corporations',
        solution: 'Add Wyoming Corporation before nationalization'
      }
    ];
  }

  async validateConfiguration(config: ValidationConfig): Promise<ValidationResult> {
    const cacheKey = this.generateCacheKey(config);
    const cached = this.ruleCache.get(cacheKey);
    
    if (cached) {
      return cached;
    }

    const result: ValidationResult = {
      isValid: true,
      score: 100,
      errors: [],
      warnings: [],
      suggestions: [],
      recommendations: []
    };

    // Validate structure compatibility
    await this.validateStructureCompatibility(config, result);
    
    // Validate connections
    await this.validateConnections(config, result);
    
    // Validate jurisdiction-specific rules
    await this.validateJurisdictionRules(config, result);
    
    // Generate recommendations
    await this.generateRecommendations(config, result);
    
    // Calculate final score
    result.score = this.calculateValidationScore(result);
    result.isValid = result.errors.length === 0;

    // Cache result
    this.ruleCache.set(cacheKey, result);
    
    return result;
  }

  async validateConnection(source: string, target: string, type: string): Promise<ConnectionValidation> {
    // Find source and target structures
    // This would need access to the current configuration
    // For now, return basic validation
    
    return {
      isValid: true,
      issues: [],
      suggestedAlternatives: []
    };
  }

  async validateStructure(structure: LegalStructure, context: ValidationContext): Promise<StructureValidation> {
    const issues: ValidationIssue[] = [];
    
    // Validate based on context
    if (context.jurisdiction === 'US' && structure.tipo === 'BDAO_SAC') {
      issues.push({
        id: 'us-resident-bdao',
        type: 'warning',
        severity: 'medium',
        title: 'US Resident BDAO Considerations',
        description: 'US residents using BDAO SAC may have additional reporting requirements',
        affectedNodes: [],
        affectedEdges: [],
        rule: this.rules[0], // Placeholder
        solution: 'Consult with tax advisor for FBAR and Form 3520 requirements'
      });
    }

    return {
      isValid: issues.filter(i => i.type === 'error').length === 0,
      issues,
      compatibleStructures: [],
      incompatibleStructures: []
    };
  }

  async getJurisdictionAlerts(jurisdiction: string, structures: LegalStructure[]): Promise<JurisdictionAlert[]> {
    try {
      return await apiService.getJurisdictionAlerts(jurisdiction);
    } catch (error) {
      console.error('Failed to get jurisdiction alerts:', error);
      return [];
    }
  }

  private async validateStructureCompatibility(config: ValidationConfig, result: ValidationResult): Promise<void> {
    const structureTypes = config.nodes.map(node => node.data.structure.tipo);
    
    for (const rule of this.rules) {
      if (rule.category === 'compatibility') {
        const applicableStructures = rule.applicableStructures.filter(type => 
          structureTypes.includes(type as any)
        );
        
        if (applicableStructures.length >= 2) {
          // Check if this is an incompatibility rule
          if (rule.id.includes('incompatible')) {
            const issue: ValidationIssue = {
              id: rule.id,
              type: 'error',
              severity: rule.severity as any,
              title: rule.name,
              description: rule.description,
              affectedNodes: config.nodes
                .filter(node => applicableStructures.includes(node.data.structure.tipo))
                .map(node => node.id),
              affectedEdges: [],
              rule,
              solution: rule.solution
            };
            
            result.errors.push(issue);
          }
        } else if (applicableStructures.length === 1 && rule.id.includes('required')) {
          // Check for required combinations
          const issue: ValidationIssue = {
            id: rule.id,
            type: 'warning',
            severity: rule.severity as any,
            title: rule.name,
            description: rule.description,
            affectedNodes: config.nodes
              .filter(node => applicableStructures.includes(node.data.structure.tipo))
              .map(node => node.id),
            affectedEdges: [],
            rule,
            solution: rule.solution
          };
          
          result.warnings.push(issue);
        }
      }
    }
  }

  private async validateConnections(config: ValidationConfig, result: ValidationResult): Promise<void> {
    for (const edge of config.edges) {
      const sourceNode = config.nodes.find(n => n.id === edge.source);
      const targetNode = config.nodes.find(n => n.id === edge.target);
      
      if (!sourceNode || !targetNode) {
        result.errors.push({
          id: `invalid-connection-${edge.id}`,
          type: 'error',
          severity: 'critical',
          title: 'Invalid Connection',
          description: 'Connection references non-existent structures',
          affectedNodes: [],
          affectedEdges: [edge.id],
          rule: {} as any,
          solution: 'Remove invalid connection'
        });
      }
    }
  }

  private async validateJurisdictionRules(config: ValidationConfig, result: ValidationResult): Promise<void> {
    if (!config.context.jurisdiction) return;
    
    const jurisdictionRules = this.jurisdictionRules.get(config.context.jurisdiction) || [];
    
    for (const rule of jurisdictionRules) {
      // Apply jurisdiction-specific validation logic
      // This would be more complex in a real implementation
    }
  }

  private async generateRecommendations(config: ValidationConfig, result: ValidationResult): Promise<void> {
    const structureTypes = config.nodes.map(node => node.data.structure.tipo);
    
    // Recommend complementary structures
    if (structureTypes.includes('BDAO_SAC') && !structureTypes.includes('WYOMING_DAO_LLC')) {
      result.recommendations.push({
        id: 'recommend-wyoming-dao',
        title: 'Consider Wyoming DAO LLC',
        description: 'Adding Wyoming DAO LLC would provide better US tax efficiency',
        type: 'structure',
        priority: 'medium',
        estimatedBenefit: 'Improved tax efficiency and operational flexibility',
        implementationComplexity: 'medium'
      });
    }
    
    // Recommend optimization
    if (config.nodes.length > 5) {
      result.recommendations.push({
        id: 'simplify-structure',
        title: 'Consider Simplifying Structure',
        description: 'Complex structures may increase compliance costs',
        type: 'optimization',
        priority: 'low',
        estimatedBenefit: 'Reduced compliance costs and complexity',
        implementationComplexity: 'low'
      });
    }
  }

  private calculateValidationScore(result: ValidationResult): number {
    let score = 100;
    
    // Deduct points for issues
    score -= result.errors.length * 20;
    score -= result.warnings.length * 10;
    score -= result.suggestions.length * 5;
    
    return Math.max(0, score);
  }

  private generateCacheKey(config: ValidationConfig): string {
    const nodeTypes = config.nodes.map(n => n.data.structure.tipo).sort();
    const edgeTypes = config.edges.map(e => e.type).sort();
    const context = JSON.stringify(config.context);
    
    return `${nodeTypes.join('-')}_${edgeTypes.join('-')}_${context}`;
  }

  // Public utility methods
  clearCache(): void {
    this.ruleCache.clear();
  }

  async refreshRules(): Promise<void> {
    await this.loadValidationRules();
    this.clearCache();
  }

  getRulesByCategory(category: string): ValidationRule[] {
    return this.rules.filter(rule => rule.category === category);
  }

  getRulesByJurisdiction(jurisdiction: string): ValidationRule[] {
    return this.jurisdictionRules.get(jurisdiction) || [];
  }
}

// Create singleton instance
export const validationEngine = new ValidationService();

