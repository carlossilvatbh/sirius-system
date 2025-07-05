<template>
  <div
    :class="nodeClasses"
    @click="handleClick"
    @contextmenu="handleContextMenu"
  >
    <!-- Status Indicator -->
    <div :class="statusIndicatorClasses"></div>
    
    <!-- Node Header -->
    <div class="node-header">
      <div class="node-icon" :style="{ backgroundColor: structureColor }">
        <component :is="structureIcon" class="w-5 h-5 text-white" />
      </div>
      
      <div class="node-title">
        <h3 class="font-semibold text-sm text-gray-900 truncate">
          {{ structure.nome }}
        </h3>
        <p class="text-xs text-gray-500 truncate">
          {{ structureTypeDisplay }}
        </p>
      </div>
      
      <button
        v-if="selected"
        class="node-delete-btn"
        @click.stop="handleDelete"
        title="Remove structure"
      >
        <XMarkIcon class="w-4 h-4" />
      </button>
    </div>
    
    <!-- Node Content -->
    <div class="node-content">
      <div class="node-stats">
        <div class="stat-item">
          <span class="stat-label">Cost:</span>
          <span class="stat-value">{{ formatCurrency(structure.custo_base) }}</span>
        </div>
        
        <div class="stat-item">
          <span class="stat-label">Complexity:</span>
          <div class="complexity-indicator">
            <div
              v-for="i in 5"
              :key="i"
              :class="[
                'complexity-dot',
                i <= structure.complexidade ? 'active' : 'inactive'
              ]"
            ></div>
          </div>
        </div>
        
        <div class="stat-item">
          <span class="stat-label">Time:</span>
          <span class="stat-value">{{ structure.tempo_implementacao }}d</span>
        </div>
      </div>
      
      <!-- Validation Messages -->
      <div v-if="validationMessages.length > 0" class="validation-messages">
        <div
          v-for="message in validationMessages"
          :key="message.id"
          :class="[
            'validation-message',
            `validation-${message.type}`
          ]"
        >
          <component :is="getValidationIcon(message.type)" class="w-3 h-3" />
          <span class="text-xs">{{ message.title }}</span>
        </div>
      </div>
    </div>
    
    <!-- Connection Handles -->
    <Handle
      type="target"
      position="top"
      class="connection-handle connection-handle-top"
    />
    <Handle
      type="source"
      position="bottom"
      class="connection-handle connection-handle-bottom"
    />
    <Handle
      type="target"
      position="left"
      class="connection-handle connection-handle-left"
    />
    <Handle
      type="source"
      position="right"
      class="connection-handle connection-handle-right"
    />
    
    <!-- Context Menu -->
    <div
      v-if="showContextMenu"
      ref="contextMenu"
      class="context-menu"
      :style="contextMenuStyle"
    >
      <button class="context-menu-item" @click="duplicateNode">
        <DuplicateIcon class="w-4 h-4" />
        Duplicate
      </button>
      <button class="context-menu-item" @click="editNode">
        <EditIcon class="w-4 h-4" />
        Edit
      </button>
      <hr class="context-menu-divider" />
      <button class="context-menu-item text-red-600" @click="deleteNode">
        <TrashIcon class="w-4 h-4" />
        Delete
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue';
import { Handle } from '@vue-flow/core';
import type { LegalStructure, ValidationIssue } from '@/types';
import { 
  getStructureTypeDisplay, 
  getStructureTypeColor, 
  formatCurrency 
} from '@/utils/helpers';
import { useSiriusStore } from '@/stores';

// Icons (placeholder - would use actual icon library)
const XMarkIcon = { template: '<div>✕</div>' };
const DuplicateIcon = { template: '<div>📋</div>' };
const EditIcon = { template: '<div>✏️</div>' };
const TrashIcon = { template: '<div>🗑️</div>' };
const AlertIcon = { template: '<div>⚠️</div>' };
const ErrorIcon = { template: '<div>❌</div>' };
const InfoIcon = { template: '<div>ℹ️</div>' };

interface Props {
  id: string;
  structure: LegalStructure;
  selected?: boolean;
  validationStatus?: 'valid' | 'warning' | 'error';
}

interface Emits {
  (e: 'select', nodeId: string): void;
  (e: 'delete', nodeId: string): void;
  (e: 'duplicate', nodeId: string): void;
  (e: 'edit', nodeId: string): void;
}

const props = withDefaults(defineProps<Props>(), {
  selected: false,
  validationStatus: 'valid',
});

const emit = defineEmits<Emits>();

const store = useSiriusStore();

// Local state
const showContextMenu = ref(false);
const contextMenuPosition = ref({ x: 0, y: 0 });
const contextMenu = ref<HTMLElement>();

// Computed properties
const nodeClasses = computed(() => [
  'structure-node',
  'bg-white',
  'border-2',
  'rounded-lg',
  'shadow-md',
  'transition-all',
  'duration-200',
  'cursor-grab',
  'hover:shadow-lg',
  'hover:-translate-y-0.5',
  'relative',
  'min-w-[200px]',
  'max-w-[250px]',
  {
    'border-sirius-500 ring-2 ring-sirius-200': props.selected,
    'border-gray-200': !props.selected && props.validationStatus === 'valid',
    'border-yellow-400 ring-2 ring-yellow-200': props.validationStatus === 'warning',
    'border-red-400 ring-2 ring-red-200': props.validationStatus === 'error',
  }
]);

