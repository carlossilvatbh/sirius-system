import { defineStore } from 'pinia';
import { ref, watch } from 'vue';
import { useCanvasStore } from './canvas';

const STORAGE_KEY = 'sirius_canvas_state';

export const usePersistenceStore = defineStore('persistence', () => {
  const canvasStore = useCanvasStore();
  const lastSaved = ref<Date | null>(null);
  const autoSaveEnabled = ref(true);
  const autoSaveInterval = ref(30000); // 30 seconds

  // Watch for changes and auto-save
  watch(
    () => [canvasStore.nodes, canvasStore.edges],
    () => {
      if (autoSaveEnabled.value) {
        debounce(saveToLocalStorage, 2000)();
      }
    },
    { deep: true }
  );

  function saveToLocalStorage() {
    try {
      const state = {
        nodes: canvasStore.nodes,
        edges: canvasStore.edges,
        timestamp: new Date().toISOString(),
      };
      
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      lastSaved.value = new Date();
      console.log('Configuration auto-saved to localStorage');
    } catch (error) {
      console.error('Failed to save to localStorage:', error);
    }
  }

  function loadFromLocalStorage() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const state = JSON.parse(saved);
        
        // Restore canvas state
        canvasStore.nodes = state.nodes || [];
        canvasStore.edges = state.edges || [];
        
        lastSaved.value = new Date(state.timestamp);
        console.log('Configuration loaded from localStorage');
        return true;
      }
    } catch (error) {
      console.error('Failed to load from localStorage:', error);
    }
    return false;
  }

  function clearLocalStorage() {
    try {
      localStorage.removeItem(STORAGE_KEY);
      lastSaved.value = null;
      console.log('localStorage cleared');
    } catch (error) {
      console.error('Failed to clear localStorage:', error);
    }
  }

  function exportConfiguration() {
    const state = {
      nodes: canvasStore.nodes,
      edges: canvasStore.edges,
      metadata: {
        exported: new Date().toISOString(),
        version: '1.0.0',
      },
    };
    
    const blob = new Blob([JSON.stringify(state, null, 2)], {
      type: 'application/json',
    });
    
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `sirius-configuration-${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function importConfiguration(file: File): Promise<boolean> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      
      reader.onload = (e) => {
        try {
          const content = e.target?.result as string;
          const state = JSON.parse(content);
          
          // Validate the structure
          if (state.nodes && Array.isArray(state.nodes)) {
            canvasStore.nodes = state.nodes;
            canvasStore.edges = state.edges || [];
            
            // Save the imported state
            saveToLocalStorage();
            resolve(true);
          } else {
            reject(new Error('Invalid configuration file format'));
          }
        } catch (error) {
          reject(error);
        }
      };
      
      reader.onerror = () => reject(new Error('Failed to read file'));
      reader.readAsText(file);
    });
  }

  // Initialize persistence on store creation
  loadFromLocalStorage();

  return {
    lastSaved,
    autoSaveEnabled,
    autoSaveInterval,
    saveToLocalStorage,
    loadFromLocalStorage,
    clearLocalStorage,
    exportConfiguration,
    importConfiguration,
  };
});

// Utility function for debouncing
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: number;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}
