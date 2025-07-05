import type { Node, Edge } from '@vue-flow/core';
import type { LegalStructure } from './index';

// Extended Vue Flow types for Sirius
export interface SiriusNode extends Node {
  type: 'structure';
  data: {
    structure: LegalStructure;
    selected?: boolean;
    highlighted?: boolean;
    validationStatus?: 'valid' | 'warning' | 'error';
  };
}

export interface SiriusEdge {
  id: string;
  source: string;
  target: string;
  type: ConnectionType;
  data?: {
    label?: string;
    connectionType: ConnectionType;
    validationStatus?: 'valid' | 'warning' | 'error';
  };
}

export type ConnectionType = 'ownership' | 'control' | 'beneficiary';

export interface CanvasState {
  nodes: SiriusNode[];
  edges: SiriusEdge[];
  selectedNodes: string[];
  selectedEdges: string[];
  viewport: {
    x: number;
    y: number;
    zoom: number;
  };
}

export interface CanvasActions {
  addNode: (structure: LegalStructure, position: { x: number; y: number }) => void;
  removeNode: (nodeId: string) => void;
  updateNode: (nodeId: string, updates: Partial<SiriusNode['data']>) => void;
  addEdge: (source: string, target: string, type: ConnectionType) => void;
  removeEdge: (edgeId: string) => void;
  selectNode: (nodeId: string) => void;
  selectMultipleNodes: (nodeIds: string[]) => void;
  clearSelection: () => void;
  fitView: () => void;
  zoomToSelection: () => void;
  autoLayout: (algorithm: 'hierarchical' | 'force' | 'circular') => void;
}

export interface CanvasConfig {
  snapToGrid: boolean;
  gridSize: number;
  showMinimap: boolean;
  showControls: boolean;
  showBackground: boolean;
  maxZoom: number;
  minZoom: number;
  defaultZoom: number;
}

export interface DragEvent {
  structure: LegalStructure;
  position: { x: number; y: number };
}

export interface CanvasHistory {
  states: CanvasState[];
  currentIndex: number;
  maxStates: number;
}

export interface LayoutAlgorithm {
  name: string;
  description: string;
  options?: Record<string, any>;
}

export const LAYOUT_ALGORITHMS: LayoutAlgorithm[] = [
  {
    name: 'hierarchical',
    description: 'Hierarchical layout for organizational structures',
    options: {
      direction: 'TB', // Top to Bottom
      spacing: { x: 200, y: 150 }
    }
  },
  {
    name: 'force',
    description: 'Force-directed layout for natural clustering',
    options: {
      strength: 0.5,
      distance: 200
    }
  },
  {
    name: 'circular',
    description: 'Circular layout for equal relationships',
    options: {
      radius: 300
    }
  }
];

export const CONNECTION_TYPES: Record<ConnectionType, { label: string; color: string; style: string }> = {
  ownership: {
    label: 'Ownership',
    color: '#059669',
    style: 'solid'
  },
  control: {
    label: 'Control',
    color: '#dc2626',
    style: 'dashed'
  },
  beneficiary: {
    label: 'Beneficiary',
    color: '#2563eb',
    style: 'dotted'
  }
};

