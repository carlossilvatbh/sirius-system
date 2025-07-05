// SIRIUS Advanced Canvas Features
// Enhanced drag-and-drop, connections, zoom/pan, snap-to-grid, undo/redo

class SiriusCanvasAdvanced {
    constructor(app) {
        this.app = app;
        this.canvas = null;
        this.ctx = null;
        this.scale = 1;
        this.panX = 0;
        this.panY = 0;
        this.isPanning = false;
        this.lastPanPoint = { x: 0, y: 0 };
        
        // Grid settings
        this.gridSize = 20;
        this.snapToGrid = true;
        
        // Connection system
        this.connections = [];
        this.isConnecting = false;
        this.connectionStart = null;
        this.tempConnection = null;
        
        // Undo/Redo system
        this.history = [];
        this.historyIndex = -1;
        this.maxHistorySize = 50;
        
        // Selection system
        this.selectedElements = new Set();
        this.selectionBox = null;
        this.isSelecting = false;
        
        this.initializeCanvas();
        this.setupEventListeners();
    }
    
    initializeCanvas() {
        // Create overlay canvas for connections and grid
        const canvasContainer = this.app.$refs.canvasContainer;
        if (!canvasContainer) return;
        
        this.canvas = document.createElement('canvas');
        this.canvas.style.position = 'absolute';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.pointerEvents = 'none';
        this.canvas.style.zIndex = '10';
        
        this.ctx = this.canvas.getContext('2d');
        canvasContainer.appendChild(this.canvas);
        
        this.resizeCanvas();
        this.saveState();
    }
    
    setupEventListeners() {
        const container = this.app.$refs.canvasContainer;
        if (!container) return;
        
        // Mouse events
        container.addEventListener('wheel', this.handleWheel.bind(this));
        container.addEventListener('mousedown', this.handleMouseDown.bind(this));
        container.addEventListener('mousemove', this.handleMouseMove.bind(this));
        container.addEventListener('mouseup', this.handleMouseUp.bind(this));
        
        // Keyboard events
        document.addEventListener('keydown', this.handleKeyDown.bind(this));
        
        // Window resize
        window.addEventListener('resize', this.resizeCanvas.bind(this));
    }
    
    resizeCanvas() {
        if (!this.canvas || !this.app.$refs.canvasContainer) return;
        
        const container = this.app.$refs.canvasContainer;
        const rect = container.getBoundingClientRect();
        
        this.canvas.width = rect.width;
        this.canvas.height = rect.height;
        
        this.redraw();
    }
    
