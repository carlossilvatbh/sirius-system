<template>
  <div class="app-container">
    <!-- Header -->
    <header class="app-header">
      <div class="header-brand">
        <div class="brand-logo">
          <i class="fas fa-layer-group"></i>
        </div>
        <div class="brand-text">
          <h1>SIRIUS Canvas</h1>
          <p>Legal Structure Designer</p>
        </div>
      </div>
      
      <div class="header-actions">
        <button @click="saveConfiguration" class="btn btn-success btn-sm">
          <i class="fas fa-save"></i>
          Save
        </button>
        <button @click="generatePDF" class="btn btn-secondary btn-sm">
          <i class="fas fa-file-pdf"></i>
          Export
        </button>
      </div>
    </header>

    <!-- Main Content -->
    <main class="app-main">
      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="sidebar-header">
          <h2>Structure Library</h2>
          <p>Drag structures to canvas</p>
        </div>
        
        <div class="sidebar-content">
          <!-- Search -->
          <div class="search-container">
            <input 
              v-model="searchQuery"
              type="text"
              placeholder="Search structures..."
              class="search-input"
            >
          </div>
          
          <!-- Structure List -->
          <div class="structures-list">
            <div 
              v-for="structure in filteredStructures"
              :key="structure.id"
              class="structure-card"
              :draggable="true"
              @dragstart="startDrag(structure, $event)"
              @click="selectStructure(structure)"
            >
              <div class="structure-icon">
                <i :class="structure.icon || 'fas fa-building'"></i>
              </div>
              <div class="structure-info">
                <h3>{{ structure.nome }}</h3>
                <p>{{ structure.descricao }}</p>
                <div class="structure-meta">
                  <span class="type">{{ structure.tipo }}</span>
                  <span class="cost">${{ structure.custo_base }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </aside>

      <!-- Canvas Area -->
      <section class="canvas-area">
        <div class="canvas-toolbar">
          <button @click="clearCanvas" class="btn btn-outline btn-sm">
            <i class="fas fa-trash"></i>
            Clear
          </button>
        </div>
        
        <!-- Canvas Container -->
        <div class="canvas-container" @drop="handleDrop" @dragover.prevent @dragenter.prevent>
          <div class="canvas-content">
            <!-- Canvas Elements -->
            <div 
              v-for="element in canvasElements"
              :key="element.canvasId"
              class="canvas-element"
              :style="{ 
                left: element.x + 'px', 
                top: element.y + 'px' 
              }"
              @click="selectElement(element)"
              :class="{ selected: selectedElement?.canvasId === element.canvasId }"
            >
              <div class="element-header">
                <i :class="element.icon || 'fas fa-building'"></i>
                <span>{{ element.nome }}</span>
                <button @click.stop="removeElement(element.canvasId)" class="remove-btn">
                  <i class="fas fa-times"></i>
                </button>
              </div>
              <div class="element-body">
                <p>{{ element.descricao }}</p>
                <div class="element-meta">
                  <span class="type">{{ element.tipo }}</span>
                  <span class="cost">${{ element.custo_base }}</span>
                </div>
              </div>
            </div>
            
            <!-- Empty State -->
            <div v-if="canvasElements.length === 0" class="canvas-empty">
              <div class="icon">
                <i class="fas fa-network-wired"></i>
              </div>
              <h3>Start Building Your Structure</h3>
              <p>Drag legal structures from the sidebar to begin</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Information Panel -->
      <InformationPanel 
        v-if="selectedElement"
        :structure="selectedElement"
        class="information-panel"
      />
    </main>

    <!-- Loading Overlay -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <p>Loading SIRIUS...</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import InformationPanel from './components/layout/InformationPanel.vue';
import type { LegalStructure } from './types';

// Types
interface DisplayStructure extends LegalStructure {
  icon?: string;
}

interface CanvasElement extends DisplayStructure {
  canvasId: string;
  x: number;
  y: number;
}

// State
const loading = ref(false);
const structures = ref<DisplayStructure[]>([]);
const canvasElements = ref<CanvasElement[]>([]);
const selectedStructure = ref<DisplayStructure | null>(null);
const selectedElement = ref<CanvasElement | null>(null);
const searchQuery = ref('');

