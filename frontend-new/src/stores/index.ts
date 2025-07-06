import { defineStore } from 'pinia';
import { ref, computed, nextTick } from 'vue';
import type { 
  LegalStructure, 
  Configuration, 
  ValidationResult, 
  Template, 
  StructureFilters,
  TemplateFilters,
  SiriusNode,
  SiriusEdge,
  Position,
  PricingScenario
} from '@/types';
import { apiService } from '@/services/api';
import { validationEngine } from '@/services/validation';
import { generateId } from '@/utils/helpers';

export const useSiriusStore = defineStore('sirius', () => {
  // State
  const structures = ref<LegalStructure[]>([]);
  const currentConfiguration = ref<Configuration | null>(null);
  const validationResults = ref<ValidationResult | null>(null);
  const templates = ref<Template[]>([]);
  const selectedStructure = ref<LegalStructure | null>(null);
  const selectedNodes = ref<string[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  
  // Filters
  const structureFilters = ref<StructureFilters>({});
  const templateFilters = ref<TemplateFilters>({});
  
  // UI State
  const sidebarOpen = ref(true);
  const mobileMenuOpen = ref(false);
  const currentPricingScenario = ref<PricingScenario>({
    id: 'basic',
    name: 'Basic Scenario',
    multiplier: 1.0,
    description: 'Basic setup costs only'
  });
  
  // Pricing scenarios
  const pricingScenarios = ref<PricingScenario[]>([
    {
      id: 'basic',
      name: 'Basic Scenario',
      multiplier: 1.0,
      description: 'Basic setup costs only'
    },
    {
      id: 'complete',
      name: 'Complete Scenario',
      multiplier: 1.5,
      description: 'Includes all necessary services'
    },
    {
      id: 'premium',
      name: 'Premium Scenario',
      multiplier: 2.2,
      description: 'Premium service with ongoing support'
    }
  ]);
  
  // Getters
  const filteredStructures = computed(() => {
    let filtered = structures.value.filter(structure => structure.ativo);
    
    if (structureFilters.value.tipo) {
      filtered = filtered.filter(s => s.tipo === structureFilters.value.tipo);
    }
    
    if (structureFilters.value.complexidade) {
      filtered = filtered.filter(s => s.complexidade <= structureFilters.value.complexidade!);
    }
    
    if (structureFilters.value.custo_max) {
      filtered = filtered.filter(s => s.custo_base <= structureFilters.value.custo_max!);
    }
    
    if (structureFilters.value.search) {
      const search = structureFilters.value.search.toLowerCase();
      filtered = filtered.filter(s => 
        s.nome.toLowerCase().includes(search) ||
        s.descricao.toLowerCase().includes(search) ||
        s.tipo.toLowerCase().includes(search)
      );
    }
    
    return filtered;
  });
  
  const filteredTemplates = computed(() => {
    let filtered = templates.value.filter(template => template.ativo);
    
    if (templateFilters.value.categoria) {
      filtered = filtered.filter(t => t.categoria === templateFilters.value.categoria);
    }
    
    if (templateFilters.value.complexidade) {
      filtered = filtered.filter(t => t.complexidade_template === templateFilters.value.complexidade);
    }
    
    if (templateFilters.value.search) {
      const search = templateFilters.value.search.toLowerCase();
      filtered = filtered.filter(t => 
        t.nome.toLowerCase().includes(search) ||
        t.descricao.toLowerCase().includes(search)
      );
    }
    
    return filtered.sort((a, b) => b.uso_count - a.uso_count);
  });
  
  const configurationCost = computed(() => {
    if (!currentConfiguration.value) return 0;
    
    const baseCost = currentConfiguration.value.nodes.reduce(
      (total, node) => total + node.data.structure.custo_base, 
      0
    );
    
    return baseCost * currentPricingScenario.value.multiplier;
  });
  
  const configurationMaintenanceCost = computed(() => {
    if (!currentConfiguration.value) return 0;
    
    const maintenanceCost = currentConfiguration.value.nodes.reduce(
      (total, node) => total + node.data.structure.custo_manutencao, 
      0
    );
    
    return maintenanceCost * currentPricingScenario.value.multiplier;
  });
  
  const implementationTime = computed(() => {
    if (!currentConfiguration.value) return 0;
    
    return Math.max(
      ...currentConfiguration.value.nodes.map(node => node.data.structure.tempo_implementacao),
      0
    );
  });
  
  const isConfigurationValid = computed(() => {
    return validationResults.value?.isValid ?? true;
  });
  
  const hasErrors = computed(() => {
    return validationResults.value?.errors.length ?? 0 > 0;
  });
  
  const hasWarnings = computed(() => {
    return validationResults.value?.warnings.length ?? 0 > 0;
  });
  
  // Actions
  async function loadStructures() {
    loading.value = true;
    error.value = null;
    
    try {
      // Use mock data for development
      const { mockStructures } = await import('@/data/mockData');
      structures.value = mockStructures;
      
      // In production, use API:
      // structures.value = await apiService.getStructures();
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load structures';
      console.error('Error loading structures:', err);
    } finally {
      loading.value = false;
    }
  }
  
  async function loadTemplates() {
    loading.value = true;
    error.value = null;
    
    try {
      // Use mock data for development
      const { mockTemplates } = await import('@/data/mockData');
      templates.value = mockTemplates;
      
      // In production, use API:
      // templates.value = await apiService.getTemplates();
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load templates';
      console.error('Error loading templates:', err);
    } finally {
      loading.value = false;
    }
  }
  
  async function validateCurrentConfiguration() {
    if (!currentConfiguration.value) {
      validationResults.value = null;
      return;
    }
    
    try {
      validationResults.value = await validationEngine.validateConfiguration({
        nodes: currentConfiguration.value.nodes,
        edges: currentConfiguration.value.edges,
        context: {
          jurisdiction: 'US', // TODO: Get from user context
          userType: 'business',
          complianceLevel: 'standard'
        }
      });
    } catch (err) {
      console.error('Error validating configuration:', err);
      validationResults.value = {
        isValid: false,
        score: 0,
        errors: [{
          id: 'validation-error',
          type: 'error',
          severity: 'critical',
          title: 'Validation Error',
          description: 'Failed to validate configuration',
          affectedNodes: [],
          affectedEdges: [],
          rule: {} as any
        }],
        warnings: [],
        suggestions: [],
        recommendations: []
      };
    }
  }
  
  function addStructureToCanvas(structure: LegalStructure, position: Position) {
    if (!currentConfiguration.value) {
      currentConfiguration.value = {
        nodes: [],
        edges: [],
        metadata: {
          name: 'New Configuration',
          created_at: new Date().toISOString()
        }
      };
    }
    
    const node: SiriusNode = {
      id: generateId(),
      type: 'structure',
      position,
      data: {
        structure,
        selected: false
      }
    };
    
    currentConfiguration.value.nodes.push(node);
    
    // Validate after adding
    nextTick(() => validateCurrentConfiguration());
  }
  
  function removeStructureFromCanvas(nodeId: string) {
    if (!currentConfiguration.value) return;
    
    // Remove node
    currentConfiguration.value.nodes = currentConfiguration.value.nodes.filter(
      node => node.id !== nodeId
    );
    
    // Remove connected edges
    currentConfiguration.value.edges = currentConfiguration.value.edges.filter(
      edge => edge.source !== nodeId && edge.target !== nodeId
    );
    
    // Clear selection if removed node was selected
    selectedNodes.value = selectedNodes.value.filter(id => id !== nodeId);
    
    // Validate after removal
    nextTick(() => validateCurrentConfiguration());
  }
  
  function updateNodePosition(nodeId: string, position: Position) {
    if (!currentConfiguration.value) return;
    
    const node = currentConfiguration.value.nodes.find(n => n.id === nodeId);
    if (node) {
      node.position = position;
    }
  }
  
  function addConnection(sourceId: string, targetId: string, type: string = 'ownership') {
    if (!currentConfiguration.value) return;
    
    const edge: SiriusEdge = {
      id: generateId(),
      source: sourceId,
      target: targetId,
      type: type as any,
      data: {
        connectionType: type as any
      }
    };
    
    currentConfiguration.value.edges.push(edge);
    
    // Validate after adding connection
    nextTick(() => validateCurrentConfiguration());
  }
  
  function removeConnection(edgeId: string) {
    if (!currentConfiguration.value) return;
    
    currentConfiguration.value.edges = currentConfiguration.value.edges.filter(
      edge => edge.id !== edgeId
    );
    
    // Validate after removal
    nextTick(() => validateCurrentConfiguration());
  }
  
  function selectStructure(structure: LegalStructure | null) {
    selectedStructure.value = structure;
  }
  
  function selectNode(nodeId: string) {
    selectedNodes.value = [nodeId];
  }
  
  function selectMultipleNodes(nodeIds: string[]) {
    selectedNodes.value = nodeIds;
  }
  
  function clearSelection() {
    selectedNodes.value = [];
    selectedStructure.value = null;
  }
  
  function clearCanvas() {
    currentConfiguration.value = null;
    validationResults.value = null;
    clearSelection();
  }
  
  async function saveTemplate(name: string, description: string, category: string) {
    if (!currentConfiguration.value) return;
    
    try {
      const template = await apiService.saveTemplate({
        nome: name,
        descricao: description,
        categoria: category as any,
        complexidade_template: 'INTERMEDIATE',
        configuracao: currentConfiguration.value
      });
      
      templates.value.push(template);
      return template;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to save template';
      throw err;
    }
  }
  
  async function loadTemplate(templateId: number) {
    try {
      const template = await apiService.getTemplate(templateId);
      currentConfiguration.value = template.configuracao;
      
      // Increment usage count
      const templateIndex = templates.value.findIndex(t => t.id === templateId);
      if (templateIndex !== -1) {
        templates.value[templateIndex].uso_count++;
      }
      
      // Validate loaded configuration
      await validateCurrentConfiguration();
      
      return template;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load template';
      throw err;
    }
  }
  
  function setPricingScenario(scenarioId: string) {
    const scenario = pricingScenarios.value.find(s => s.id === scenarioId);
    if (scenario) {
      currentPricingScenario.value = scenario;
    }
  }
  
  function updateStructureFilters(filters: Partial<StructureFilters>) {
    structureFilters.value = { ...structureFilters.value, ...filters };
  }
  
  function updateTemplateFilters(filters: Partial<TemplateFilters>) {
    templateFilters.value = { ...templateFilters.value, ...filters };
  }
  
  function toggleSidebar() {
    sidebarOpen.value = !sidebarOpen.value;
  }
  
  function toggleMobileMenu() {
    mobileMenuOpen.value = !mobileMenuOpen.value;
  }
  
  function closeMobileMenu() {
    mobileMenuOpen.value = false;
  }
  
  // Initialize store
  function initialize() {
    loadStructures();
    loadTemplates();
  }
  
  return {
    // State
    structures,
    currentConfiguration,
    validationResults,
    templates,
    selectedStructure,
    selectedNodes,
    loading,
    error,
    structureFilters,
    templateFilters,
    sidebarOpen,
    mobileMenuOpen,
    currentPricingScenario,
    pricingScenarios,
    
    // Getters
    filteredStructures,
    filteredTemplates,
    configurationCost,
    configurationMaintenanceCost,
    implementationTime,
    isConfigurationValid,
    hasErrors,
    hasWarnings,
    
    // Actions
    loadStructures,
    loadTemplates,
    validateCurrentConfiguration,
    addStructureToCanvas,
    removeStructureFromCanvas,
    updateNodePosition,
    addConnection,
    removeConnection,
    selectStructure,
    selectNode,
    selectMultipleNodes,
    clearSelection,
    clearCanvas,
    saveTemplate,
    loadTemplate,
    setPricingScenario,
    updateStructureFilters,
    updateTemplateFilters,
    toggleSidebar,
    toggleMobileMenu,
    closeMobileMenu,
    initialize
  };
});