    // Grid System
    drawGrid() {
        if (!this.ctx) return;
        
        const ctx = this.ctx;
        const width = this.canvas.width;
        const height = this.canvas.height;
        
        ctx.save();
        ctx.strokeStyle = '#e5e7eb';
        ctx.lineWidth = 0.5;
        
        const gridSize = this.gridSize * this.scale;
        const offsetX = (this.panX % gridSize);
        const offsetY = (this.panY % gridSize);
        
        // Vertical lines
        for (let x = offsetX; x < width; x += gridSize) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, height);
            ctx.stroke();
        }
        
        // Horizontal lines
        for (let y = offsetY; y < height; y += gridSize) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }
        
        ctx.restore();
    }
    
    snapToGridPosition(x, y) {
        if (!this.snapToGrid) return { x, y };
        
        const gridSize = this.gridSize;
        return {
            x: Math.round(x / gridSize) * gridSize,
            y: Math.round(y / gridSize) * gridSize
        };
    }
    
    // Connection System
    createConnection(fromElement, toElement, type = 'default') {
        const connection = {
            id: `connection_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            from: fromElement.id,
            to: toElement.id,
            type: type,
            style: {
                color: '#3b82f6',
                width: 2,
                dashArray: type === 'dependency' ? [5, 5] : []
            }
        };
        
        this.connections.push(connection);
        this.app.conexoes = this.connections;
        this.redraw();
        this.saveState();
        
        return connection;
    }
    
    removeConnection(connectionId) {
        const index = this.connections.findIndex(c => c.id === connectionId);
        if (index !== -1) {
            this.connections.splice(index, 1);
            this.app.conexoes = this.connections;
            this.redraw();
            this.saveState();
        }
    }
    
    drawConnections() {
        if (!this.ctx) return;
        
        const ctx = this.ctx;
        
        this.connections.forEach(connection => {
            const fromElement = this.app.elementos.find(el => el.id === connection.from);
            const toElement = this.app.elementos.find(el => el.id === connection.to);
            
            if (!fromElement || !toElement) return;
            
            const fromPos = this.getElementCenter(fromElement);
            const toPos = this.getElementCenter(toElement);
            
            this.drawConnection(fromPos, toPos, connection.style);
        });
        
        // Draw temporary connection while connecting
        if (this.tempConnection) {
            this.drawConnection(
                this.tempConnection.start,
                this.tempConnection.end,
                { color: '#6b7280', width: 2, dashArray: [3, 3] }
            );
        }
    }
    
    drawConnection(from, to, style) {
        const ctx = this.ctx;
        
        ctx.save();
        ctx.strokeStyle = style.color;
        ctx.lineWidth = style.width;
        
        if (style.dashArray && style.dashArray.length > 0) {
            ctx.setLineDash(style.dashArray);
        }
        
        // Calculate control points for curved connection
        const dx = to.x - from.x;
        const dy = to.y - from.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        const controlOffset = Math.min(distance * 0.3, 100);
        const cp1x = from.x + controlOffset;
        const cp1y = from.y;
        const cp2x = to.x - controlOffset;
        const cp2y = to.y;
        
        // Draw curved line
        ctx.beginPath();
        ctx.moveTo(from.x, from.y);
        ctx.bezierCurveTo(cp1x, cp1y, cp2x, cp2y, to.x, to.y);
        ctx.stroke();
        
        // Draw arrow head
        this.drawArrowHead(ctx, cp2x, cp2y, to.x, to.y, style.color);
        
        ctx.restore();
    }
    
    drawArrowHead(ctx, fromX, fromY, toX, toY, color) {
        const headLength = 10;
        const angle = Math.atan2(toY - fromY, toX - fromX);
        
        ctx.save();
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.moveTo(toX, toY);
        ctx.lineTo(
            toX - headLength * Math.cos(angle - Math.PI / 6),
            toY - headLength * Math.sin(angle - Math.PI / 6)
        );
        ctx.lineTo(
            toX - headLength * Math.cos(angle + Math.PI / 6),
            toY - headLength * Math.sin(angle + Math.PI / 6)
        );
        ctx.closePath();
        ctx.fill();
        ctx.restore();
    }
    
    getElementCenter(element) {
        return {
            x: element.position.x + 100, // Half of element width (200px)
            y: element.position.y + 50   // Half of element height (100px)
        };
    }
    
    // Zoom and Pan
    handleWheel(event) {
        event.preventDefault();
        
        const rect = this.canvas.getBoundingClientRect();
        const mouseX = event.clientX - rect.left;
        const mouseY = event.clientY - rect.top;
        
        const zoomFactor = event.deltaY > 0 ? 0.9 : 1.1;
        const newScale = Math.max(0.1, Math.min(3, this.scale * zoomFactor));
        
        if (newScale !== this.scale) {
            // Zoom towards mouse position
            const scaleChange = newScale / this.scale;
            this.panX = mouseX - (mouseX - this.panX) * scaleChange;
            this.panY = mouseY - (mouseY - this.panY) * scaleChange;
            this.scale = newScale;
            
            this.updateElementTransforms();
            this.redraw();
        }
    }
    
    startPan(x, y) {
        this.isPanning = true;
        this.lastPanPoint = { x, y };
    }
    
    updatePan(x, y) {
        if (!this.isPanning) return;
        
        const dx = x - this.lastPanPoint.x;
        const dy = y - this.lastPanPoint.y;
        
        this.panX += dx;
        this.panY += dy;
        
        this.lastPanPoint = { x, y };
        
        this.updateElementTransforms();
        this.redraw();
    }
    
    stopPan() {
        this.isPanning = false;
    }
    
    updateElementTransforms() {
        // Update element positions based on pan and zoom
        const container = this.app.$refs.canvasContainer;
        if (!container) return;
        
        container.style.transform = `translate(${this.panX}px, ${this.panY}px) scale(${this.scale})`;
        container.style.transformOrigin = '0 0';
    }
    
    // Selection System
    startSelection(x, y) {
        this.isSelecting = true;
        this.selectionBox = {
            startX: x,
            startY: y,
            endX: x,
            endY: y
        };
    }
    
    updateSelection(x, y) {
        if (!this.isSelecting || !this.selectionBox) return;
        
        this.selectionBox.endX = x;
        this.selectionBox.endY = y;
        
        this.redraw();
    }
    
    finishSelection() {
        if (!this.isSelecting || !this.selectionBox) return;
        
        const box = this.selectionBox;
        const minX = Math.min(box.startX, box.endX);
        const maxX = Math.max(box.startX, box.endX);
        const minY = Math.min(box.startY, box.endY);
        const maxY = Math.max(box.startY, box.endY);
        
        // Select elements within selection box
        this.selectedElements.clear();
        this.app.elementos.forEach(element => {
            const elX = element.position.x;
            const elY = element.position.y;
            const elW = 200; // Element width
            const elH = 100; // Element height
            
            if (elX < maxX && elX + elW > minX && elY < maxY && elY + elH > minY) {
                this.selectedElements.add(element.id);
            }
        });
        
        this.isSelecting = false;
        this.selectionBox = null;
        this.redraw();
    }
    
    drawSelectionBox() {
        if (!this.isSelecting || !this.selectionBox) return;
        
        const ctx = this.ctx;
        const box = this.selectionBox;
        
        ctx.save();
        ctx.strokeStyle = '#3b82f6';
        ctx.fillStyle = 'rgba(59, 130, 246, 0.1)';
        ctx.lineWidth = 1;
        ctx.setLineDash([5, 5]);
        
        const x = Math.min(box.startX, box.endX);
        const y = Math.min(box.startY, box.endY);
        const width = Math.abs(box.endX - box.startX);
        const height = Math.abs(box.endY - box.startY);
        
        ctx.fillRect(x, y, width, height);
        ctx.strokeRect(x, y, width, height);
        
        ctx.restore();
    }
    
    // Undo/Redo System
    saveState() {
        const state = {
            elementos: JSON.parse(JSON.stringify(this.app.elementos)),
            conexoes: JSON.parse(JSON.stringify(this.connections)),
            timestamp: Date.now()
        };
        
        // Remove states after current index
        this.history = this.history.slice(0, this.historyIndex + 1);
        
        // Add new state
        this.history.push(state);
        this.historyIndex = this.history.length - 1;
        
        // Limit history size
        if (this.history.length > this.maxHistorySize) {
            this.history.shift();
            this.historyIndex--;
        }
    }
    
    undo() {
        if (this.historyIndex > 0) {
            this.historyIndex--;
            this.restoreState(this.history[this.historyIndex]);
        }
    }
    
    redo() {
        if (this.historyIndex < this.history.length - 1) {
            this.historyIndex++;
            this.restoreState(this.history[this.historyIndex]);
        }
    }
    
    restoreState(state) {
        this.app.elementos = JSON.parse(JSON.stringify(state.elementos));
        this.connections = JSON.parse(JSON.stringify(state.conexoes));
        this.app.conexoes = this.connections;
        
        this.app.calcularTotais();
        this.redraw();
    }
    
    // Event Handlers
    handleMouseDown(event) {
        const rect = this.canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        
        if (event.button === 1 || (event.button === 0 && event.ctrlKey)) {
            // Middle mouse or Ctrl+click for panning
            this.startPan(x, y);
        } else if (event.button === 0 && event.shiftKey) {
            // Shift+click for selection
            this.startSelection(x, y);
        }
    }
    
    handleMouseMove(event) {
        const rect = this.canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        
        if (this.isPanning) {
            this.updatePan(x, y);
        } else if (this.isSelecting) {
            this.updateSelection(x, y);
        } else if (this.tempConnection) {
            this.tempConnection.end = { x, y };
            this.redraw();
        }
    }
    
    handleMouseUp(event) {
        if (this.isPanning) {
            this.stopPan();
        } else if (this.isSelecting) {
            this.finishSelection();
        }
    }
    
    handleKeyDown(event) {
        if (event.ctrlKey || event.metaKey) {
            switch (event.key) {
                case 'z':
                    event.preventDefault();
                    if (event.shiftKey) {
                        this.redo();
                    } else {
                        this.undo();
                    }
                    break;
                case 'y':
                    event.preventDefault();
                    this.redo();
                    break;
                case 'a':
                    event.preventDefault();
                    this.selectAll();
                    break;
            }
        } else {
            switch (event.key) {
                case 'Delete':
                case 'Backspace':
                    this.deleteSelected();
                    break;
                case 'Escape':
                    this.clearSelection();
                    this.cancelConnection();
                    break;
                case 'g':
                    this.toggleGrid();
                    break;
            }
        }
    }
    
    // Utility Methods
    selectAll() {
        this.selectedElements.clear();
        this.app.elementos.forEach(element => {
            this.selectedElements.add(element.id);
        });
        this.redraw();
    }
    
    clearSelection() {
        this.selectedElements.clear();
        this.redraw();
    }
    
    deleteSelected() {
        if (this.selectedElements.size === 0) return;
        
        // Remove selected elements
        this.app.elementos = this.app.elementos.filter(element => 
            !this.selectedElements.has(element.id)
        );
        
        // Remove connections to deleted elements
        this.connections = this.connections.filter(connection => 
            !this.selectedElements.has(connection.from) && 
            !this.selectedElements.has(connection.to)
        );
        
        this.app.conexoes = this.connections;
        this.selectedElements.clear();
        
        this.app.calcularTotais();
        this.redraw();
        this.saveState();
    }
    
    toggleGrid() {
        this.snapToGrid = !this.snapToGrid;
        this.redraw();
        
        this.app.showNotification(
            `Grid snap ${this.snapToGrid ? 'enabled' : 'disabled'}`,
            'info'
        );
    }
    
    cancelConnection() {
        this.isConnecting = false;
        this.connectionStart = null;
        this.tempConnection = null;
        this.redraw();
    }
    
    // Main redraw method
    redraw() {
        if (!this.ctx) return;
        
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw grid
        this.drawGrid();
        
        // Draw connections
        this.drawConnections();
        
        // Draw selection box
        this.drawSelectionBox();
        
        // Highlight selected elements
        this.highlightSelectedElements();
    }
    
    highlightSelectedElements() {
        if (this.selectedElements.size === 0) return;
        
        const ctx = this.ctx;
        
        ctx.save();
        ctx.strokeStyle = '#3b82f6';
        ctx.lineWidth = 2;
        ctx.setLineDash([]);
        
        this.app.elementos.forEach(element => {
            if (this.selectedElements.has(element.id)) {
                const x = element.position.x - 2;
                const y = element.position.y - 2;
                const width = 204; // Element width + border
                const height = 104; // Element height + border
                
                ctx.strokeRect(x, y, width, height);
            }
        });
        
        ctx.restore();
    }
    
    // Public API methods
    resetView() {
        this.scale = 1;
        this.panX = 0;
        this.panY = 0;
        this.updateElementTransforms();
        this.redraw();
    }
    
    fitToContent() {
        if (this.app.elementos.length === 0) return;
        
        // Calculate bounding box of all elements
        let minX = Infinity, minY = Infinity;
        let maxX = -Infinity, maxY = -Infinity;
        
        this.app.elementos.forEach(element => {
            minX = Math.min(minX, element.position.x);
            minY = Math.min(minY, element.position.y);
            maxX = Math.max(maxX, element.position.x + 200);
            maxY = Math.max(maxY, element.position.y + 100);
        });
        
        const contentWidth = maxX - minX;
        const contentHeight = maxY - minY;
        const padding = 50;
        
        const scaleX = (this.canvas.width - padding * 2) / contentWidth;
        const scaleY = (this.canvas.height - padding * 2) / contentHeight;
        
        this.scale = Math.min(scaleX, scaleY, 1);
        this.panX = (this.canvas.width - contentWidth * this.scale) / 2 - minX * this.scale;
        this.panY = (this.canvas.height - contentHeight * this.scale) / 2 - minY * this.scale;
        
        this.updateElementTransforms();
        this.redraw();
    }
    
    exportCanvas() {
        // Create a temporary canvas with the current view
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = this.canvas.width;
        tempCanvas.height = this.canvas.height;
        
        const tempCtx = tempCanvas.getContext('2d');
        
        // Copy current canvas content
        tempCtx.drawImage(this.canvas, 0, 0);
        
        return tempCanvas.toDataURL('image/png');
    }
    
    // Cleanup
    destroy() {
        if (this.canvas && this.canvas.parentNode) {
            this.canvas.parentNode.removeChild(this.canvas);
        }
        
        document.removeEventListener('keydown', this.handleKeyDown.bind(this));
        window.removeEventListener('resize', this.resizeCanvas.bind(this));
    }
}

// Export for use in main app
window.SiriusCanvasAdvanced = SiriusCanvasAdvanced;

