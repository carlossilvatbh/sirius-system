<template>
  <g class="connection-edge" :class="{ 'selected': isSelected }">
    <!-- Main edge path -->
    <path
      :d="edgePath"
      :stroke="edgeColor"
      :stroke-width="strokeWidth"
      :stroke-dasharray="strokeDasharray"
      fill="none"
      marker-end="url(#arrowhead)"
      class="edge-path"
      @click="selectEdge"
    />
    
    <!-- Invisible thicker path for easier selection -->
    <path
      :d="edgePath"
      stroke="transparent"
      stroke-width="12"
      fill="none"
      class="edge-selector"
      @click="selectEdge"
    />
    
    <!-- Label background -->
    <rect
      v-if="label"
      :x="labelX - labelWidth / 2"
      :y="labelY - 10"
      :width="labelWidth"
      height="20"
      rx="4"
      fill="white"
      stroke="#e5e7eb"
      stroke-width="1"
      class="label-background"
    />
    
    <!-- Label text -->
    <text
      v-if="label"
      :x="labelX"
      :y="labelY"
      class="edge-label"
      text-anchor="middle"
      dominant-baseline="middle"
      @click="selectEdge"
    >
      {{ label }}
    </text>
    
    <!-- Delete button when selected -->
    <g v-if="isSelected" class="delete-button" @click="deleteEdge">
      <circle
        :cx="labelX + labelWidth / 2 + 15"
        :cy="labelY"
        r="8"
        fill="#ef4444"
        stroke="white"
        stroke-width="2"
      />
      <text
        :x="labelX + labelWidth / 2 + 15"
        :y="labelY + 1"
        fill="white"
        text-anchor="middle"
        dominant-baseline="middle"
        font-size="10"
        font-weight="bold"
      >
        ×
      </text>
    </g>
  </g>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { ConnectionType } from '@/types';

interface Props {
  id: string;
  sourceX: number;
  sourceY: number;
  targetX: number;
  targetY: number;
  type: ConnectionType;
  label?: string;
  isSelected?: boolean;
  validationStatus?: 'valid' | 'warning' | 'error';
}

const props = withDefaults(defineProps<Props>(), {
  label: '',
  isSelected: false,
  validationStatus: 'valid'
});

const emit = defineEmits<{
  select: [edgeId: string];
  delete: [edgeId: string];
}>();

// Compute a smooth curved path
const edgePath = computed(() => {
  const { sourceX, sourceY, targetX, targetY } = props;
  
  // Calculate control points for a smooth curve
  const dx = targetX - sourceX;
  const dy = targetY - sourceY;
  
  // Control point offset for smooth curves
  const offset = Math.abs(dx) / 2;
  
  const cp1x = sourceX + offset;
  const cp1y = sourceY;
  const cp2x = targetX - offset;
  const cp2y = targetY;
  
  return `M ${sourceX} ${sourceY} C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${targetX} ${targetY}`;
});

const edgeColor = computed(() => {
  if (props.validationStatus === 'error') return '#ef4444';
  if (props.validationStatus === 'warning') return '#f59e0b';
  
  switch (props.type) {
    case 'ownership':
      return props.isSelected ? '#2563eb' : '#6b7280';
    case 'control':
      return props.isSelected ? '#7c3aed' : '#6b7280';
    case 'beneficiary':
      return props.isSelected ? '#059669' : '#6b7280';
    default:
      return props.isSelected ? '#2563eb' : '#6b7280';
  }
});

const strokeWidth = computed(() => props.isSelected ? 3 : 2);

const strokeDasharray = computed(() => {
  switch (props.type) {
    case 'control':
      return '5,5';
    case 'beneficiary':
      return '10,5';
    default:
      return 'none';
  }
});

// Calculate label position (midpoint of the edge)
const labelX = computed(() => (props.sourceX + props.targetX) / 2);
const labelY = computed(() => (props.sourceY + props.targetY) / 2);
const labelWidth = computed(() => (props.label?.length || 0) * 8 + 16);

const selectEdge = () => {
  emit('select', props.id);
};

const deleteEdge = () => {
  emit('delete', props.id);
};
</script>

<style scoped>
.connection-edge {
  cursor: pointer;
}

.edge-path {
  transition: stroke-width 0.2s ease, stroke 0.2s ease;
}

.edge-path:hover {
  stroke-width: 3;
}

.edge-selector {
  cursor: pointer;
}

.edge-label {
  font-size: 12px;
  font-weight: 500;
  fill: #374151;
  pointer-events: none;
}

.label-background {
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

.delete-button {
  cursor: pointer;
  opacity: 0.8;
  transition: opacity 0.2s ease;
}

.delete-button:hover {
  opacity: 1;
}

.connection-edge.selected .edge-path {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}
</style>
  
  const colors = {
    ownership: '#059669',
    control: '#dc2626',
    beneficiary: '#2563eb',
  };
  
  return colors[props.type] || '#6b7280';
});

const strokeWidth = computed(() => {
  return props.validationStatus === 'error' ? 3 : 2;
});

const strokeDasharray = computed(() => {
  if (props.type === 'control') return '5,5';
  if (props.type === 'beneficiary') return '2,2';
  return 'none';
});

const labelX = computed(() => {
  return (props.sourceX + props.targetX) / 2;
});

const labelY = computed(() => {
  return (props.sourceY + props.targetY) / 2;
});
</script>

<style scoped>
.edge-label {
  @apply text-xs font-medium fill-gray-700;
  pointer-events: none;
}
</style>

