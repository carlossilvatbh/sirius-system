<template>
  <div class="sirius-app">
    <!-- Header -->
    <AppHeader />
    
    <!-- Main Content -->
    <div class="app-content">
      <!-- Sidebar -->
      <AppSidebar
        :open="sidebarOpen"
        @close="closeSidebar"
      />
      
      <!-- Main Canvas Area -->
      <main class="main-content">
        <SiriusCanvas class="canvas-area" />
        
        <!-- Right Panel - Validation & Information -->
        <div class="right-panel" v-if="showRightPanel">
          <ValidationPanel 
          :results="validationStore.validationResults || { isValid: true, score: 0, errors: [], warnings: [], suggestions: [] }" 
        />
        </div>
      </main>
    </div>
    
    <!-- Loading Overlay -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner">
        <div class="spinner"></div>
        <p class="loading-text">Loading Sirius...</p>
      </div>
    </div>
    
    <!-- Error Toast -->
    <div
      v-if="error"
      class="error-toast"
    >
      <div class="error-content">
        <span class="error-icon">⚠️</span>
        <span class="error-message">{{ error }}</span>
        <button
          @click="clearError"
          class="error-close"
        >
          ✕
        </button>
      </div>
    </div>
    
    <!-- Auto-save Indicator -->
    <div v-if="persistenceStore.lastSaved" class="autosave-indicator">
      <span class="autosave-icon">💾</span>
      <span class="autosave-text">
        Last saved: {{ formatLastSaved }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted } from 'vue';
import { useSiriusStore } from '@/stores';
import { useCanvasStore } from '@/stores/canvas';
import { useStructuresStore } from '@/stores/structures';
import { useValidationStore } from '@/stores/validation';
import { usePersistenceStore } from '@/stores/persistence';

// Components
import AppHeader from '@/components/layout/AppHeader.vue';
import AppSidebar from '@/components/layout/AppSidebar.vue';
import SiriusCanvas from '@/components/canvas/SiriusCanvas.vue';
import ValidationPanel from '@/components/canvas/ValidationPanel.vue';

// Stores
const siriusStore = useSiriusStore();
const canvasStore = useCanvasStore();
const structuresStore = useStructuresStore();
const validationStore = useValidationStore();
const persistenceStore = usePersistenceStore();

// Computed properties
const sidebarOpen = computed(() => siriusStore.sidebarOpen);
const loading = computed(() => structuresStore.isLoading);
const error = computed(() => structuresStore.error);
const showRightPanel = computed(() => canvasStore.nodes.length > 0);

const formatLastSaved = computed(() => {
  if (!persistenceStore.lastSaved) return '';
  const now = new Date();
  const diff = now.getTime() - persistenceStore.lastSaved.getTime();
  const minutes = Math.floor(diff / 60000);
  
  if (minutes < 1) return 'just now';
  if (minutes === 1) return '1 minute ago';
  return `${minutes} minutes ago`;
});

// Methods
const closeSidebar = () => {
  siriusStore.toggleSidebar();
};

const clearError = () => {
  structuresStore.error = null;
};

// Keyboard shortcuts
const handleKeydown = (event: KeyboardEvent) => {
  // Global shortcuts are handled in SiriusCanvas
  // This is for app-level shortcuts
  if (event.ctrlKey || event.metaKey) {
    switch (event.key) {
      case 'e':
        event.preventDefault();
        persistenceStore.exportConfiguration();
        break;
      case 'o':
        event.preventDefault();
        // Trigger file input for import
        triggerImport();
        break;
    }
  }
};

const triggerImport = () => {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.json';
  input.onchange = async (e) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (file) {
      try {
        await persistenceStore.importConfiguration(file);
        console.log('Configuration imported successfully');
      } catch (error) {
        console.error('Failed to import configuration:', error);
        structuresStore.error = 'Failed to import configuration file';
      }
    }
  };
  input.click();
};

// Handle beforeunload to warn about unsaved changes
const handleBeforeUnload = (event: BeforeUnloadEvent) => {
  if (canvasStore.nodes.length > 0) {
    event.preventDefault();
    event.returnValue = 'You have unsaved changes. Are you sure you want to leave?';
  }
};

onMounted(async () => {
  // Load initial data
  await structuresStore.fetchStructures();
  
  // Set up event listeners
  document.addEventListener('keydown', handleKeydown);
  window.addEventListener('beforeunload', handleBeforeUnload);
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown);
  window.removeEventListener('beforeunload', handleBeforeUnload);
});
</script>

<style scoped>
.sirius-app {
  @apply h-screen flex flex-col bg-gray-50;
}

.app-content {
  @apply flex-1 flex overflow-hidden;
}

.main-content {
  @apply flex-1 flex relative;
}

.canvas-wrapper {
  @apply flex-1 relative;
}

.information-panel {
  @apply w-80 border-l border-gray-200 bg-white;
}

.mobile-overlay {
  @apply fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden;
}

.loading-overlay {
  @apply fixed inset-0 bg-white bg-opacity-90 flex items-center justify-center z-50;
}

.loading-spinner {
  @apply text-center;
}

.spinner {
  @apply w-12 h-12 border-4 border-sirius-200 border-t-sirius-500 rounded-full animate-spin mx-auto mb-4;
}

.loading-text {
  @apply text-gray-600 font-medium;
}

.error-toast {
  @apply fixed bottom-4 right-4 z-50;
}

.error-content {
  @apply bg-red-50 border border-red-200 rounded-lg p-4 flex items-center gap-3 shadow-lg max-w-md;
}

.error-close {
  @apply text-red-400 hover:text-red-600 transition-colors;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .information-panel {
    @apply absolute right-0 top-0 bottom-0 z-30 shadow-lg;
    transform: translateX(100%);
    transition: transform 0.3s ease-in-out;
  }
  
  .information-panel.open {
    transform: translateX(0);
  }
}

/* Animation for error toast */
.error-toast {
  animation: slideInRight 0.3s ease-out;
}

@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Focus styles for accessibility */
button:focus,
[tabindex]:focus {
  @apply outline-none ring-2 ring-sirius-500 ring-offset-2;
}
</style>

