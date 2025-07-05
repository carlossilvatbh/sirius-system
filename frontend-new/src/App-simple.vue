<template>
  <div id="app" class="sirius-app">
    <!-- Header -->
    <header class="app-header">
      <div class="header-content">
        <div class="header-left">
          <button @click="toggleSidebar" class="sidebar-toggle">☰</button>
          <div class="logo">
            <h1 class="logo-text">Sirius 2.0</h1>
          </div>
        </div>
        
        <div class="header-center">
          <h2 class="page-title">Legal Structure Configuration Platform</h2>
        </div>
        
        <div class="header-right">
          <button class="btn-secondary">Save Configuration</button>
          <button class="btn-primary">Generate PDF</button>
        </div>
      </div>
    </header>
    
    <!-- Main Content -->
    <div class="app-content">
      <!-- Sidebar -->
      <aside :class="sidebarClasses">
        <div class="sidebar-content">
          <div class="sidebar-section">
            <h3 class="section-title">Legal Structures</h3>
            <div class="structures-list">
              <div
                v-for="structure in structures"
                :key="structure.id"
                class="structure-item"
                @click="selectStructure(structure)"
                :class="{ active: selectedStructure?.id === structure.id }"
              >
                <div class="structure-info">
                  <h4 class="structure-name">{{ structure.nome }}</h4>
                  <p class="structure-type">{{ structure.tipo }}</p>
                  <p class="structure-cost">${{ structure.custo_base.toLocaleString() }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </aside>
      
      <!-- Main Canvas Area -->
      <main class="main-content">
        <div class="canvas-wrapper">
          <div class="canvas-area">
            <div class="canvas-header">
              <h3>Configuration Canvas</h3>
              <div class="canvas-tools">
                <button class="tool-btn">🔍 Fit View</button>
                <button class="tool-btn">📐 Auto Layout</button>
                <button class="tool-btn">🗑️ Clear</button>
              </div>
            </div>
            
            <div class="canvas-content">
              <div v-if="selectedStructure" class="canvas-placeholder">
                <div class="structure-preview">
                  <h4>{{ selectedStructure.nome }}</h4>
                  <p>{{ selectedStructure.descricao }}</p>
                  <div class="structure-stats">
                    <div class="stat">
                      <span class="label">Cost:</span>
                      <span class="value">${{ selectedStructure.custo_base.toLocaleString() }}</span>
                    </div>
                    <div class="stat">
                      <span class="label">Time:</span>
                      <span class="value">{{ selectedStructure.tempo_implementacao }} days</span>
                    </div>
                    <div class="stat">
                      <span class="label">Complexity:</span>
                      <span class="value">{{ selectedStructure.complexidade }}/5</span>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="canvas-empty">
                <div class="empty-state">
                  <h3>Welcome to Sirius 2.0</h3>
                  <p>Select a legal structure from the sidebar to begin configuration</p>
                  <div class="features">
                    <div class="feature">✨ Modern Vue 3 + TypeScript</div>
                    <div class="feature">🎨 Tailwind CSS Design System</div>
                    <div class="feature">⚡ Vite Build System</div>
                    <div class="feature">🔄 Real-time Validation</div>
                    <div class="feature">📱 Mobile Responsive</div>
                    <div class="feature">♿ Accessibility Compliant</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

interface LegalStructure {
  id: number;
  nome: string;
  tipo: string;
  descricao: string;
  custo_base: number;
  tempo_implementacao: number;
  complexidade: number;
}

// State
const sidebarOpen = ref(true);
const loading = ref(true);
const selectedStructure = ref<LegalStructure | null>(null);
const structures = ref<LegalStructure[]>([]);

// Computed
const sidebarClasses = computed(() => [
  'app-sidebar',
  'bg-white',
  'border-r',
  'border-gray-200',
  'transition-all',
  'duration-300',
  {
    'w-80': sidebarOpen.value,
    'w-0 overflow-hidden': !sidebarOpen.value,
  }
]);

// Methods
const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value;
};

const selectStructure = (structure: LegalStructure) => {
  selectedStructure.value = structure;
};

