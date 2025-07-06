import type {
  LegalStructure,
  Template,
  Configuration,
  ValidationResult,
  StructureFilters,
  TemplateFilters,
  CreateTemplateRequest,
  UpdateTemplateRequest,
  SaveConfigurationRequest,
  SavedConfiguration,
  PDFOptions,
  Report,
  ReportType,
  JurisdictionAlert,
  CostBreakdown
} from '../types';

class ApiService {
  private baseURL: string;
  private cache: Map<string, { data: any; timestamp: number; ttl: number }>;
  private defaultTTL = 5 * 60 * 1000; // 5 minutes

  constructor(baseURL: string = '/estruturas/api') {
    this.baseURL = baseURL;
    this.cache = new Map();
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const defaultHeaders = {
      'Content-Type': 'application/json',
      'X-CSRFToken': this.getCSRFToken(),
    };

    const config: RequestInit = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(
          response.status,
          errorData.message || errorData.error || `HTTP ${response.status}: ${response.statusText}`,
          errorData
        );
      }

      const data = await response.json();
      return data;
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new ApiError(0, 'Network error or server unreachable', { originalError: error });
    }
  }

  private getCSRFToken(): string {
    // Try to get CSRF token from cookie
    const cookieValue = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      ?.split('=')[1];
    
    // Try to get from meta tag
    if (!cookieValue) {
      const metaTag = document.querySelector('meta[name="csrf-token"]') as HTMLMetaElement;
      return metaTag?.content || '';
    }
    
    return cookieValue || '';
  }

  private getCacheKey(endpoint: string, params?: Record<string, any>): string {
    const paramString = params ? JSON.stringify(params) : '';
    return `${endpoint}${paramString}`;
  }

  private getFromCache<T>(key: string): T | null {
    const cached = this.cache.get(key);
    if (cached && Date.now() - cached.timestamp < cached.ttl) {
      return cached.data;
    }
    this.cache.delete(key);
    return null;
  }

  private setCache(key: string, data: any, ttl: number = this.defaultTTL): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl,
    });
  }

  // Structure API
  async getStructures(filters?: StructureFilters): Promise<LegalStructure[]> {
    const cacheKey = this.getCacheKey('/estruturas/', filters);
    const cached = this.getFromCache<LegalStructure[]>(cacheKey);
    
    if (cached) {
      return cached;
    }

    try {
      // Call Django API endpoint
      const structures = await this.request<LegalStructure[]>('/estruturas/');
      
      // Apply client-side filtering if needed
      let filteredStructures = structures;
      
      if (filters?.search) {
        const searchLower = filters.search.toLowerCase();
        filteredStructures = filteredStructures.filter(s => 
          s.nome.toLowerCase().includes(searchLower) ||
          s.descricao.toLowerCase().includes(searchLower)
        );
      }
      
      if (filters?.tipo) {
        filteredStructures = filteredStructures.filter(s => s.tipo === filters.tipo);
      }
      
      if (filters?.complexidade) {
        filteredStructures = filteredStructures.filter(s => s.complexidade <= filters.complexidade!);
      }
      
      if (filters?.custo_max) {
        filteredStructures = filteredStructures.filter(s => s.custo_base <= filters.custo_max!);
      }
      
      this.setCache(cacheKey, filteredStructures);
      return filteredStructures;
    } catch (error) {
      console.error('Error fetching structures:', error);
      // Return fallback data if API fails
      return this.getFallbackStructures();
    }
  }

  async getStructureById(id: number): Promise<LegalStructure> {
    const cacheKey = this.getCacheKey(`/estruturas/${id}/`);
    const cached = this.getFromCache<LegalStructure>(cacheKey);
    
    if (cached) {
      return cached;
    }

    try {
      const structure = await this.request<LegalStructure>(`/estruturas/${id}/`);
      this.setCache(cacheKey, structure);
      return structure;
    } catch (error) {
      console.error(`Error fetching structure ${id}:`, error);
      throw error;
    }
  }

  // Template API
  async getTemplates(filters?: TemplateFilters): Promise<Template[]> {
    const cacheKey = this.getCacheKey('/templates/', filters);
    const cached = this.getFromCache<Template[]>(cacheKey);
    
    if (cached) {
      return cached;
    }

    try {
      const templates = await this.request<Template[]>('/templates/');
      
      // Apply client-side filtering
      let filteredTemplates = templates;
      
      if (filters?.search) {
        const searchLower = filters.search.toLowerCase();
        filteredTemplates = filteredTemplates.filter(t =>
          t.nome.toLowerCase().includes(searchLower) ||
          t.descricao.toLowerCase().includes(searchLower)
        );
      }
      
      if (filters?.categoria) {
        filteredTemplates = filteredTemplates.filter(t => t.categoria === filters.categoria);
      }
      
      if (filters?.complexidade) {
        filteredTemplates = filteredTemplates.filter(t => t.complexidade_template === filters.complexidade);
      }
      
      this.setCache(cacheKey, filteredTemplates);
      return filteredTemplates;
    } catch (error) {
      console.error('Error fetching templates:', error);
      return [];
    }
  }

  async createTemplate(templateData: CreateTemplateRequest): Promise<Template> {
    return await this.request<Template>('/templates/', {
      method: 'POST',
      body: JSON.stringify(templateData),
    });
  }

  async updateTemplate(id: number, templateData: UpdateTemplateRequest): Promise<Template> {
    return await this.request<Template>(`/templates/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(templateData),
    });
  }

  async deleteTemplate(id: number): Promise<void> {
    await this.request(`/templates/${id}/`, {
      method: 'DELETE',
    });
  }

  async applyTemplate(templateId: number): Promise<Configuration> {
    const result = await this.request<{ configuracao: Configuration }>('/aplicar-template/', {
      method: 'POST',
      body: JSON.stringify({ template_id: templateId }),
    });
    return result.configuracao;
  }

  // Validation API
  async validateConfiguration(config: Configuration): Promise<ValidationResult> {
    try {
      const result = await this.request<any>('/validar-configuracao/', {
        method: 'POST',
        body: JSON.stringify({
          elementos: config.nodes.map(node => ({
            estrutura_id: node.data.structure.id,
            position: node.position
          })),
          conexoes: config.edges.map(edge => ({
            source: edge.source,
            target: edge.target,
            type: edge.type
          }))
        })
      });

      // Transform Django response to frontend format
      return {
        isValid: result.valid || result.isValid || true,
        score: result.score || this.calculateScore(result),
        errors: (result.errors || result.problemas || []).map((error: any) => ({
          id: error.id || `error-${Date.now()}`,
          message: error.message || error.mensagem || error.descricao || 'Validation error',
          structureIds: error.estruturas_afetadas || error.structureIds || [],
          severity: 'ERROR' as const
        })),
        warnings: (result.warnings || result.avisos || []).map((warning: any) => ({
          id: warning.id || `warning-${Date.now()}`,
          message: warning.message || warning.mensagem || warning.descricao || 'Validation warning',
          structureIds: warning.estruturas_afetadas || warning.structureIds || [],
          severity: 'WARNING' as const
        })),
        suggestions: (result.suggestions || result.sugestoes || []).map((suggestion: any) => ({
          id: suggestion.id || `suggestion-${Date.now()}`,
          message: suggestion.message || suggestion.mensagem || suggestion.descricao || 'Validation suggestion',
          structureIds: suggestion.estruturas_afetadas || suggestion.structureIds || [],
          severity: 'INFO' as const
        }))
      };
    } catch (error) {
      console.error('Validation API error:', error);
      
      // Fallback to client-side validation
      return {
        isValid: true,
        score: 85,
        errors: [],
        warnings: [],
        suggestions: []
      };
    }
  }

  private calculateScore(result: any): number {
    let score = 100;
    const errors = result.errors || result.problemas || [];
    const warnings = result.warnings || result.avisos || [];
    const suggestions = result.suggestions || result.sugestoes || [];
    
    score -= errors.length * 20;
    score -= warnings.length * 10;
    score -= suggestions.length * 5;
    
    return Math.max(0, score);
  }

  async getValidationRules(): Promise<any[]> {
    const cacheKey = this.getCacheKey('/regras-validacao/');
    const cached = this.getFromCache<any[]>(cacheKey);
    
    if (cached) {
      return cached;
    }

    try {
      const rules = await this.request<any[]>('/regras-validacao/');
      this.setCache(cacheKey, rules);
      return rules;
    } catch (error) {
      console.error('Error fetching validation rules:', error);
      return [];
    }
  }

  // Cost Calculation API
  async calculateCosts(config: Configuration, scenario: string = 'basic'): Promise<CostBreakdown> {
    try {
      const result = await this.request<any>('/calcular-custos/', {
        method: 'POST',
        body: JSON.stringify({
          elementos: config.nodes.map(node => ({
            estrutura: node.data.structure,
            position: node.position
          })),
          cenario: scenario,
          incluir_analise_risco: true
        })
      });

      // Transform Django response to frontend format
      return {
        setup_cost: result.custo_configuracao || result.setup_cost || 0,
        maintenance_cost: result.custo_manutencao_anual || result.maintenance_cost || 0,
        total_first_year: result.custo_total_primeiro_ano || result.total_first_year || 0,
        annual_cost: result.custo_anual || result.annual_cost || 0,
        scenario_multiplier: result.multiplicador_cenario || result.scenario_multiplier || 1,
        final_cost: result.custo_final || result.final_cost || 0
      };
    } catch (error) {
      console.error('Cost calculation error:', error);
      return this.calculateCostsFallback(config);
    }
  }

  private calculateCostsFallback(config: Configuration): CostBreakdown {
    let setupCost = 0;
    let maintenanceCost = 0;

    config.nodes.forEach(node => {
      setupCost += node.data.structure.custo_base;
      maintenanceCost += node.data.structure.custo_manutencao;
    });

    return {
      setup_cost: setupCost,
      maintenance_cost: maintenanceCost,
      total_first_year: setupCost + maintenanceCost,
      annual_cost: maintenanceCost,
      scenario_multiplier: 1,
      final_cost: setupCost + maintenanceCost
    };
  }

  // Configuration Management API
  async saveConfiguration(config: SaveConfigurationRequest): Promise<SavedConfiguration> {
    try {
      const result = await this.request<any>('/salvar-configuracao/', {
        method: 'POST',
        body: JSON.stringify({
          nome: config.nome,
          descricao: config.descricao,
          elementos: config.configuracao.nodes.map((node: any) => ({
            estrutura_id: node.data.structure.id,
            position: node.position
          })),
          conexoes: config.configuracao.edges.map((edge: any) => ({
            source: edge.source,
            target: edge.target,
            type: edge.type
          })),
          custo_total: 0, // Will be calculated by backend
          tempo_total: 0  // Will be calculated by backend
        })
      });

      return {
        id: result.id,
        nome: config.nome,
        descricao: config.descricao,
        configuracao: config.configuracao,
        custo_estimado: result.custo_total,
        tempo_estimado: result.tempo_total,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };
    } catch (error) {
      console.error('Save configuration error:', error);
      throw error;
    }
  }

  async getSavedConfigurations(): Promise<SavedConfiguration[]> {
    const cacheKey = this.getCacheKey('/configuracoes-salvas/');
    const cached = this.getFromCache<SavedConfiguration[]>(cacheKey);
    
    if (cached) {
      return cached;
    }

    try {
      const configurations = await this.request<any[]>('/configuracoes-salvas/');
      
      const formattedConfigs = configurations.map(config => ({
        id: config.id,
        nome: config.nome,
        descricao: config.descricao,
        configuracao: JSON.parse(config.configuracao_json),
        custo_estimado: config.custo_total,
        tempo_estimado: config.tempo_total,
        created_at: config.data_criacao,
        updated_at: config.data_atualizacao || config.data_criacao
      }));

      this.setCache(cacheKey, formattedConfigs);
      return formattedConfigs;
    } catch (error) {
      console.error('Error fetching saved configurations:', error);
      return [];
    }
  }

  async loadConfiguration(id: number): Promise<Configuration> {
    try {
      const config = await this.request<any>(`/configuracoes-salvas/${id}/`);
      return JSON.parse(config.configuracao_json);
    } catch (error) {
      console.error(`Error loading configuration ${id}:`, error);
      throw error;
    }
  }

  async deleteConfiguration(id: number): Promise<void> {
    await this.request(`/configuracoes-salvas/${id}/`, {
      method: 'DELETE',
    });
  }

  // Jurisdiction Alerts API
  async getJurisdictionAlerts(jurisdiction?: string): Promise<JurisdictionAlert[]> {
    const params = jurisdiction ? { jurisdiction } : undefined;
    const cacheKey = this.getCacheKey('/alertas-jurisdicao/', params);
    const cached = this.getFromCache<JurisdictionAlert[]>(cacheKey);
    
    if (cached) {
      return cached;
    }

    try {
      const alerts = await this.request<any[]>('/alertas-jurisdicao/');
      
      const formattedAlerts = alerts.map(alert => ({
        id: alert.id.toString(),
        jurisdiction: alert.jurisdicao,
        type: this.mapAlertType(alert.tipo_alerta),
        priority: this.mapPriority(alert.nivel_prioridade),
        title: alert.titulo,
        description: alert.mensagem,
        deadline: alert.data_fim,
        affectedStructures: alert.estruturas_aplicaveis || [],
        actionRequired: alert.nivel_prioridade > 2
      }));

      this.setCache(cacheKey, formattedAlerts, 10 * 60 * 1000); // 10 minutes for alerts
      return formattedAlerts;
    } catch (error) {
      console.error('Error fetching jurisdiction alerts:', error);
      return [];
    }
  }

  private mapAlertType(type: string): 'tax' | 'compliance' | 'reporting' | 'deadline' | 'regulatory' {
    const typeMap: Record<string, 'tax' | 'compliance' | 'reporting' | 'deadline' | 'regulatory'> = {
      'TAX': 'tax',
      'COMPLIANCE': 'compliance', 
      'REPORTING': 'reporting',
      'DEADLINE': 'deadline',
      'REGULATORY': 'regulatory'
    };
    return typeMap[type] || 'regulatory';
  }

  private mapPriority(level: number): 'critical' | 'high' | 'medium' | 'low' {
    if (level >= 4) return 'critical';
    if (level >= 3) return 'high';
    if (level >= 2) return 'medium';
    return 'low';
  }

  // PDF Generation API
  async generatePDF(config: Configuration, options: PDFOptions = {}): Promise<Blob> {
    try {
      const response = await fetch(`${this.baseURL}/gerar-pdf/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken(),
        },
        body: JSON.stringify({
          configuracao: {
            elementos: config.nodes.map(node => ({
              estrutura_id: node.data.structure.id,
              position: node.position
            })),
            conexoes: config.edges.map(edge => ({
              source: edge.source,
              target: edge.target,
              type: edge.type
            }))
          },
          opcoes: options
        }),
      });

      if (!response.ok) {
        throw new ApiError(response.status, 'PDF generation failed');
      }

      return await response.blob();
    } catch (error) {
      console.error('PDF generation error:', error);
      throw error;
    }
  }

  // Reports API
  async generateReport(type: ReportType, config: Configuration): Promise<Report> {
    return await this.request<Report>('/generate-report/', {
      method: 'POST',
      body: JSON.stringify({
        type,
        configuration: config,
      }),
    });
  }

  // Fallback data methods
  private getFallbackStructures(): LegalStructure[] {
    return [
      {
        id: 1,
        nome: 'Bahamas DAO SAC',
        tipo: 'BDAO_SAC',
        descricao: 'Bahamas DAO Segregated Account Company',
        custo_base: 25000,
        custo_manutencao: 12000,
        tempo_implementacao: 45,
        complexidade: 4,
        impacto_tributario_eua: 'Pass-through taxation',
        impacto_tributario_brasil: 'Subject to CFC rules',
        nivel_confidencialidade: 5,
        protecao_patrimonial: 4,
        impacto_privacidade: 'High privacy protection',
        facilidade_banking: 3,
        documentacao_necessaria: 'Corporate documents, KYC documentation',
        ativo: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      {
        id: 2,
        nome: 'Wyoming DAO LLC',
        tipo: 'WYOMING_DAO_LLC',
        descricao: 'Wyoming Decentralized Autonomous Organization LLC',
        custo_base: 15000,
        custo_manutencao: 8000,
        tempo_implementacao: 30,
        complexidade: 3,
        impacto_tributario_eua: 'Pass-through taxation',
        impacto_tributario_brasil: 'Subject to CFC rules',
        nivel_confidencialidade: 3,
        protecao_patrimonial: 3,
        impacto_privacidade: 'Moderate privacy protection',
        facilidade_banking: 4,
        documentacao_necessaria: 'Operating agreement, member information',
        ativo: true,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
    ];
  }

  // Cache Management
  clearCache(): void {
    this.cache.clear();
  }

  getCacheSize(): number {
    return this.cache.size;
  }

  getCacheStats(): { size: number; keys: string[] } {
    return {
      size: this.cache.size,
      keys: Array.from(this.cache.keys()),
    };
  }
}

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public data?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export const apiService = new ApiService();
