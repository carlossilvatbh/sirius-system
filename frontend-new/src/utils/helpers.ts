import type { LegalStructure, StructureType } from '@/types';

// ID Generation
export function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

export function generateNodeId(prefix: string = 'node'): string {
  return `${prefix}-${generateId()}`;
}

export function generateEdgeId(source: string, target: string): string {
  return `edge-${source}-${target}-${Date.now()}`;
}

// Currency Formatting
export function formatCurrency(amount: number, currency: string = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

export function formatCurrencyDetailed(amount: number, currency: string = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
}

// Number Formatting
export function formatNumber(number: number): string {
  return new Intl.NumberFormat('en-US').format(number);
}

export function formatPercentage(value: number, decimals: number = 1): string {
  return `${(value * 100).toFixed(decimals)}%`;
}

// Date Formatting
export function formatDate(date: string | Date): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(d);
}

export function formatDateTime(date: string | Date): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(d);
}

export function formatRelativeTime(date: string | Date): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  const now = new Date();
  const diffMs = now.getTime() - d.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  
  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
  if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
  return `${Math.floor(diffDays / 365)} years ago`;
}

// String Utilities
export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

export function camelToTitle(str: string): string {
  return str
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, (s) => s.toUpperCase())
    .trim();
}

export function slugify(str: string): string {
  return str
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_-]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

// Structure Type Utilities
export function getStructureTypeDisplay(type: StructureType): string {
  const displayNames: Record<StructureType, string> = {
    BDAO_SAC: 'Bahamas DAO SAC',
    WYOMING_DAO_LLC: 'Wyoming DAO LLC',
    BTS_VAULT: 'BTS Vault',
    WYOMING_FOUNDATION: 'Wyoming Foundation',
    WYOMING_CORP: 'Wyoming Corporation',
    NATIONALIZATION: 'Nationalization',
    FUND_TOKEN: 'Fund Token as a Service',
  };
  
  return displayNames[type] || type;
}

export function getStructureTypeColor(type: StructureType): string {
  const colors: Record<StructureType, string> = {
    BDAO_SAC: '#8b5cf6',
    WYOMING_DAO_LLC: '#8b5cf6',
    BTS_VAULT: '#ea580c',
    WYOMING_FOUNDATION: '#dc2626',
    WYOMING_CORP: '#059669',
    NATIONALIZATION: '#059669',
    FUND_TOKEN: '#ea580c',
  };
  
  return colors[type] || '#6b7280';
}

export function getComplexityDisplay(level: number): string {
  const displays = {
    1: 'Very Simple',
    2: 'Simple',
    3: 'Moderate',
    4: 'Complex',
    5: 'Very Complex',
  };
  
  return displays[level as keyof typeof displays] || 'Unknown';
}

export function getComplexityColor(level: number): string {
  const colors = {
    1: '#10b981',
    2: '#84cc16',
    3: '#f59e0b',
    4: '#f97316',
    5: '#ef4444',
  };
  
  return colors[level as keyof typeof colors] || '#6b7280';
}

// Validation Utilities
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

export function isValidUrl(url: string): boolean {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

// Array Utilities
export function unique<T>(array: T[]): T[] {
  return [...new Set(array)];
}

export function groupBy<T, K extends keyof T>(array: T[], key: K): Record<string, T[]> {
  return array.reduce((groups, item) => {
    const group = String(item[key]);
    groups[group] = groups[group] || [];
    groups[group].push(item);
    return groups;
  }, {} as Record<string, T[]>);
}

export function sortBy<T>(array: T[], key: keyof T, direction: 'asc' | 'desc' = 'asc'): T[] {
  return [...array].sort((a, b) => {
    const aVal = a[key];
    const bVal = b[key];
    
    if (aVal < bVal) return direction === 'asc' ? -1 : 1;
    if (aVal > bVal) return direction === 'asc' ? 1 : -1;
    return 0;
  });
}

// Debouncing
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: number;
  
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait) as any;
  };
}

// Throttling
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean;
  
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

// Local Storage Utilities
export function getFromStorage<T>(key: string, defaultValue: T): T {
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : defaultValue;
  } catch {
    return defaultValue;
  }
}

export function setToStorage<T>(key: string, value: T): void {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (error) {
    console.warn('Failed to save to localStorage:', error);
  }
}

export function removeFromStorage(key: string): void {
  try {
    localStorage.removeItem(key);
  } catch (error) {
    console.warn('Failed to remove from localStorage:', error);
  }
}

// Canvas Utilities
export function calculateCanvasBounds(nodes: { position: { x: number; y: number } }[]): {
  minX: number;
  minY: number;
  maxX: number;
  maxY: number;
  width: number;
  height: number;
} {
  if (nodes.length === 0) {
    return { minX: 0, minY: 0, maxX: 0, maxY: 0, width: 0, height: 0 };
  }
  
  const positions = nodes.map(node => node.position);
  const minX = Math.min(...positions.map(p => p.x));
  const minY = Math.min(...positions.map(p => p.y));
  const maxX = Math.max(...positions.map(p => p.x));
  const maxY = Math.max(...positions.map(p => p.y));
  
  return {
    minX,
    minY,
    maxX,
    maxY,
    width: maxX - minX,
    height: maxY - minY,
  };
}

export function getOptimalZoom(
  canvasBounds: { width: number; height: number },
  viewportBounds: { width: number; height: number },
  padding: number = 50
): number {
  const scaleX = (viewportBounds.width - padding * 2) / canvasBounds.width;
  const scaleY = (viewportBounds.height - padding * 2) / canvasBounds.height;
  
  return Math.min(scaleX, scaleY, 1); // Don't zoom in beyond 100%
}

// Error Handling
export function handleError(error: unknown, context?: string): string {
  console.error(context ? `Error in ${context}:` : 'Error:', error);
  
  if (error instanceof Error) {
    return error.message;
  }
  
  if (typeof error === 'string') {
    return error;
  }
  
  return 'An unexpected error occurred';
}

// Type Guards
export function isLegalStructure(obj: any): obj is LegalStructure {
  return (
    obj &&
    typeof obj === 'object' &&
    typeof obj.id === 'number' &&
    typeof obj.nome === 'string' &&
    typeof obj.tipo === 'string' &&
    typeof obj.custo_base === 'number'
  );
}

// Download Utilities
export function downloadBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

export function downloadJson(data: any, filename: string): void {
  const json = JSON.stringify(data, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  downloadBlob(blob, filename);
}

// Color Utilities
export function hexToRgb(hex: string): { r: number; g: number; b: number } | null {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
      }
    : null;
}

export function rgbToHex(r: number, g: number, b: number): string {
  return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`;
}

export function adjustColorOpacity(color: string, opacity: number): string {
  const rgb = hexToRgb(color);
  if (!rgb) return color;
  
  return `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${opacity})`;
}

