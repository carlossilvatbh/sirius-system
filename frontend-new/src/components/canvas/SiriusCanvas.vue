<template>
  <div class="sirius-canvas-container">
    <VueFlow
      v-model:nodes="nodes"
      v-model:edges="edges"
      :class="canvasClasses"
      :default-zoom="1"
      :min-zoom="0.1"
      :max-zoom="4"
      :snap-to-grid="snapToGrid"
      :snap-grid="[20, 20]"
      @nodes-change="onNodesChange"
      @edges-change="onEdgesChange"
      @node-click="onNodeClick"
      @edge-click="onEdgeClick"
      @pane-click="onPaneClick"
      @drop="onDrop"
      @dragover="onDragOver"
    >
      <Background
        :pattern="BackgroundVariant.Dots"
        :gap="20"
        :size="1"
        color="#e5e7eb"
      />
      
      <Controls
        :show-zoom="true"
        :show-fit-view="true"
        :show-interactive="true"
      />
      
      <MiniMap
        v-if="showMinimap"
        :node-color="getNodeColor"
        :mask-color="'rgba(255, 255, 255, 0.8)'"
        :position="'bottom-right'"
      />
      
      <!-- Custom Node Types -->
      <template #node-structure="{ data, id }">
        <StructureNode
          :id="id"
          :structure="data.structure"
          :selected="data.selected"
          :validation-status="data.validationStatus"
          @select="selectNode"
          @delete="deleteNode"
        />
      </template>
      
      <!-- Custom Edge Types -->
      <template #edge-ownership="{ id, sourceX, sourceY, targetX, targetY, data }">
        <ConnectionEdge
          :id="id"
          :source-x="sourceX"
          :source-y="sourceY"
          :target-x="targetX"
          :target-y="targetY"
          :type="'ownership'"
          :label="data?.label"
          :validation-status="data?.validationStatus"
        />
      </template>
      
      <template #edge-control="{ id, sourceX, sourceY, targetX, targetY, data }">
        <ConnectionEdge
          :id="id"
          :source-x="sourceX"
          :source-y="sourceY"
          :target-x="targetX"
          :target-y="targetY"
          :type="'control'"
          :label="data?.label"
          :validation-status="data?.validationStatus"
        />
      </template>
      
      <template #edge-beneficiary="{ id, sourceX, sourceY, targetX, targetY, data }">
        <ConnectionEdge
          :id="id"
          :source-x="sourceX"
          :source-y="sourceY"
          :target-x="targetX"
          :target-y="targetY"
          :type="'beneficiary'"
          :label="data?.label"
          :validation-status="data?.validationStatus"
        />
      </template>
    </VueFlow>
    
    <!-- Canvas Toolbar -->
    <div class="canvas-toolbar">
      <Button
        variant="secondary"
        size="sm"
        @click="fitView"
      >
        <ZoomInIcon class="w-4 h-4" />
        Fit View
      </Button>
      
      <Button
        variant="secondary"
        size="sm"
        @click="autoLayout"
      >
        <LayoutIcon class="w-4 h-4" />
        Auto Layout
      </Button>
      
      <Button
        variant="secondary"
        size="sm"
        @click="toggleMinimap"
      >
        <MapIcon class="w-4 h-4" />
        Minimap
      </Button>
      
      <Button
        variant="secondary"
        size="sm"
        @click="clearCanvas"
      >
        <TrashIcon class="w-4 h-4" />
        Clear
      </Button>
    </div>
    
    <!-- Validation Panel -->
    <ValidationPanel
      v-if="validationResults"
      :results="validationResults"
      :class="validationPanelClasses"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue';
import { VueFlow, Background, Controls, MiniMap, BackgroundVariant } from '@vue-flow/core';
import type { Node, Edge, NodeChange, EdgeChange } from '@vue-flow/core';
import { useSiriusStore } from '@/stores';
import type { LegalStructure, SiriusNode, SiriusEdge } from '@/types';
import { generateNodeId, generateEdgeId } from '@/utils/helpers';

// Components
import Button from '@/components/ui/Button.vue';
import StructureNode from './StructureNode.vue';
import ConnectionEdge from './ConnectionEdge.vue';
import ValidationPanel from './ValidationPanel.vue';

// Icons (placeholder - would use actual icon library)
const ZoomInIcon = { template: '<div>🔍</div>' };
const LayoutIcon = { template: '<div>📐</div>' };
const MapIcon = { template: '<div>🗺️</div>' };
const TrashIcon = { template: '<div>🗑️</div>' };

const store = useSiriusStore();

// Local state
const showMinimap = ref(true);
const snapToGrid = ref(true);

// Computed properties
const nodes = computed({
  get: () => store.currentConfiguration?.nodes || [],
  set: (value: SiriusNode[]) => {
    if (store.currentConfiguration) {
      store.currentConfiguration.nodes = value;
    }
  }
});

const edges = computed({
  get: () => store.currentConfiguration?.edges || [],
  set: (value: SiriusEdge[]) => {
    if (store.currentConfiguration) {
      store.currentConfiguration.edges = value;
    }
  }
});

