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
  ApiResponse,
  ApiError
} from '@/types';

class ApiService {
  private baseURL: string;
  private cache: Map<string, { data: any; timestamp: number; ttl: number }>;
  private defaultTTL = 5 * 60 * 1000; // 5 minutes

  constructor(baseURL: string = '') {
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
          errorData.message || `HTTP ${response.status}: ${response.statusText}`,
          response.status,
          errorData.code
        );
      }

      const data = await response.json();
      return data;
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      
      throw new ApiError(
        error instanceof Error ? error.message : 'Network error',
        0
      );
    }
  }

  private getCSRFToken(): string {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
      const [name, value] = cookie.trim().split('=');
      if (name === 'csrftoken') {
        return decodeURIComponent(value);
      }
    }
    return '';
  }

  private getCacheKey(endpoint: string, params?: any): string {
    const paramString = params ? JSON.stringify(params) : '';
    return `${endpoint}${paramString}`;
  }

  private getFromCache<T>(key: string): T | null {
    const entry = this.cache.get(key);
    if (!entry) return null;
    
    if (Date.now() - entry.timestamp > entry.ttl) {
      this.cache.delete(key);
      return null;
    }
    
    return entry.data;
  }

  private setCache<T>(key: string, data: T, ttl: number = this.defaultTTL): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl
    });
  }

  private clearCachePattern(pattern: string): void {
    for (const key of this.cache.keys()) {
      if (key.includes(pattern)) {
        this.cache.delete(key);
      }
    }
  }

  // Structures API
  async getStructures(filters?: StructureFilters): Promise<LegalStructure[]> {
    const cacheKey = this.getCacheKey('/api/estruturas/', filters);
    const cached = this.getFromCache<LegalStructure[]>(cacheKey);
    
    if (cached) {
      return cached;
    }

    const params = new URLSearchParams();
    if (filters?.tipo) params.append('tipo', filters.tipo);
    if (filters?.complexidade) params.append('complexidade', filters.complexidade.toString());
    if (filters?.custo_max) params.append('custo_max', filters.custo_max.toString());
    if (filters?.search) params.append('search', filters.search);

    const queryString = params.toString();
    const endpoint = `/api/estruturas/${queryString ? `?${queryString}` : ''}`;
    
    const data = await this.request<LegalStructure[]>(endpoint);
    this.setCache(cacheKey, data);
    
    return data;
  }

  async getStructure(id: number): Promise<LegalStructure> {
    const cacheKey = this.getCacheKey(`/api/estruturas/${id}/`);
    const cached = this.getFromCache<LegalStructure>(cacheKey);
    
    if (cached) {
      return cached;
    }

    const data = await this.request<LegalStructure>(`/api/estruturas/${id}/`);
    this.setCache(cacheKey, data);
    
    return data;
  }

  // Validation API
  async validateConfiguration(config: Configuration): Promise<ValidationResult> {
    const data = await this.request<ValidationResult>('/api/validar/', {
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

    return data;
  }

  async getValidationRules(): Promise<any[]> {
    const cacheKey = this.getCacheKey('/api/regras-validacao/');
    const cached = this.getFromCache<any[]>(cacheKey);
    
    if (cached) {
      return cached;
    }

    const data = await this.request<any[]>('/api/regras-validacao/');
    this.setCache(cacheKey, data, 10 * 60 * 1000); // Cache for 10 minutes
    
    return data;
  }

  // Templates API
  async getTemplates(filters?: TemplateFilters): Promise<Template[]> {
    const cacheKey = this.getCacheKey('/api/templates/', filters);
    const cached = this.getFromCache<Template[]>(cacheKey);
    
    if (cached) {
      return cached;
    }

    const params = new URLSearchParams();
    if (filters?.categoria) params.append('categoria', filters.categoria);
    if (filters?.complexidade) params.append('complexidade', filters.complexidade);
    if (filters?.search) params.append('search', filters.search);

    const queryString = params.toString();
    const endpoint = `/api/templates/${queryString ? `?${queryString}` : ''}`;
    
    const data = await this.request<Template[]>(endpoint);
    this.setCache(cacheKey, data);
    
    return data;
  }

  async getTemplate(id: number): Promise<Template> {
    const cacheKey = this.getCacheKey(`/api/templates/${id}/`);
    const cached = this.getFromCache<Template>(cacheKey);
    
    if (cached) {
      return cached;
    }

    const data = await this.request<Template>(`/api/templates/${id}/`);
    this.setCache(cacheKey, data);
    
    return data;
  }

  async saveTemplate(template: CreateTemplateRequest): Promise<Template> {
    const data = await this.request<Template>('/api/templates/', {
      method: 'POST',
      body: JSON.stringify(template)
    });

    // Clear templates cache
    this.clearCachePattern('/api/templates/');
    
    return data;
  }

  async updateTemplate(id: number, updates: UpdateTemplateRequest): Promise<Template> {
    const data = await this.request<Template>(`/api/templates/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(updates)
    });

    // Clear templates cache
    this.clearCachePattern('/api/templates/');
    
    return data;
  }

  async deleteTemplate(id: number): Promise<void> {
    await this.request<void>(`/api/templates/${id}/`, {
      method: 'DELETE'
    });

    // Clear templates cache
    this.clearCachePattern('/api/templates/');
  }

  // Configurations API
  async saveConfiguration(config: SaveConfigurationRequest): Promise<SavedConfiguration> {
    const data = await this.request<SavedConfiguration>('/api/configuracoes/', {
      method: 'POST',
      body: JSON.stringify(config)
    });

    return data;
  }

  async loadConfiguration(id: number): Promise<SavedConfiguration> {
    const data = await this.request<SavedConfiguration>(`/api/configuracoes/${id}/`);
    return data;
  }

  // Reports API
  async generatePDF(config: Configuration, options?: PDFOptions): Promise<Blob> {
    const response = await fetch(`${this.baseURL}/api/gerar-pdf/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getCSRFToken(),
      },
      body: JSON.stringify({
        configuracao: config,
        opcoes: options
      })
    });

    if (!response.ok) {
      throw new ApiError(`Failed to generate PDF: ${response.statusText}`, response.status);
    }

    return response.blob();
  }

  async generateReport(config: Configuration, type: ReportType): Promise<Report> {
    const data = await this.request<Report>('/api/gerar-relatorio/', {
      method: 'POST',
      body: JSON.stringify({
        configuracao: config,
        tipo: type
      })
    });

    return data;
  }

  // Jurisdiction Alerts API
  async getJurisdictionAlerts(jurisdiction?: string): Promise<JurisdictionAlert[]> {
    const cacheKey = this.getCacheKey('/api/alertas-jurisdicao/', { jurisdiction });
    const cached = this.getFromCache<JurisdictionAlert[]>(cacheKey);
    
    if (cached) {
      return cached;
    }

    const params = new URLSearchParams();
    if (jurisdiction) params.append('jurisdicao', jurisdiction);

    const queryString = params.toString();
    const endpoint = `/api/alertas-jurisdicao/${queryString ? `?${queryString}` : ''}`;
    
    const data = await this.request<JurisdictionAlert[]>(endpoint);
    this.setCache(cacheKey, data, 15 * 60 * 1000); // Cache for 15 minutes
    
    return data;
  }

  // Utility methods
  clearCache(): void {
    this.cache.clear();
  }

  getCacheStats(): { size: number; keys: string[] } {
    return {
      size: this.cache.size,
      keys: Array.from(this.cache.keys())
    };
  }
}

class ApiError extends Error {
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

// Create singleton instance
export const apiService = new ApiService();
export { ApiError };

