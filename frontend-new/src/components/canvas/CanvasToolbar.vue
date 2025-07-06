<template>
  <div class="canvas-toolbar">
    <div class="toolbar-section">
      <button 
        @click="zoomIn"
        class="toolbar-btn"
        title="Zoom In"
      >
        <ZoomInIcon class="w-4 h-4" />
      </button>
      <button 
        @click="zoomOut"
        class="toolbar-btn"
        title="Zoom Out"
      >
        <ZoomOutIcon class="w-4 h-4" />
      </button>
      <button 
        @click="resetZoom"
        class="toolbar-btn"
        title="Reset Zoom"
      >
        <span class="text-xs">{{ Math.round(zoomLevel * 100) }}%</span>
      </button>
      <button 
        @click="fitToScreen"
        class="toolbar-btn"
        title="Fit to Screen"
      >
        <FitScreenIcon class="w-4 h-4" />
      </button>
    </div>
    
    <div class="toolbar-section">
      <button 
        @click="toggleGrid"
        class="toolbar-btn"
        :class="{ 'active': gridVisible }"
        title="Toggle Grid"
      >
        <GridIcon class="w-4 h-4" />
      </button>
      <button 
        @click="toggleSnap"
        class="toolbar-btn"
        :class="{ 'active': snapToGrid }"
        title="Snap to Grid"
      >
        <SnapIcon class="w-4 h-4" />
      </button>
    </div>
    
    <div class="toolbar-section">
      <button 
        @click="undo"
        class="toolbar-btn"
        :disabled="!canUndo"
        title="Undo (Ctrl+Z)"
      >
        <UndoIcon class="w-4 h-4" />
      </button>
      <button 
        @click="redo"
        class="toolbar-btn"
        :disabled="!canRedo"
        title="Redo (Ctrl+Y)"
      >
        <RedoIcon class="w-4 h-4" />
      </button>
    </div>
    
    <div class="toolbar-section">
      <button 
        @click="clearCanvas"
        class="toolbar-btn danger"
        title="Clear Canvas"
      >
        <TrashIcon class="w-4 h-4" />
      </button>
      <button 
        @click="saveConfiguration"
        class="toolbar-btn primary"
        title="Save Configuration (Ctrl+S)"
      >
        <SaveIcon class="w-4 h-4" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useCanvasStore } from '@/stores/canvas';

// Simple icon components
const ZoomInIcon = { template: '<div>🔍+</div>' };
const ZoomOutIcon = { template: '<div>🔍-</div>' };
const FitScreenIcon = { template: '<div>📐</div>' };
const GridIcon = { template: '<div>⊞</div>' };
const SnapIcon = { template: '<div>📍</div>' };
const UndoIcon = { template: '<div>↶</div>' };
const RedoIcon = { template: '<div>↷</div>' };
const TrashIcon = { template: '<div>🗑️</div>' };
const SaveIcon = { template: '<div>💾</div>' };

const canvasStore = useCanvasStore();

// State
const gridVisible = ref(true);
const snapToGrid = ref(true);
const zoomLevel = ref(1);

// Computed
const canUndo = computed(() => canvasStore.canUndo);
const canRedo = computed(() => canvasStore.canRedo);

// Methods
const zoomIn = () => {
  zoomLevel.value = Math.min(zoomLevel.value * 1.2, 3);
  emit('zoom', zoomLevel.value);
};

const zoomOut = () => {
  zoomLevel.value = Math.max(zoomLevel.value / 1.2, 0.1);
  emit('zoom', zoomLevel.value);
};

const resetZoom = () => {
  zoomLevel.value = 1;
  emit('zoom', zoomLevel.value);
};

const fitToScreen = () => {
  emit('fit-to-screen');
};

const toggleGrid = () => {
  gridVisible.value = !gridVisible.value;
  emit('toggle-grid', gridVisible.value);
};

const toggleSnap = () => {
  snapToGrid.value = !snapToGrid.value;
  emit('toggle-snap', snapToGrid.value);
};

const undo = () => {
  canvasStore.undo();
};

const redo = () => {
  canvasStore.redo();
};

const clearCanvas = () => {
  if (confirm('Are you sure you want to clear the canvas? This action cannot be undone.')) {
    canvasStore.clearCanvas();
  }
};

const saveConfiguration = () => {
  emit('save-configuration');
};

// Emit events
const emit = defineEmits<{
  zoom: [level: number];
  'fit-to-screen': [];
  'toggle-grid': [visible: boolean];
  'toggle-snap': [enabled: boolean];
  'save-configuration': [];
}>();
</script>

<style scoped>
.canvas-toolbar {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 0.5rem 1rem;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.toolbar-section {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  border-right: 1px solid #e5e7eb;
  padding-right: 1rem;
}

.toolbar-section:last-child {
  border-right: none;
  padding-right: 0;
}

.toolbar-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border-radius: 0.375rem;
  border: none;
  background: none;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.toolbar-btn:hover {
  background-color: #f3f4f6;
}

.toolbar-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.toolbar-btn:disabled:hover {
  background: transparent;
}

.toolbar-btn.active {
  background-color: #dbeafe;
  color: #2563eb;
}

.toolbar-btn.primary {
  background-color: #2563eb;
  color: white;
}

.toolbar-btn.primary:hover {
  background-color: #1d4ed8;
}

.toolbar-btn.danger {
  color: #dc2626;
}

.toolbar-btn.danger:hover {
  background-color: #fef2f2;
}
</style>
