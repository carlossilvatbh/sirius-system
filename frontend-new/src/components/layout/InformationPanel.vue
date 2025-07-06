<template>
  <div class="information-panel">
    <div class="panel-header">
      <h3 class="panel-title">Structure Details</h3>
    </div>
    
    <div class="panel-content">
      <div class="structure-overview">
        <h4 class="structure-name">{{ structure.nome }}</h4>
        <p class="structure-type">{{ getStructureTypeDisplay(structure.tipo) }}</p>
      </div>
      
      <div class="structure-stats">
        <div class="stat-item">
          <span class="stat-label">Base Cost</span>
          <span class="stat-value">{{ formatCurrency(structure.custo_base) }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Maintenance Cost</span>
          <span class="stat-value">{{ formatCurrency(structure.custo_manutencao) }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Implementation Time</span>
          <span class="stat-value">{{ structure.tempo_implementacao }} days</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Complexity</span>
          <span class="stat-value">{{ getComplexityDisplay(structure.complexidade) }}</span>
        </div>
      </div>

      <div class="structure-description">
        <h5 class="description-title">Description</h5>
        <p class="description-text">{{ structure.descricao }}</p>
      </div>

      <div class="tax-section">
        <h5 class="section-title">Tax Implications</h5>
        <div class="tax-item">
          <span class="tax-label">USA:</span>
          <p class="tax-text">{{ structure.impacto_tributario_eua }}</p>
        </div>
        <div class="tax-item">
          <span class="tax-label">Brazil:</span>
          <p class="tax-text">{{ structure.impacto_tributario_brasil }}</p>
        </div>
        <div v-if="structure.impacto_tributario_outros" class="tax-item">
          <span class="tax-label">Other:</span>
          <p class="tax-text">{{ structure.impacto_tributario_outros }}</p>
        </div>
      </div>

      <div class="privacy-section">
        <h5 class="section-title">Privacy Impact</h5>
        <div class="privacy-item">
          <span class="privacy-label">Privacy Level:</span>
          <p class="privacy-text">{{ structure.impacto_privacidade }}</p>
        </div>
        <div class="privacy-item">
          <span class="privacy-label">Confidentiality:</span>
          <p class="privacy-text">Level {{ structure.nivel_confidencialidade }}/10</p>
        </div>
        <div class="privacy-item">
          <span class="privacy-label">Asset Protection:</span>
          <p class="privacy-text">Level {{ structure.protecao_patrimonial }}/10</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import type { LegalStructure } from '../../types';
import { getStructureTypeDisplay, formatCurrency, getComplexityDisplay } from '../../utils/helpers';

export default defineComponent({
  name: 'InformationPanel',
  props: {
    structure: {
      type: Object as () => LegalStructure,
      required: true
    }
  },
  setup() {
    return {
      getStructureTypeDisplay,
      formatCurrency,
      getComplexityDisplay
    };
  }
});
</script>

<style scoped>
.information-panel {
  height: 100%;
  overflow-y: auto;
  background-color: #ffffff;
  border-left: 1px solid #e2e8f0;
}

.panel-header {
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
  background-color: #f7fafc;
}

.panel-title {
  font-size: 18px;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
}

.panel-content {
  padding: 20px;
}

.structure-overview {
  margin-bottom: 24px;
}

.structure-name {
  font-size: 20px;
  font-weight: 600;
  color: #2d3748;
  margin: 0 0 8px 0;
}

.structure-type {
  font-size: 14px;
  color: #718096;
  margin: 0 0 16px 0;
}

.structure-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 24px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #e2e8f0;
}

.stat-label {
  font-size: 14px;
  color: #718096;
}

.stat-value {
  font-size: 14px;
  font-weight: 600;
  color: #2d3748;
}

.structure-description,
.tax-section,
.privacy-section {
  margin-bottom: 24px;
}

.description-title,
.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #4a5568;
  margin: 0 0 8px 0;
}

.description-text,
.tax-text,
.privacy-text {
  font-size: 14px;
  color: #718096;
  line-height: 1.6;
  margin: 0;
}

.tax-item,
.privacy-item {
  margin-bottom: 12px;
}

.tax-label,
.privacy-label {
  font-size: 14px;
  font-weight: 500;
  color: #4a5568;
  display: block;
  margin-bottom: 4px;
}
</style>
