<template>
  <div class="app-container">
    <!-- Enhanced Header -->
    <header class="app-header">
      <div class="header-brand">
        <button 
          class="sidebar-toggle mobile-only" 
          @click="toggleMobileSidebar"
          aria-label="Toggle sidebar"
        >
          <i class="fas fa-bars"></i>
        </button>
        <div class="brand-logo">
          <i class="fas fa-layer-group"></i>
        </div>
        <div class="brand-text">
          <h1>SIRIUS Canvas</h1>
          <p class="desktop-only">Legal Structure Designer</p>
        </div>
      </div>
      
      <div class="header-actions">
        <button 
          @click="saveConfiguration" 
          class="btn btn-success btn-sm"
          :disabled="loading"
        >
          <i class="fas fa-save"></i>
          <span class="desktop-only">Save</span>
        </button>
        <button 
          @click="generatePDF" 
          class="btn btn-secondary btn-sm"
          :disabled="loading"
        >
          <i class="fas fa-file-pdf"></i>
          <span class="desktop-only">Export</span>
        </button>
        <button 
          class="sidebar-toggle desktop-only" 
          @click="toggleSidebar"
          aria-label="Toggle sidebar"
        >
          <i class="fas fa-sidebar"></i>
        </button>
      </div>
    </header>

    <!-- Main Content -->
    <main class="app-main">
      <!-- Mobile Sidebar Overlay -->
      <div 
        v-if="showMobileSidebar" 
        class="sidebar-overlay" 
        @click="toggleMobileSidebar"
      ></div>
      
      <!-- Enhanced Sidebar -->
      <aside 
        class="sidebar" 
        :class="{ 
          'collapsed': sidebarCollapsed, 
          'mobile-open': showMobileSidebar 
        }"
      >
        <div class="sidebar-header">
          <h2>
            <i class="fas fa-layer-group"></i>
            Structure Library
          </h2>
          <p>Drag structures to canvas to build your configuration</p>
          <button 
            class="sidebar-toggle desktop-only" 
            @click="toggleSidebar"
          >
            <i class="fas fa-chevron-left"></i>
          </button>
          <button 
            class="sidebar-close mobile-only" 
            @click="toggleMobileSidebar"
          >
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <div class="sidebar-content">
          <!-- Search -->
          <div class="search-filters">
            <div class="search-container">
              <input 
                v-model="searchQuery"
                type="text"
                placeholder="Search structures..."
                class="search-input"
              >
              <i class="fas fa-search search-icon"></i>
              <button 
                v-if="searchQuery"
                @click="clearSearch"
                class="search-clear"
              >
                <i class="fas fa-times"></i>
              </button>
            </div>
            
            <!-- Filter Controls -->
            <div class="filter-controls">
              <button 
                v-for="filter in filters"
                :key="filter.value"
                @click="setFilter(filter.value)"
                :class="['filter-tag', { active: currentFilter === filter.value }]"
              >
                {{ filter.label }}
              </button>
            </div>
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
              :class="{ selected: selectedStructure?.id === structure.id }"
            >
              <div class="structure-icon">
                <i :class="structure.icon || 'fas fa-building'"></i>
              </div>
              <div class="structure-info">
                <h3>{{ structure.name }}</h3>
                <p>{{ structure.description }}</p>
                <div class="structure-meta">
                  <span class="type">{{ structure.type }}</span>
                  <span class="cost">${{ structure.cost }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Empty State -->
          <div v-if="filteredStructures.length === 0" class="empty-state">
            <div class="icon">
              <i class="fas fa-search"></i>
            </div>
            <h3>No structures found</h3>
            <p>Try adjusting your search or filter criteria</p>
          </div>
        </div>
      </aside>

      <!-- Canvas Area -->
      <section class="canvas-area">
        <!-- Toolbar -->
        <div class="canvas-toolbar">
          <div class="toolbar-section">
            <div class="btn-group">
              <button @click="clearCanvas" class="btn btn-outline btn-sm">
                <i class="fas fa-trash"></i>
                <span class="desktop-only">Clear</span>
              </button>
              <button @click="undo" class="btn btn-outline btn-sm" :disabled="!canUndo">
                <i class="fas fa-undo"></i>
              </button>
              <button @click="redo" class="btn btn-outline btn-sm" :disabled="!canRedo">
                <i class="fas fa-redo"></i>
              </button>
            </div>
            
            <div class="btn-group">
              <button @click="zoomOut" class="btn btn-outline btn-sm">
                <i class="fas fa-search-minus"></i>
              </button>
              <button @click="resetZoom" class="btn btn-outline btn-sm">
                <span>{{ Math.round(zoomLevel * 100) }}%</span>
              </button>
              <button @click="zoomIn" class="btn btn-outline btn-sm">
                <i class="fas fa-search-plus"></i>
              </button>
            </div>
            
            <button 
              @click="toggleConnectionMode" 
              class="btn btn-ghost btn-sm"
              :class="{ active: connectionMode }"
            >
              <i class="fas fa-link"></i>
              <span class="desktop-only">Connect</span>
            </button>
          </div>
          
          <div class="toolbar-separator"></div>
          
          <div class="toolbar-section">
            <div class="stats-display">
              <div class="stats-item">
                <span class="stats-label">Elements</span>
                <span class="stats-value">{{ canvasElements.length }}</span>
              </div>
              <div class="stats-item">
                <span class="stats-label">Total Cost</span>
                <span class="stats-value success">${{ totalCost }}</span>
              </div>
            </div>
            
            <select v-model="pricingScenario" class="filter-select">
              <option value="basico">Basic</option>
              <option value="completo">Complete</option>
              <option value="premium">Premium</option>
            </select>
          </div>
        </div>
        
        <!-- Connection Mode Indicator -->
        <div 
          v-if="connectionMode" 
          class="connecting-mode-indicator"
        >
          <i class="fas fa-link"></i>
          <span>Connection Mode Active</span>
        </div>
        
        <!-- Canvas Container -->
        <div 
          class="canvas-container"
          @drop="handleDrop"
          @dragover.prevent
          @dragenter.prevent
        >
          <div class="canvas-content" :style="{ transform: `scale(${zoomLevel})` }">
            <div class="canvas-grid"></div>
            <div class="canvas-elements">
              <!-- Canvas Elements -->
              <div 
                v-for="element in canvasElements"
                :key="element.id"
                class="canvas-element"
                :style="{ 
                  left: element.x + 'px', 
                  top: element.y + 'px' 
                }"
                @click="selectElement(element)"
                :class="{ selected: selectedElement?.id === element.id }"
              >
                <div class="element-header">
                  <i :class="element.icon || 'fas fa-building'"></i>
                  <span>{{ element.name }}</span>
                  <button @click="removeElement(element.id)" class="remove-btn">
                    <i class="fas fa-times"></i>
                  </button>
                </div>
                <div class="element-body">
                  <p>{{ element.description }}</p>
                  <div class="element-meta">
                    <span class="type">{{ element.type }}</span>
                    <span class="cost">${{ element.cost }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Empty State -->
            <div v-if="canvasElements.length === 0" class="canvas-empty">
              <div class="icon">
                <i class="fas fa-network-wired"></i>
              </div>
              <h3>Start Building Your Structure</h3>
              <p>Drag legal structures from the sidebar to begin designing your optimal configuration</p>
              <button class="btn btn-primary mobile-only" @click="toggleMobileSidebar">
                <i class="fas fa-plus"></i>
                Add Structure
              </button>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>

  <!-- Loading Overlay -->
  <div v-if="loading" class="loading-overlay">
    <div class="loading-content">
      <div class="loading-spinner"></div>
      <p>Loading SIRIUS...</p>
    </div>
  </div>

  <!-- Toast Notifications -->
  <div class="toast-container">
    <div 
      v-for="toast in toasts"
      :key="toast.id"
      :class="['toast', toast.type]"
    >
      <i :class="getToastIcon(toast.type)"></i>
      <span>{{ toast.message }}</span>
      <button @click="removeToast(toast.id)">
        <i class="fas fa-times"></i>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watchEffect } from 'vue'

