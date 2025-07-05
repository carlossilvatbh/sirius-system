<template>
  <g>
    <path
      :d="edgePath"
      :stroke="edgeColor"
      :stroke-width="strokeWidth"
      :stroke-dasharray="strokeDasharray"
      fill="none"
      marker-end="url(#arrowhead)"
    />
    
    <text
      v-if="label"
      :x="labelX"
      :y="labelY"
      class="edge-label"
      text-anchor="middle"
      dominant-baseline="middle"
    >
      {{ label }}
    </text>
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
  validationStatus?: 'valid' | 'warning' | 'error';
}

const props = defineProps<Props>();

const edgePath = computed(() => {
  const { sourceX, sourceY, targetX, targetY } = props;
  return `M ${sourceX} ${sourceY} L ${targetX} ${targetY}`;
});

const edgeColor = computed(() => {
  if (props.validationStatus === 'error') return '#ef4444';
  if (props.validationStatus === 'warning') return '#f59e0b';
  
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

