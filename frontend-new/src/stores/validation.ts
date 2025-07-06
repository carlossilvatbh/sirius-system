import { defineStore } from 'pinia';
import { ref, computed, watch } from 'vue';
import { useCanvasStore } from './canvas';
import { apiService } from '@/services/api';
import type { ValidationResult, CostBreakdown } from '@/types';

export const useValidationStore = defineStore('validation', () => {
  const canvasStore = useCanvasStore();
  
  const validationResults = ref<ValidationResult | null>(null);
  const costBreakdown = ref<CostBreakdown | null>(null);
  const isValidating = ref(false);
  const isCalculatingCosts = ref(false);

  // Watch for changes in canvas and trigger validation
  watch(
    () => [canvasStore.nodes, canvasStore.edges],
    async () => {
      await validateConfiguration();
      await calculateCosts();
    },
    { deep: true }
  );

  async function validateConfiguration() {
    if (canvasStore.nodes.length === 0) {
      validationResults.value = null;
      return;
    }

    isValidating.value = true;
    try {
      const configuration = {
        nodes: canvasStore.nodes,
        edges: canvasStore.edges,
      };
      
      validationResults.value = await apiService.validateConfiguration(configuration);
    } catch (error) {
      console.error('Validation failed:', error);
      validationResults.value = {
        isValid: false,
        score: 0,
        errors: [{ 
          id: 'validation_error', 
          message: 'Failed to validate configuration', 
          structureIds: [], 
          severity: 'ERROR' as const 
        }],
        warnings: [],
        suggestions: [],
      };
    } finally {
      isValidating.value = false;
    }
  }

  async function calculateCosts() {
    if (canvasStore.nodes.length === 0) {
      costBreakdown.value = null;
      return;
    }

    isCalculatingCosts.value = true;
    try {
      // Simulate cost calculation
      const setupCost = canvasStore.nodes.reduce((sum, node) => 
        sum + node.data.structure.custo_base, 0
      );
      
      const maintenanceCost = canvasStore.nodes.reduce((sum, node) => 
        sum + (node.data.structure.custo_manutencao || 0), 0
      );

      costBreakdown.value = {
        setup_cost: setupCost,
        maintenance_cost: maintenanceCost,
        total_first_year: setupCost + maintenanceCost,
        annual_cost: maintenanceCost,
        scenario_multiplier: 1.15, // Complete scenario
        final_cost: (setupCost + maintenanceCost) * 1.15,
      };
    } catch (error) {
      console.error('Cost calculation failed:', error);
    } finally {
      isCalculatingCosts.value = false;
    }
  }  const hasErrors = computed(() => 
    validationResults.value?.errors && validationResults.value.errors.length > 0
  );
  
  const hasWarnings = computed(() => 
    validationResults.value?.warnings && validationResults.value.warnings.length > 0
  );

  const totalCost = computed(() => 
    costBreakdown.value?.final_cost || 0
  );

  return {
    validationResults,
    costBreakdown,
    isValidating,
    isCalculatingCosts,
    hasErrors,
    hasWarnings,
    totalCost,
    validateConfiguration,
    calculateCosts,
  };
});