const validationResults = computed(() => store.validationResults);

const canvasClasses = computed(() => [
  'sirius-canvas',
  'canvas-container',
  'w-full',
  'h-full',
  'bg-gray-50'
]);

const validationPanelClasses = computed(() => [
  'validation-panel',
  'absolute',
  'top-4',
  'right-4',
  'max-w-sm',
  'z-10'
]);

// Event handlers
const onNodesChange = (changes: NodeChange[]) => {
  // Handle node position updates
  changes.forEach(change => {
    if (change.type === 'position' && change.position) {
      store.updateNodePosition(change.id, change.position);
    }
  });
};

const onEdgesChange = (changes: EdgeChange[]) => {
  // Handle edge changes
  changes.forEach(change => {
    if (change.type === 'remove') {
      store.removeConnection(change.id);
    }
  });
};

const onNodeClick = (event: any) => {
  const nodeId = event.node.id;
  store.selectNode(nodeId);
};

const onEdgeClick = (event: any) => {
  // Handle edge selection
  console.log('Edge clicked:', event.edge);
};

const onPaneClick = () => {
  store.clearSelection();
};

const onDrop = (event: DragEvent) => {
  event.preventDefault();
  
  const structureData = event.dataTransfer?.getData('application/json');
  if (!structureData) return;
  
  try {
    const structure: LegalStructure = JSON.parse(structureData);
    const canvasRect = (event.target as HTMLElement).getBoundingClientRect();
    
    const position = {
      x: event.clientX - canvasRect.left,
      y: event.clientY - canvasRect.top
    };
    
    store.addStructureToCanvas(structure, position);
  } catch (error) {
    console.error('Failed to add structure to canvas:', error);
  }
};

const onDragOver = (event: DragEvent) => {
  event.preventDefault();
  event.dataTransfer!.dropEffect = 'copy';
};

// Canvas actions
const selectNode = (nodeId: string) => {
  store.selectNode(nodeId);
};

const deleteNode = (nodeId: string) => {
  store.removeStructureFromCanvas(nodeId);
};

const fitView = () => {
  // Implementation would use Vue Flow's fitView method
  console.log('Fit view');
};

const autoLayout = () => {
  // Implementation would apply automatic layout algorithm
  console.log('Auto layout');
};

const toggleMinimap = () => {
  showMinimap.value = !showMinimap.value;
};

const clearCanvas = () => {
  if (confirm('Are you sure you want to clear the canvas?')) {
    store.clearCanvas();
  }
};

const getNodeColor = (node: Node) => {
  const structureNode = node as SiriusNode;
  const validationStatus = structureNode.data.validationStatus;
  
  if (validationStatus === 'error') return '#ef4444';
  if (validationStatus === 'warning') return '#f59e0b';
  return '#10b981';
};

// Watch for validation changes and update node colors
watch(validationResults, (results) => {
  if (!results || !store.currentConfiguration) return;
  
  // Update node validation status based on validation results
  store.currentConfiguration.nodes.forEach(node => {
    const hasError = results.errors.some(error => 
      error.affectedNodes.includes(node.id)
    );
    const hasWarning = results.warnings.some(warning => 
      warning.affectedNodes.includes(node.id)
    );
    
    node.data.validationStatus = hasError ? 'error' : hasWarning ? 'warning' : 'valid';
  });
  
  // Update edge validation status
  store.currentConfiguration.edges.forEach(edge => {
    const hasError = results.errors.some(error => 
      error.affectedEdges.includes(edge.id)
    );
    const hasWarning = results.warnings.some(warning => 
      warning.affectedEdges.includes(edge.id)
    );
    
    if (edge.data) {
      edge.data.validationStatus = hasError ? 'error' : hasWarning ? 'warning' : 'valid';
    }
  });
}, { deep: true });
</script>

<style scoped>
.sirius-canvas-container {
  @apply relative w-full h-full;
}

.sirius-canvas {
  @apply w-full h-full;
}

.canvas-toolbar {
  @apply absolute top-4 left-4 flex gap-2 z-10;
}

.validation-panel {
  @apply bg-white rounded-lg shadow-lg border border-gray-200;
}

/* Vue Flow custom styles */
:deep(.vue-flow__node) {
  @apply cursor-grab;
}

:deep(.vue-flow__node.selected) {
  @apply ring-2 ring-sirius-500;
}

:deep(.vue-flow__edge) {
  @apply cursor-pointer;
}

:deep(.vue-flow__edge.selected) {
  @apply stroke-sirius-500;
}

:deep(.vue-flow__controls) {
  @apply bg-white border border-gray-200 rounded-lg shadow-md;
}

:deep(.vue-flow__minimap) {
  @apply border border-gray-200 rounded-lg shadow-md;
}

/* Custom scrollbar for canvas */
:deep(.vue-flow__pane) {
  cursor: grab;
}

:deep(.vue-flow__pane:active) {
  cursor: grabbing;
}
</style>