const statusIndicatorClasses = computed(() => [
  'absolute',
  'top-2',
  'right-2',
  'w-3',
  'h-3',
  'rounded-full',
  {
    'bg-green-500': props.validationStatus === 'valid',
    'bg-yellow-500': props.validationStatus === 'warning',
    'bg-red-500': props.validationStatus === 'error',
  }
]);

const structureColor = computed(() => getStructureTypeColor(props.structure.tipo));

const structureTypeDisplay = computed(() => getStructureTypeDisplay(props.structure.tipo));

const structureIcon = computed(() => {
  // Return appropriate icon based on structure type
  const icons = {
    BDAO_SAC: { template: '<div>🏛️</div>' },
    WYOMING_DAO_LLC: { template: '<div>🏢</div>' },
    BTS_VAULT: { template: '<div>🔒</div>' },
    WYOMING_FOUNDATION: { template: '<div>🏛️</div>' },
    WYOMING_CORP: { template: '<div>🏢</div>' },
    NATIONALIZATION: { template: '<div>🌍</div>' },
    FUND_TOKEN: { template: '<div>🪙</div>' },
  };
  
  return icons[props.structure.tipo] || { template: '<div>📄</div>' };
});

const validationMessages = computed(() => {
  if (!store.validationResults) return [];
  
  const allIssues = [
    ...store.validationResults.errors,
    ...store.validationResults.warnings,
    ...store.validationResults.suggestions,
  ];
  
  return allIssues.filter(issue => 
    issue.affectedNodes.includes(props.id)
  ).slice(0, 2); // Show max 2 messages
});

const contextMenuStyle = computed(() => ({
  left: `${contextMenuPosition.value.x}px`,
  top: `${contextMenuPosition.value.y}px`,
}));

// Event handlers
const handleClick = (event: MouseEvent) => {
  event.stopPropagation();
  emit('select', props.id);
};

const handleDelete = () => {
  emit('delete', props.id);
};

const handleContextMenu = (event: MouseEvent) => {
  event.preventDefault();
  event.stopPropagation();
  
  contextMenuPosition.value = {
    x: event.offsetX,
    y: event.offsetY,
  };
  
  showContextMenu.value = true;
};

const duplicateNode = () => {
  emit('duplicate', props.id);
  showContextMenu.value = false;
};

const editNode = () => {
  emit('edit', props.id);
  showContextMenu.value = false;
};

const deleteNode = () => {
  emit('delete', props.id);
  showContextMenu.value = false;
};

const getValidationIcon = (type: string) => {
  switch (type) {
    case 'error': return ErrorIcon;
    case 'warning': return AlertIcon;
    default: return InfoIcon;
  }
};

// Close context menu when clicking outside
const handleClickOutside = (event: MouseEvent) => {
  if (contextMenu.value && !contextMenu.value.contains(event.target as Node)) {
    showContextMenu.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.structure-node {
  @apply p-3 space-y-3;
}

.node-header {
  @apply flex items-start gap-2;
}

.node-icon {
  @apply w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0;
}

.node-title {
  @apply flex-1 min-w-0;
}

.node-delete-btn {
  @apply w-6 h-6 rounded-full bg-red-100 text-red-600 hover:bg-red-200 flex items-center justify-center transition-colors;
}

.node-content {
  @apply space-y-2;
}

.node-stats {
  @apply space-y-1;
}

.stat-item {
  @apply flex items-center justify-between text-xs;
}

.stat-label {
  @apply text-gray-500 font-medium;
}

.stat-value {
  @apply text-gray-900 font-semibold;
}

.complexity-indicator {
  @apply flex gap-1;
}

.complexity-dot {
  @apply w-2 h-2 rounded-full;
}

.complexity-dot.active {
  @apply bg-sirius-500;
}

.complexity-dot.inactive {
  @apply bg-gray-300;
}

.validation-messages {
  @apply space-y-1;
}

.validation-message {
  @apply flex items-center gap-1 px-2 py-1 rounded text-xs;
}

.validation-error {
  @apply bg-red-50 text-red-700;
}

.validation-warning {
  @apply bg-yellow-50 text-yellow-700;
}

.validation-suggestion {
  @apply bg-blue-50 text-blue-700;
}

.connection-handle {
  @apply w-3 h-3 border-2 border-white bg-sirius-500 rounded-full opacity-0 transition-opacity;
}

.structure-node:hover .connection-handle {
  @apply opacity-100;
}

.connection-handle-top {
  @apply -top-1.5;
}

.connection-handle-bottom {
  @apply -bottom-1.5;
}

.connection-handle-left {
  @apply -left-1.5;
}

.connection-handle-right {
  @apply -right-1.5;
}

.context-menu {
  @apply absolute bg-white border border-gray-200 rounded-lg shadow-lg py-1 z-50 min-w-[120px];
}

.context-menu-item {
  @apply w-full px-3 py-2 text-left text-sm hover:bg-gray-100 flex items-center gap-2 transition-colors;
}

.context-menu-divider {
  @apply border-gray-200 my-1;
}

/* Drag styles */
.structure-node:active {
  @apply cursor-grabbing scale-105;
}

/* Focus styles for accessibility */
.structure-node:focus {
  @apply outline-none ring-2 ring-sirius-500 ring-offset-2;
}
</style>

