import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { CanvasNode, LegalStructure, CanvasEdge } from '@/types';

export const useCanvasStore = defineStore('canvas', () => {
  const nodes = ref<CanvasNode[]>([]);
  const edges = ref<CanvasEdge[]>([]);
  const selectedNodeId = ref<string | null>(null);
  const history = ref<{ nodes: CanvasNode[]; edges: CanvasEdge[] }[]>([]);
  const historyIndex = ref(-1);

  // Computed properties
  const canUndo = computed(() => historyIndex.value > 0);
  const canRedo = computed(() => historyIndex.value < history.value.length - 1);
  const selectedNode = computed(() => nodes.value.find(n => n.id === selectedNodeId.value));

  // History management
  function saveState() {
    const state = {
      nodes: JSON.parse(JSON.stringify(nodes.value)),
      edges: JSON.parse(JSON.stringify(edges.value))
    };
    
    // Remove any states after current index
    history.value = history.value.slice(0, historyIndex.value + 1);
    history.value.push(state);
    historyIndex.value++;
    
    // Limit history size
    if (history.value.length > 50) {
      history.value.shift();
      historyIndex.value--;
    }
  }

  function undo() {
    if (canUndo.value) {
      historyIndex.value--;
      const state = history.value[historyIndex.value];
      nodes.value = JSON.parse(JSON.stringify(state.nodes));
      edges.value = JSON.parse(JSON.stringify(state.edges));
    }
  }

  function redo() {
    if (canRedo.value) {
      historyIndex.value++;
      const state = history.value[historyIndex.value];
      nodes.value = JSON.parse(JSON.stringify(state.nodes));
      edges.value = JSON.parse(JSON.stringify(state.edges));
    }
  }

  // Function to add a new structure to the canvas as a node
  function addNode(structure: LegalStructure, position: { x: number; y: number }) {
    const newNode: CanvasNode = {
      id: `node_${Date.now()}`,
      type: 'structure',
      position,
      data: {
        structure,
      },
    };
    nodes.value.push(newNode);
    saveState();
  }

  // Function to update a node's position
  function updateNodePosition(nodeId: string, newPosition: { x: number; y: number }) {
    const node = nodes.value.find((n) => n.id === nodeId);
    if (node) {
      node.position = newPosition;
    }
  }

  // Function to remove a node from the canvas
  function removeNode(nodeId: string) {
    nodes.value = nodes.value.filter((n) => n.id !== nodeId);
    edges.value = edges.value.filter((e) => e.source !== nodeId && e.target !== nodeId);
    if (selectedNodeId.value === nodeId) {
      selectedNodeId.value = null;
    }
    saveState();
  }

  // Function to clear the entire canvas
  function clearCanvas() {
    nodes.value = [];
    edges.value = [];
    selectedNodeId.value = null;
    saveState();
  }

  // Function to select a node
  function selectNode(nodeId: string | null) {
    selectedNodeId.value = nodeId;
  }

  // Function to add an edge between two nodes
  function addEdge(sourceId: string, targetId: string, type: 'ownership' | 'control' | 'beneficiary' = 'ownership') {
    const edgeId = `edge_${Date.now()}`;
    const newEdge: CanvasEdge = {
      id: edgeId,
      source: sourceId,
      target: targetId,
      type,
    };
    edges.value.push(newEdge);
    saveState();
  }

  // Function to remove an edge
  function removeEdge(edgeId: string) {
    edges.value = edges.value.filter((e) => e.id !== edgeId);
    saveState();
  }

  // Initialize history with empty state
  saveState();

  return {
    nodes,
    edges,
    selectedNodeId,
    selectedNode,
    canUndo,
    canRedo,
    addNode,
    updateNodePosition,
    removeNode,
    clearCanvas,
    selectNode,
    addEdge,
    removeEdge,
    undo,
    redo,
  };
});
