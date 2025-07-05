<template>
  <div class="validation-panel">
    <div class="panel-header">
      <h3 class="panel-title">Validation Results</h3>
      <div :class="scoreClasses">
        Score: {{ results.score }}/100
      </div>
    </div>
    
    <div class="panel-content">
      <div v-if="results.errors.length > 0" class="validation-section">
        <h4 class="section-title error">Errors ({{ results.errors.length }})</h4>
        <div class="validation-items">
          <div
            v-for="error in results.errors"
            :key="error.id"
            class="validation-item error"
          >
            <div class="item-icon">❌</div>
            <div class="item-content">
              <p class="item-title">{{ error.message }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="results.warnings.length > 0" class="validation-section">
        <h4 class="section-title warning">Warnings ({{ results.warnings.length }})</h4>
        <div class="validation-items">
          <div
            v-for="warning in results.warnings"
            :key="warning.id"
            class="validation-item warning"
          >
            <div class="item-icon">⚠️</div>
            <div class="item-content">
              <p class="item-title">{{ warning.message }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="results.suggestions.length > 0" class="validation-section">
        <h4 class="section-title info">Suggestions ({{ results.suggestions.length }})</h4>
        <div class="validation-items">
          <div
            v-for="suggestion in results.suggestions"
            :key="suggestion.id"
            class="validation-item info"
          >
            <div class="item-icon">💡</div>
            <div class="item-content">
              <p class="item-title">{{ suggestion.message }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="results.isValid" class="validation-success">
        <div class="success-icon">✅</div>
        <p class="success-text">Configuration is valid!</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { ValidationResult } from '@/types';

interface Props {
  results: ValidationResult;
}

const props = defineProps<Props>();

const scoreClasses = computed(() => [
  'score-badge',
  {
    'score-high': props.results.score >= 80,
    'score-medium': props.results.score >= 60 && props.results.score < 80,
    'score-low': props.results.score < 60,
  }
]);
</script>

<style scoped>
.validation-panel {
  @apply bg-white rounded-lg shadow-lg border border-gray-200 max-w-sm;
}

.panel-header {
  @apply p-4 border-b border-gray-200 flex justify-between items-center;
}

.panel-title {
  @apply text-lg font-semibold text-gray-900;
}

.score-badge {
  @apply px-2 py-1 rounded text-sm font-medium;
}

.score-high {
  @apply bg-green-100 text-green-800;
}

.score-medium {
  @apply bg-yellow-100 text-yellow-800;
}

.score-low {
  @apply bg-red-100 text-red-800;
}

.panel-content {
  @apply p-4 space-y-4 max-h-96 overflow-y-auto;
}

.validation-section {
  @apply space-y-2;
}

.section-title {
  @apply text-sm font-semibold;
}

.section-title.error {
  @apply text-red-700;
}

.section-title.warning {
  @apply text-yellow-700;
}

.section-title.info {
  @apply text-blue-700;
}

.validation-items {
  @apply space-y-2;
}

.validation-item {
  @apply flex gap-2 p-2 rounded-lg;
}

.validation-item.error {
  @apply bg-red-50;
}

.validation-item.warning {
  @apply bg-yellow-50;
}

.validation-item.info {
  @apply bg-blue-50;
}

.item-icon {
  @apply text-sm;
}

.item-content {
  @apply flex-1;
}

.item-title {
  @apply text-sm text-gray-700;
}

.validation-success {
  @apply text-center py-4;
}

.success-icon {
  @apply text-2xl mb-2;
}

.success-text {
  @apply text-green-700 font-medium;
}
</style>

