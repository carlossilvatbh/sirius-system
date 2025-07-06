import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { apiService } from '@/services/api';
import type { LegalStructure } from '@/types';

export const useStructuresStore = defineStore('structures', () => {
  const structures = ref<LegalStructure[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  async function fetchStructures() {
    if (structures.value.length > 0) return;

    isLoading.value = true;
    error.value = null;
    try {
      const data = await apiService.getStructures();
      structures.value = data;
    } catch (e: any) {
      error.value = e.message || 'Failed to fetch structures';
    } finally {
      isLoading.value = false;
    }
  }

  const structureMap = computed(() => {
    return new Map(structures.value.map((s) => [s.id, s]));
  });

  function getStructureById(id: number): LegalStructure | undefined {
    return structureMap.value.get(id);
  }

  return {
    structures,
    isLoading,
    error,
    fetchStructures,
    getStructureById,
  };
});
