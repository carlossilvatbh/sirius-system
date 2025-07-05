<template>
  <div class="information-panel">
    <div class="panel-header">
      <h3 class="panel-title">Structure Details</h3>
    </div>
    
    <div class="panel-content">
      <div class="structure-overview">
        <h4 class="structure-name">{{ structure.nome }}</h4>
        <p class="structure-type">{{ getStructureTypeDisplay(structure.tipo) }}</p>
        
        <div class="structure-stats">
          <div class="stat-item">
            <span class="stat-label">Base Cost:</span>
            <span class="stat-value">{{ formatCurrency(structure.custo_base) }}</span>
          </div>
          
          <div class="stat-item">
            <span class="stat-label">Maintenance:</span>
            <span class="stat-value">{{ formatCurrency(structure.custo_manutencao) }}</span>
          </div>
          
          <div class="stat-item">
            <span class="stat-label">Implementation:</span>
            <span class="stat-value">{{ structure.tempo_implementacao }} days</span>
          </div>
          
          <div class="stat-item">
            <span class="stat-label">Complexity:</span>
            <span class="stat-value">{{ getComplexityDisplay(structure.complexidade) }}</span>
          </div>
        </div>
      </div>
      
      <div class="structure-description">
        <h5 class="description-title">Description</h5>
        <p class="description-text">{{ structure.descricao }}</p>
      </div>
      
      <div class="tax-implications">
        <h5 class="section-title">Tax Implications</h5>
        <div class="tax-item">
          <span class="tax-label">USA:</span>
          <p class="tax-text">{{ structure.impacto_tributario_eua }}</p>
        </div>
        <div class="tax-item">
          <span class="tax-label">Brazil:</span>
          <p class="tax-text">{{ structure.impacto_tributario_brasil }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { LegalStructure } from '@/types';
import { getStructureTypeDisplay, formatCurrency, getComplexityDisplay } from '@/utils/helpers';

interface Props {
  structure: LegalStructure;
}

defineProps<Props>();
</script>

<style scoped>
.information-panel {
  @apply h-full overflow-y-auto;
}

.panel-header {
  @apply p-4 border-b border-gray-200;
}

.panel-title {
  @apply text-lg font-semibold text-gray-900;
}

.panel-content {
  @apply p-4 space-y-6;
}

.structure-name {
  @apply text-xl font-bold text-gray-900;
}

.structure-type {
  @apply text-sm text-gray-600 mb-4;
}

.structure-stats {
  @apply space-y-2;
}

.stat-item {
  @apply flex justify-between items-center;
}

.stat-label {
  @apply text-sm text-gray-600;
}

.stat-value {
  @apply text-sm font-semibold text-gray-900;
}

.description-title,
.section-title {
  @apply text-sm font-semibold text-gray-700 mb-2;
}

.description-text,
.tax-text {
  @apply text-sm text-gray-600 leading-relaxed;
}

.tax-item {
  @apply mb-3;
}

.tax-label {
  @apply text-sm font-medium text-gray-700;
}
</style>

