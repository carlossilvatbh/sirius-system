<template>
  <aside :class="sidebarClasses">
    <div class="sidebar-content">
      <div class="sidebar-section">
        <h3 class="section-title">Legal Structures</h3>
        <div class="structures-list">
          <div
            v-for="structure in filteredStructures"
            :key="structure.id"
            class="structure-item"
            draggable="true"
            @dragstart="handleDragStart($event, structure)"
          >
            <div class="structure-info">
              <h4 class="structure-name">{{ structure.nome }}</h4>
              <p class="structure-type">{{ getStructureTypeDisplay(structure.tipo) }}</p>
              <p class="structure-cost">{{ formatCurrency(structure.custo_base) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useSiriusStore } from '@/stores';
import type { LegalStructure } from '@/types';
import { getStructureTypeDisplay, formatCurrency } from '@/utils/helpers';

interface Props {
  open: boolean;
}

interface Emits {
  (e: 'close'): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const store = useSiriusStore();

const sidebarClasses = computed(() => [
  'app-sidebar',
  'bg-white',
  'border-r',
  'border-gray-200',
  'transition-all',
  'duration-300',
  {
    'w-80': props.open,
    'w-0 overflow-hidden': !props.open,
  }
]);

const filteredStructures = computed(() => store.filteredStructures);

const handleDragStart = (event: DragEvent, structure: LegalStructure) => {
  if (event.dataTransfer) {
    event.dataTransfer.setData('application/json', JSON.stringify(structure));
    event.dataTransfer.effectAllowed = 'copy';
  }
};
</script>

<style scoped>
.app-sidebar {
  @apply h-full overflow-y-auto;
}

.sidebar-content {
  @apply p-4 space-y-6;
}

.sidebar-section {
  @apply space-y-3;
}

.section-title {
  @apply text-sm font-semibold text-gray-700 uppercase tracking-wide;
}

.structures-list {
  @apply space-y-2;
}

.structure-item {
  @apply p-3 bg-gray-50 rounded-lg cursor-grab hover:bg-gray-100 transition-colors;
}

.structure-item:active {
  @apply cursor-grabbing;
}

.structure-info {
  @apply space-y-1;
}

.structure-name {
  @apply text-sm font-medium text-gray-900;
}

.structure-type {
  @apply text-xs text-gray-600;
}

.structure-cost {
  @apply text-xs font-semibold text-sirius-600;
}
</style>

