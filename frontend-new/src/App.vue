<template>
  <div id="app" class="sirius-app">
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
        <div class="canvas-wrapper">
          <SiriusCanvas />
        </div>
        
        <!-- Information Panel -->
        <InformationPanel
          v-if="selectedStructure"
          :structure="selectedStructure"
          class="information-panel"
        />
      </main>
    </div>
    
    <!-- Mobile Menu Overlay -->
    <div
      v-if="mobileMenuOpen"
      class="mobile-overlay"
      @click="closeMobileMenu"
    ></div>
    
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
        <AlertIcon class="w-5 h-5 text-red-500" />
        <span>{{ error }}</span>
        <button
          @click="clearError"
          class="error-close"
        >
          <XMarkIcon class="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useSiriusStore } from '@/stores';

// Components
import AppHeader from '@/components/layout/AppHeader.vue';
import AppSidebar from '@/components/layout/AppSidebar.vue';
import SiriusCanvas from '@/components/canvas/SiriusCanvas.vue';
import InformationPanel from '@/components/layout/InformationPanel.vue';

// Icons
const AlertIcon = { template: '<div>⚠️</div>' };
const XMarkIcon = { template: '<div>✕</div>' };

const store = useSiriusStore();

// Computed properties
const sidebarOpen = computed(() => store.sidebarOpen);
const mobileMenuOpen = computed(() => store.mobileMenuOpen);
const selectedStructure = computed(() => store.selectedStructure);
const loading = computed(() => store.loading);
const error = computed(() => store.error);

// Methods
const closeSidebar = () => {
  store.toggleSidebar();
};

const closeMobileMenu = () => {
  store.closeMobileMenu();
};

const clearError = () => {
  store.error = null;
};
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

