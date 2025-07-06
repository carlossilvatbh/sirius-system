<template>
  <div class="sirius-canvas-wrapper">
    <!-- Canvas Toolbar -->
    <CanvasToolbar
      @zoom="handleZoom"
      @fit-to-screen="fitToScreen"
      @toggle-grid="toggleGrid"
      @toggle-snap="toggleSnapToGrid"
      @save-configuration="saveConfiguration"
    />
    
    <!-- Main Canvas Area -->
    <div 
      class="sirius-canvas"
      :class="{ 'show-grid': showGrid }"
      :style="{ transform: `scale(${zoomLevel})` }"
      @drop="onDrop"
      @dragover="onDragOver"
      @click="onCanvasClick"
      ref="canvasRef"
    >
      <!-- Grid Background -->
      <div v-if="showGrid" class="canvas-grid"></div>
      
      <!-- Render all nodes -->
      <StructureNode
        v-for="node in canvasStore.nodes"
        :key="node.id"
        :node="node"
        :is-selected="node.id === canvasStore.selectedNodeId"
        @select="selectNode"
        @remove="removeNode"
      />
      
      <!-- SVG Layer for Connections -->
      <svg 
        class="connections-layer"
        :width="canvasWidth"
        :height="canvasHeight"
      >
        <defs>
          <marker
            id="arrowhead"
            markerWidth="10"
            markerHeight="7"
            refX="9"
            refY="3.5"
            orient="auto"
          >
            <polygon
              points="0 0, 10 3.5, 0 7"
              fill="#6b7280"
            />
          </marker>
        </defs>
        
        <!-- Render all edges -->
        <ConnectionEdge
          v-for="edge in canvasStore.edges"
          :key="edge.id"
          :id="edge.id"
          :source-x="getNodePosition(edge.source).x + 140"
          :source-y="getNodePosition(edge.source).y + 60"
          :target-x="getNodePosition(edge.target).x + 140"
          :target-y="getNodePosition(edge.target).y + 60"
          :type="edge.type"
          :label="getEdgeLabel(edge.type)"
          :is-selected="selectedEdgeId === edge.id"
          @select="selectEdge"
          @delete="removeEdge"
        />
        
        <!-- Temporary connection line when dragging -->
        <line
          v-if="isCreatingConnection"
          :x1="connectionStart.x"
          :y1="connectionStart.y"
          :x2="mousePosition.x"
          :y2="mousePosition.y"
          stroke="#3b82f6"
          stroke-width="2"
          stroke-dasharray="5,5"
        />
      </svg>
      
      <!-- Drop Zone Indicator -->
      <div 
        v-if="isDragOver"
        class="drop-indicator"
      >
        <div class="drop-content">
          <div class="drop-icon">📋</div>
          <div class="drop-text">Drop structure here</div>
        </div>
      </div>
    </div>
    
    <!-- Minimap -->
    <div v-if="showMinimap" class="minimap">
      <div class="minimap-content">
        <div
          v-for="node in canvasStore.nodes"
          :key="node.id"
          class="minimap-node"
          :style="{
            left: (node.position.x / canvasWidth) * 150 + 'px',
            top: (node.position.y / canvasHeight) * 100 + 'px'
          }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useCanvasStore } from '@/stores/canvas';
import { useStructuresStore } from '@/stores/structures';
import CanvasToolbar from './CanvasToolbar.vue';
import StructureNode from './StructureNode.vue';
import ConnectionEdge from './ConnectionEdge.vue';

const canvasStore = useCanvasStore();
const structuresStore = useStructuresStore();

// Refs
const canvasRef = ref<HTMLElement>();

// State
const zoomLevel = ref(1);
const showGrid = ref(true);
const snapToGrid = ref(true);
const showMinimap = ref(false);
const isDragOver = ref(false);
const selectedEdgeId = ref<string | null>(null);
const isCreatingConnection = ref(false);
const connectionStart = ref({ x: 0, y: 0 });
const mousePosition = ref({ x: 0, y: 0 });

// Canvas dimensions
const canvasWidth = ref(2000);
const canvasHeight = ref(1500);

// Methods
const handleZoom = (level: number) => {
  zoomLevel.value = level;
};

const fitToScreen = () => {
  // Implementation for fit to screen
  zoomLevel.value = 1;
};

const toggleGrid = (visible: boolean) => {
  showGrid.value = visible;
};

const toggleSnapToGrid = (enabled: boolean) => {
  snapToGrid.value = enabled;
};

const saveConfiguration = () => {
  // Implementation for saving configuration
  console.log('Saving configuration...');
};

const onDragOver = (event: DragEvent) => {
  event.preventDefault();
  isDragOver.value = true;
};

const onDrop = (event: DragEvent) => {
  event.preventDefault();
  isDragOver.value = false;
  
  const structureId = event.dataTransfer?.getData('text/plain');
  if (structureId) {
    const structure = structuresStore.getStructureById(parseInt(structureId));
    if (structure) {
      const rect = canvasRef.value?.getBoundingClientRect();
      if (rect) {
        let x = (event.clientX - rect.left) / zoomLevel.value;
        let y = (event.clientY - rect.top) / zoomLevel.value;
        
        // Snap to grid if enabled
        if (snapToGrid.value) {
          x = Math.round(x / 20) * 20;
          y = Math.round(y / 20) * 20;
        }
        
        canvasStore.addNode(structure, { x, y });
      }
    }
  }
};

const onCanvasClick = (event: MouseEvent) => {
  // Deselect nodes and edges when clicking on empty canvas
  if (event.target === canvasRef.value) {
    canvasStore.selectNode(null);
    selectedEdgeId.value = null;
  }
};

const selectNode = (nodeId: string) => {
  canvasStore.selectNode(nodeId);
  selectedEdgeId.value = null;
};

const removeNode = (nodeId: string) => {
  canvasStore.removeNode(nodeId);
};

const selectEdge = (edgeId: string) => {
  selectedEdgeId.value = edgeId;
  canvasStore.selectNode(null);
};

const removeEdge = (edgeId: string) => {
  canvasStore.removeEdge(edgeId);
  selectedEdgeId.value = null;
};

const getNodePosition = (nodeId: string) => {
  const node = canvasStore.nodes.find(n => n.id === nodeId);
  return node ? node.position : { x: 0, y: 0 };
};

const getEdgeLabel = (type: string) => {
  switch (type) {
    case 'ownership':
      return 'Owns';
    case 'control':
      return 'Controls';
    case 'beneficiary':
      return 'Benefits';
    default:
      return '';
  }
};

// Keyboard shortcuts
const handleKeydown = (event: KeyboardEvent) => {
  if (event.ctrlKey || event.metaKey) {
    switch (event.key) {
      case 'z':
        event.preventDefault();
        canvasStore.undo();
        break;
      case 'y':
        event.preventDefault();
        canvasStore.redo();
        break;
      case 's':
        event.preventDefault();
        saveConfiguration();
        break;
    }
  } else if (event.key === 'Delete' || event.key === 'Backspace') {
    if (canvasStore.selectedNodeId) {
      canvasStore.removeNode(canvasStore.selectedNodeId);
    } else if (selectedEdgeId.value) {
      removeEdge(selectedEdgeId.value);
    }
  }
};

onMounted(() => {
  document.addEventListener('keydown', handleKeydown);
  
  // Set up mouse tracking for connection creation
  document.addEventListener('mousemove', (e) => {
    mousePosition.value = { x: e.clientX, y: e.clientY };
  });
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown);
});
</script>
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