const loadMockData = () => {
  structures.value = [
    {
      id: 1,
      nome: "Bahamas DAO SAC",
      tipo: "BDAO_SAC",
      descricao: "Segregated Account Company in the Bahamas designed for DAO operations with enhanced privacy and asset protection.",
      custo_base: 15000,
      tempo_implementacao: 45,
      complexidade: 4
    },
    {
      id: 2,
      nome: "Wyoming DAO LLC",
      tipo: "WYOMING_DAO_LLC",
      descricao: "Limited Liability Company in Wyoming specifically designed for Decentralized Autonomous Organizations.",
      custo_base: 8000,
      tempo_implementacao: 21,
      complexidade: 3
    },
    {
      id: 3,
      nome: "BTS Vault",
      tipo: "BTS_VAULT",
      descricao: "Bitcoin Treasury Services vault solution for institutional-grade cryptocurrency storage and management.",
      custo_base: 25000,
      tempo_implementacao: 60,
      complexidade: 5
    },
    {
      id: 4,
      nome: "Wyoming Foundation",
      tipo: "WYOMING_FOUNDATION",
      descricao: "Private foundation in Wyoming for charitable, educational, or family purposes with perpetual existence.",
      custo_base: 12000,
      tempo_implementacao: 35,
      complexidade: 4
    },
    {
      id: 5,
      nome: "Wyoming Corporation",
      tipo: "WYOMING_CORP",
      descricao: "C-Corporation in Wyoming providing strong asset protection and business flexibility.",
      custo_base: 6000,
      tempo_implementacao: 14,
      complexidade: 2
    }
  ];
};

// Lifecycle
onMounted(() => {
  setTimeout(() => {
    loadMockData();
    loading.value = false;
  }, 1500);
});
</script>

<style scoped>
.sirius-app {
  @apply h-screen flex flex-col bg-gray-50 font-sans;
}

.app-header {
  @apply bg-white border-b border-gray-200 px-6 py-4 shadow-sm;
}

.header-content {
  @apply flex items-center justify-between;
}

.header-left {
  @apply flex items-center gap-4;
}

.sidebar-toggle {
  @apply p-2 rounded-lg hover:bg-gray-100 transition-colors text-lg;
}

.logo-text {
  @apply text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent;
}

.page-title {
  @apply text-lg font-semibold text-gray-700;
}

.header-right {
  @apply flex items-center gap-3;
}

.btn-primary {
  @apply bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200;
}

.btn-secondary {
  @apply bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg transition-colors duration-200;
}

.app-content {
  @apply flex-1 flex overflow-hidden;
}

.app-sidebar {
  @apply h-full overflow-y-auto;
}

.sidebar-content {
  @apply p-6 space-y-6;
}

.section-title {
  @apply text-sm font-semibold text-gray-700 uppercase tracking-wide mb-4;
}

.structures-list {
  @apply space-y-3;
}

.structure-item {
  @apply p-4 bg-gray-50 rounded-xl cursor-pointer hover:bg-blue-50 hover:border-blue-200 transition-all duration-200 border-2 border-transparent;
}

.structure-item.active {
  @apply bg-blue-50 border-blue-300 ring-2 ring-blue-200;
}

.structure-name {
  @apply text-sm font-semibold text-gray-900 mb-1;
}

.structure-type {
  @apply text-xs text-blue-600 font-medium mb-2;
}

.structure-cost {
  @apply text-xs font-bold text-green-600;
}

.main-content {
  @apply flex-1 flex flex-col;
}

.canvas-wrapper {
  @apply flex-1 p-6;
}

.canvas-area {
  @apply bg-white rounded-xl shadow-sm border border-gray-200 h-full flex flex-col;
}

.canvas-header {
  @apply p-6 border-b border-gray-200 flex justify-between items-center;
}

.canvas-tools {
  @apply flex gap-2;
}

.tool-btn {
  @apply px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors;
}

.canvas-content {
  @apply flex-1 p-6 flex items-center justify-center;
}

.canvas-empty {
  @apply text-center;
}

.empty-state h3 {
  @apply text-2xl font-bold text-gray-900 mb-2;
}

.empty-state p {
  @apply text-gray-600 mb-8;
}

.features {
  @apply grid grid-cols-2 gap-4 max-w-md mx-auto;
}

.feature {
  @apply text-sm text-gray-700 bg-gray-50 px-3 py-2 rounded-lg;
}

.structure-preview {
  @apply bg-gradient-to-br from-blue-50 to-purple-50 p-8 rounded-xl border border-blue-200 max-w-md;
}

.structure-preview h4 {
  @apply text-xl font-bold text-gray-900 mb-3;
}

.structure-preview p {
  @apply text-gray-600 mb-6 leading-relaxed;
}

.structure-stats {
  @apply space-y-3;
}

.stat {
  @apply flex justify-between items-center;
}

.stat .label {
  @apply text-sm font-medium text-gray-600;
}

.stat .value {
  @apply text-sm font-bold text-gray-900;
}

.loading-overlay {
  @apply fixed inset-0 bg-white bg-opacity-95 flex items-center justify-center z-50;
}

.loading-spinner {
  @apply text-center;
}

.spinner {
  @apply w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4;
}

.loading-text {
  @apply text-gray-600 font-medium;
}

/* Responsive */
@media (max-width: 1024px) {
  .app-sidebar {
    @apply absolute left-0 top-0 bottom-0 z-30 shadow-lg;
  }
  
  .header-center {
    @apply hidden;
  }
  
  .features {
    @apply grid-cols-1;
  }
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.structure-preview {
  animation: fadeIn 0.5s ease-out;
}
</style>