// Types
interface Structure {
  id: string
  name: string
  description: string
  type: string
  cost: number
  icon?: string
}

interface CanvasElement extends Structure {
  x: number
  y: number
}

interface Toast {
  id: string
  message: string
  type: 'success' | 'error' | 'warning' | 'info'
}

// State
const loading = ref(false)
const structures = ref<Structure[]>([])
const canvasElements = ref<CanvasElement[]>([])
const selectedStructure = ref<Structure | null>(null)
const selectedElement = ref<CanvasElement | null>(null)
const searchQuery = ref('')
const currentFilter = ref('')
const sidebarCollapsed = ref(false)
const showMobileSidebar = ref(false)
const connectionMode = ref(false)
const zoomLevel = ref(1)
const pricingScenario = ref('basico')
const toasts = ref<Toast[]>([])

// Computed
const filteredStructures = computed(() => {
  let filtered = structures.value

  if (searchQuery.value) {
    filtered = filtered.filter(s => 
      s.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      s.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  if (currentFilter.value) {
    filtered = filtered.filter(s => s.type === currentFilter.value)
  }

  return filtered
})

const totalCost = computed(() => {
  return canvasElements.value.reduce((total, element) => total + element.cost, 0)
})

const canUndo = ref(false)
const canRedo = ref(false)

// Filters
const filters = [
  { label: 'All', value: '' },
  { label: 'DAO', value: 'BDAO_SAC' },
  { label: 'LLC', value: 'WYOMING_LLC' },
  { label: 'Foundation', value: 'FOUNDATION' },
  { label: 'Corporation', value: 'CORP' }
]

// Methods
const loadStructures = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/estruturas/')
    if (!response.ok) throw new Error('Failed to load structures')
    structures.value = await response.json()
    showToast('Structures loaded successfully', 'success')
  } catch (error) {
    console.error('Error loading structures:', error)
    showToast('Failed to load structures', 'error')
  } finally {
    loading.value = false
  }
}

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