// Computed
const filteredStructures = computed(() => {
  let filtered = structures.value;

  if (searchQuery.value) {
    filtered = filtered.filter(s => 
      s.nome.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      s.descricao.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  }

  return filtered;
});

// Methods
const loadStructures = async () => {
  loading.value = true;
  try {
    const response = await fetch('/api/estruturas/');
    if (!response.ok) throw new Error('Failed to load structures');
    const data: LegalStructure[] = await response.json();
    structures.value = data.map(s => ({ 
      ...s, 
      icon: 'fas fa-building' 
    }));
  } catch (error) {
    console.error('Error loading structures:', error);
  } finally {
    loading.value = false;
  }
};

const selectStructure = (structure: DisplayStructure) => {
  selectedStructure.value = structure;
};

const selectElement = (element: CanvasElement) => {
  selectedElement.value = element;
};

const startDrag = (structure: DisplayStructure, event: DragEvent) => {
  if (event.dataTransfer) {
    event.dataTransfer.setData('application/json', JSON.stringify(structure));
  }
};

const handleDrop = (event: DragEvent) => {
  event.preventDefault();
  const data = event.dataTransfer?.getData('application/json');
  if (data) {
    const structure = JSON.parse(data) as DisplayStructure;
    const rect = (event.currentTarget as HTMLElement).getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    
    const newElement: CanvasElement = {
      ...structure,
      canvasId: `canvas-element-${Date.now()}`,
      x: x - 100,
      y: y - 50
    };
    
    canvasElements.value.push(newElement);
  }
};

const removeElement = (elementCanvasId: string) => {
  canvasElements.value = canvasElements.value.filter(e => e.canvasId !== elementCanvasId);
  if (selectedElement.value?.canvasId === elementCanvasId) {
    selectedElement.value = null;
  }
};

const clearCanvas = () => {
  canvasElements.value = [];
  selectedElement.value = null;
};

const saveConfiguration = async () => {
  console.log('Saving configuration...');
};

const generatePDF = async () => {
  console.log('Generating PDF...');
};

// Lifecycle
onMounted(() => {
  loadStructures();
});
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.app-header {
  background-color: #ffffff;
  padding: 10px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-brand {
  display: flex;
  align-items: center;
}

.brand-logo {
  font-size: 24px;
  color: #4a5568;
  margin-right: 10px;
}

.brand-text h1 {
  font-size: 18px;
  margin: 0;
  color: #2d3748;
}

.brand-text p {
  margin: 0;
  font-size: 14px;
  color: #718096;
}

.header-actions {
  display: flex;
  align-items: center;
}

.btn {
  display: inline-flex;
  align-items: center;
  padding: 8px 12px;
  margin-left: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.btn-success {
  background-color: #48bb78;
  color: #ffffff;
}

.btn-secondary {
  background-color: #3182ce;
  color: #ffffff;
}

.btn-outline {
  background-color: transparent;
  color: #4a5568;
  border: 1px solid #cbd5e0;
}

.app-main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  background-color: #f7fafc;
  border-right: 1px solid #e2e8f0;
  padding: 20px;
  width: 300px;
}

.sidebar-header h2 {
  font-size: 16px;
  margin: 0 0 10px 0;
  color: #2d3748;
}

.sidebar-header p {
  margin: 0 0 20px 0;
  font-size: 14px;
  color: #718096;
}

.search-container {
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #cbd5e0;
  border-radius: 4px;
  font-size: 14px;
}

.structures-list {
  max-height: calc(100vh - 200px);
  overflow-y: auto;
}

.structure-card {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 10px;
  display: flex;
  cursor: pointer;
  transition: box-shadow 0.3s;
}

.structure-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.structure-icon {
  font-size: 24px;
  color: #3182ce;
  margin-right: 10px;
}

.structure-info {
  flex-grow: 1;
}

.structure-info h3 {
  font-size: 16px;
  margin: 0 0 5px 0;
  color: #2d3748;
}

.structure-info p {
  margin: 0;
  font-size: 14px;
  color: #718096;
}

.structure-meta {
  margin-top: 10px;
}

.type {
  background-color: #edf2f7;
  color: #4a5568;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.cost {
  margin-left: 10px;
  font-weight: 600;
  color: #2f855a;
}

.canvas-area {
  flex-grow: 1;
  position: relative;
}

.canvas-toolbar {
  padding: 10px;
  background-color: #f7fafc;
  border-bottom: 1px solid #e2e8f0;
}

.canvas-container {
  height: calc(100% - 60px);
  overflow: hidden;
  position: relative;
}

.canvas-content {
  width: 100%;
  height: 100%;
  position: relative;
}

.canvas-element {
  position: absolute;
  background-color: #ffffff;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.3s;
  min-width: 200px;
}

.canvas-element:hover {
  border-color: #3182ce;
}

.canvas-element.selected {
  border-color: #3182ce;
  box-shadow: 0 0 0 3px rgba(49, 130, 206, 0.1);
}

.element-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.element-header i {
  color: #3182ce;
  margin-right: 8px;
}

.element-header span {
  font-weight: 600;
  color: #2d3748;
}

.remove-btn {
  background: none;
  border: none;
  color: #e53e3e;
  cursor: pointer;
  font-size: 14px;
}

.element-body p {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #718096;
}

.element-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.canvas-empty {
  text-align: center;
  padding: 50px 20px;
  color: #a0aec0;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.canvas-empty .icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.information-panel {
  width: 320px;
  border-left: 1px solid #e2e8f0;
  background-color: #ffffff;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-content {
  text-align: center;
}

.loading-spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top: 4px solid #3182ce;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