const toggleMobileSidebar = () => {
  showMobileSidebar.value = !showMobileSidebar.value
}

const toggleConnectionMode = () => {
  connectionMode.value = !connectionMode.value
}

const clearSearch = () => {
  searchQuery.value = ''
}

const setFilter = (filter: string) => {
  currentFilter.value = filter
}

const selectStructure = (structure: Structure) => {
  selectedStructure.value = structure
}

const selectElement = (element: CanvasElement) => {
  selectedElement.value = element
}

const startDrag = (structure: Structure, event: DragEvent) => {
  if (event.dataTransfer) {
    event.dataTransfer.setData('application/json', JSON.stringify(structure))
  }
}

const handleDrop = (event: DragEvent) => {
  event.preventDefault()
  const data = event.dataTransfer?.getData('application/json')
  if (data) {
    const structure = JSON.parse(data) as Structure
    const rect = (event.currentTarget as HTMLElement).getBoundingClientRect()
    const x = event.clientX - rect.left
    const y = event.clientY - rect.top
    
    const newElement: CanvasElement = {
      ...structure,
      id: Date.now().toString(),
      x: x - 100, // Center the element
      y: y - 50
    }
    
    canvasElements.value.push(newElement)
    showToast('Structure added to canvas', 'success')
  }
}

const removeElement = (elementId: string) => {
  canvasElements.value = canvasElements.value.filter(e => e.id !== elementId)
  if (selectedElement.value?.id === elementId) {
    selectedElement.value = null
  }
  showToast('Structure removed', 'info')
}

const clearCanvas = () => {
  if (canvasElements.value.length > 0) {
    canvasElements.value = []
    selectedElement.value = null
    showToast('Canvas cleared', 'info')
  }
}

const zoomIn = () => {
  zoomLevel.value = Math.min(zoomLevel.value + 0.1, 2)
}

const zoomOut = () => {
  zoomLevel.value = Math.max(zoomLevel.value - 0.1, 0.5)
}

const resetZoom = () => {
  zoomLevel.value = 1
}

const undo = () => {
  // TODO: Implement undo functionality
  showToast('Undo functionality coming soon', 'info')
}

const redo = () => {
  // TODO: Implement redo functionality
  showToast('Redo functionality coming soon', 'info')
}

const saveConfiguration = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/salvar-configuracao/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        elements: canvasElements.value,
        scenario: pricingScenario.value
      })
    })
    
    if (!response.ok) throw new Error('Failed to save configuration')
    
    showToast('Configuration saved successfully', 'success')
  } catch (error) {
    console.error('Error saving configuration:', error)
    showToast('Failed to save configuration', 'error')
  } finally {
    loading.value = false
  }
}

const generatePDF = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/gerar-pdf/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        elements: canvasElements.value,
        scenario: pricingScenario.value
      })
    })
    
    if (!response.ok) throw new Error('Failed to generate PDF')
    
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'sirius-configuration.pdf'
    a.click()
    window.URL.revokeObjectURL(url)
    
    showToast('PDF generated successfully', 'success')
  } catch (error) {
    console.error('Error generating PDF:', error)
    showToast('Failed to generate PDF', 'error')
  } finally {
    loading.value = false
  }
}

const showToast = (message: string, type: Toast['type']) => {
  const toast: Toast = {
    id: Date.now().toString(),
    message,
    type
  }
  toasts.value.push(toast)
  
  // Auto remove after 3 seconds
  setTimeout(() => {
    removeToast(toast.id)
  }, 3000)
}

const removeToast = (toastId: string) => {
  toasts.value = toasts.value.filter(t => t.id !== toastId)
}

const getToastIcon = (type: Toast['type']) => {
  switch (type) {
    case 'success': return 'fas fa-check-circle'
    case 'error': return 'fas fa-exclamation-circle'
    case 'warning': return 'fas fa-exclamation-triangle'
    case 'info': return 'fas fa-info-circle'
    default: return 'fas fa-info-circle'
  }
}

// Lifecycle
onMounted(() => {
  loadStructures()
})

// Persist state
watchEffect(() => {
  if (canvasElements.value.length > 0) {
    localStorage.setItem('sirius-canvas-elements', JSON.stringify(canvasElements.value))
  }
})

// Load persisted state
const loadPersistedState = () => {
  const saved = localStorage.getItem('sirius-canvas-elements')
  if (saved) {
    try {
      canvasElements.value = JSON.parse(saved)
    } catch (error) {
      console.error('Error loading persisted state:', error)
    }
  }
}

onMounted(() => {
  loadPersistedState()
})
</script>
