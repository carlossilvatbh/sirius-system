// SIRIUS Canvas - Enhanced UX/UI JavaScript
// Version: 3.0 - Modern UX/UI Architecture

class SiriusCanvas {
    constructor() {
        this.structures = [];
        this.canvasElements = [];
        this.connections = [];
        this.selectedElement = null;
        this.selectedStructure = null;
        this.totalCost = 0;
        this.draggedStructure = null;
        this.isDragging = false;
        this.currentFilter = '';
        this.searchQuery = '';
        this.zoomLevel = 1;
        this.connectionMode = false;
        this.connectionSource = null;
        this.history = [];
        this.historyIndex = -1;
        this.pricingScenario = 'basico';
        
        // UI State
        this.isMobile = window.innerWidth < 768;
        this.sidebarCollapsed = false;
        this.notifications = [];
        this.notificationId = 0;
        
        this.init();
    }

    async init() {
        try {
            this.showLoading();
            await this.loadStructures();
            this.setupEventListeners();
            this.setupResponsiveHandlers();
            this.setupFilterHandlers();
            this.renderStructures();
            this.updateStats();
            this.showSuccessMessage('SIRIUS Canvas initialized successfully');
        } catch (error) {
            console.error('Failed to initialize canvas:', error);
            this.showErrorMessage('Failed to initialize canvas. Please refresh the page.');
        } finally {
            this.hideLoading();
        }
    }

    async loadStructures() {
        try {
            const response = await fetch(window.djangoData.apiUrls.estruturas);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            this.structures = await response.json();
            console.log(`Loaded ${this.structures.length} structures`);
        } catch (error) {
            console.error('Error loading structures:', error);
            this.structures = [];
            throw error;
        }
    }

    setupEventListeners() {
        // Search functionality
        const searchInput = document.getElementById('search-structures');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.searchQuery = e.target.value;
                this.filterStructures();
                this.updateSearchClearButton();
            });
        }

        // Toolbar buttons
        this.setupToolbarButtons();
        
        // Canvas events
        this.setupCanvasEvents();
        
        // Keyboard shortcuts
        this.setupKeyboardShortcuts();
    }

    setupToolbarButtons() {
        const buttons = {
            'save-btn': () => this.saveConfiguration(),
            'pdf-btn': () => this.generatePDF(),
            'clear-canvas': () => this.clearCanvas(),
            'undo-btn': () => this.undoAction(),
            'redo-btn': () => this.redoAction(),
            'zoom-in': () => this.zoomIn(),
            'zoom-out': () => this.zoomOut(),
            'zoom-reset': () => this.resetZoom(),
            'connection-mode-btn': () => this.toggleConnectionMode()
        };

        Object.entries(buttons).forEach(([id, handler]) => {
            const btn = document.getElementById(id);
            if (btn) {
                btn.addEventListener('click', handler);
            }
        });

        // Pricing scenario selector
        const scenarioSelect = document.getElementById('pricing-scenario');
        if (scenarioSelect) {
            scenarioSelect.addEventListener('change', (e) => {
                this.pricingScenario = e.target.value;
                this.recalculateCosts();
            });
        }
    }

    setupCanvasEvents() {
        const canvasContainer = document.getElementById('canvas-container');
        if (canvasContainer) {
            canvasContainer.addEventListener('click', (e) => {
                if (e.target === canvasContainer || e.target.classList.contains('canvas-content')) {
                    this.deselectAll();
                }
            });
        }
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case 'z':
                        e.preventDefault();
                        this.undoAction();
                        break;
                    case 'y':
                        e.preventDefault();
                        this.redoAction();
                        break;
                    case 's':
                        e.preventDefault();
                        this.saveConfiguration();
                        break;
                    case 'f':
                        e.preventDefault();
                        document.getElementById('search-structures')?.focus();
                        break;
                }
            }
            
            if (e.key === 'Escape') {
                this.deselectAll();
                this.exitConnectionMode();
            }
            
            if (e.key === 'Delete' && this.selectedElement) {
                this.removeElement(this.selectedElement.id);
            }
        });
    }

    setupResponsiveHandlers() {
        window.addEventListener('resize', () => {
            this.isMobile = window.innerWidth < 768;
            this.handleResize();
        });
    }

    setupFilterHandlers() {
        const filterButtons = document.querySelectorAll('.filter-tag');
        filterButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                // Remove active class from all buttons
                filterButtons.forEach(btn => btn.classList.remove('active'));
                
                // Add active class to clicked button
                e.target.classList.add('active');
                
                // Update filter
                this.currentFilter = e.target.dataset.filter;
                this.filterStructures();
            });
        });
    }

    handleResize() {
        if (!this.isMobile) {
            this.closeMobileSidebar();
        }
    }

    // Enhanced filtering and search
    filterStructures() {
        const searchQuery = this.searchQuery.toLowerCase();
        const filteredStructures = this.structures.filter(structure => {
            const matchesSearch = searchQuery === '' || 
                structure.nome.toLowerCase().includes(searchQuery) ||
                structure.descricao.toLowerCase().includes(searchQuery) ||
                structure.tipo.toLowerCase().includes(searchQuery);
                
            const matchesFilter = this.currentFilter === '' || 
                structure.tipo === this.currentFilter;
                
            return matchesSearch && matchesFilter;
        });
        
        this.renderFilteredStructures(filteredStructures);
    }

    updateSearchClearButton() {
        const clearBtn = document.getElementById('search-clear');
        if (clearBtn) {
            clearBtn.style.display = this.searchQuery.length > 0 ? 'block' : 'none';
        }
    }

    renderStructures() {
        this.filterStructures();
    }

    renderFilteredStructures(structures) {
        const structuresList = document.getElementById('structures-list');
        const emptyState = document.getElementById('structures-empty');
        
        if (!structuresList || !emptyState) return;

        if (structures.length === 0) {
            structuresList.innerHTML = '';
            emptyState.style.display = 'block';
            return;
        }

        emptyState.style.display = 'none';
        structuresList.innerHTML = '';

        structures.forEach(structure => {
            const card = this.createStructureCard(structure);
            structuresList.appendChild(card);
        });
    }

    createStructureCard(structure) {
        const card = document.createElement('div');
        card.className = 'structure-card animate-fadeIn';
        card.draggable = true;
        card.dataset.structureId = structure.id;

        card.innerHTML = `
            <div class="structure-header">
                <div class="structure-type">${structure.tipo}</div>
                <div class="complexity-indicator complexity-${structure.complexidade}"></div>
            </div>
            <h3 class="structure-name">${structure.nome}</h3>
            <div class="structure-cost">${this.formatCurrency(structure.custo_base)}</div>
            <div class="structure-meta">
                <span><i class="fas fa-clock"></i>${structure.tempo_implementacao}d</span>
                <span><i class="fas fa-shield-alt"></i>${structure.nivel_confidencialidade}/5</span>
            </div>
        `;

        // Enhanced drag and drop
        card.addEventListener('dragstart', (e) => {
            this.startDragStructure(structure, e);
        });

        card.addEventListener('dragend', (e) => {
            this.endDragStructure(e);
        });

        // Click to select
        card.addEventListener('click', () => {
            this.selectStructure(structure);
        });

        return card;
    }

    // Enhanced drag and drop functionality
    startDragStructure(structure, e) {
        this.draggedStructure = structure;
        const card = e.target.closest('.structure-card');
        if (card) {
            card.classList.add('dragging');
        }
        
        e.dataTransfer.setData('text/plain', JSON.stringify(structure));
        e.dataTransfer.effectAllowed = 'move';
        
        // Add drag image
        const dragImage = card.cloneNode(true);
        dragImage.style.opacity = '0.8';
        dragImage.style.transform = 'rotate(5deg)';
        dragImage.style.position = 'absolute';
        dragImage.style.top = '-1000px';
        document.body.appendChild(dragImage);
        e.dataTransfer.setDragImage(dragImage, 0, 0);
        
        setTimeout(() => {
            document.body.removeChild(dragImage);
        }, 0);
    }

    endDragStructure(e) {
        const card = e.target.closest('.structure-card');
        if (card) {
            card.classList.remove('dragging');
        }
        this.draggedStructure = null;
        
        // Remove drag-over state from canvas
        const canvasContainer = document.getElementById('canvas-container');
        if (canvasContainer) {
            canvasContainer.classList.remove('drag-over');
        }
    }

    selectStructure(structure) {
        this.selectedStructure = structure;
        
        // Update UI selection
        document.querySelectorAll('.structure-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        const selectedCard = document.querySelector(`[data-structure-id="${structure.id}"]`);
        if (selectedCard) {
            selectedCard.classList.add('selected');
        }
        
        // Show mobile details if needed
        if (this.isMobile) {
            this.showMobileDetails(structure);
        }
    }

        this.structures.forEach(structure => {
            const card = this.createStructureCard(structure);
            structuresList.appendChild(card);
        });
    }

    createStructureCard(structure) {
        const card = document.createElement('div');
        card.className = 'structure-card fade-in';
        card.draggable = true;
        card.dataset.structureId = structure.id;

        card.innerHTML = `
            <h3>${structure.nome}</h3>
            <p>${structure.descricao.substring(0, 100)}${structure.descricao.length > 100 ? '...' : ''}</p>
            <div class="structure-meta">
                <span class="structure-cost">${this.formatCurrency(structure.custo_base)}</span>
                <span>${structure.tempo_implementacao} days</span>
            </div>
        `;

        // Drag events
        card.addEventListener('dragstart', (e) => this.handleDragStart(e, structure));
        card.addEventListener('dragend', (e) => this.handleDragEnd(e));

        return card;
    }

    filterStructures(query) {
        const cards = document.querySelectorAll('.structure-card');
        const lowercaseQuery = query.toLowerCase();

        cards.forEach(card => {
            const structureId = parseInt(card.dataset.structureId);
            const structure = this.structures.find(s => s.id === structureId);
            
            if (!structure) return;

            const matches = 
                structure.nome.toLowerCase().includes(lowercaseQuery) ||
                structure.descricao.toLowerCase().includes(lowercaseQuery) ||
                structure.tipo.toLowerCase().includes(lowercaseQuery);

            card.style.display = matches ? 'block' : 'none';
        });
    }

    handleDragStart(e, structure) {
        this.draggedStructure = structure;
        e.dataTransfer.setData('text/plain', JSON.stringify(structure));
        e.dataTransfer.effectAllowed = 'copy';
        
        e.target.classList.add('dragging');
    }

    handleDragEnd(e) {
        e.target.classList.remove('dragging');
        this.draggedStructure = null;
    }

    addToCanvas(structure, x, y) {
        const element = {
            id: `element_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            structure: structure,
            x: Math.max(0, x - 100),
            y: Math.max(0, y - 50),
            width: 200,
            height: 120
        };

        this.canvasElements.push(element);
        this.renderCanvasElement(element);
        this.updateTotalCost();
        this.showSuccessMessage(`Added ${structure.nome} to canvas`);
    }

    renderCanvasElement(element) {
        const canvasElements = document.getElementById('canvas-elements');
        if (!canvasElements) return;

        const elementDiv = document.createElement('div');
        elementDiv.className = 'canvas-element fade-in';
        elementDiv.dataset.elementId = element.id;
        elementDiv.style.left = element.x + 'px';
        elementDiv.style.top = element.y + 'px';
        elementDiv.style.width = element.width + 'px';
        elementDiv.style.minHeight = element.height + 'px';

        elementDiv.innerHTML = `
            <div class="element-actions">
                <button onclick="canvas.removeElement('${element.id}')" title="Remove">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <h4>${element.structure.nome}</h4>
            <p>${element.structure.descricao.substring(0, 80)}${element.structure.descricao.length > 80 ? '...' : ''}</p>
            <div class="structure-meta">
                <span class="structure-cost">${this.formatCurrency(element.structure.custo_base)}</span>
                <span>${element.structure.tempo_implementacao} days</span>
            </div>
        `;

        // Make element draggable within canvas
        this.makeElementDraggable(elementDiv, element);

        // Click to select
        elementDiv.addEventListener('click', (e) => {
            e.stopPropagation();
            this.selectElement(element.id);
        });

        canvasElements.appendChild(elementDiv);
    }

    makeElementDraggable(elementDiv, element) {
        let isDragging = false;
        let startX, startY, initialX, initialY;

        elementDiv.addEventListener('mousedown', (e) => {
            if (e.target.tagName === 'BUTTON' || e.target.tagName === 'I') return;
            
            isDragging = true;
            startX = e.clientX;
            startY = e.clientY;
            initialX = element.x;
            initialY = element.y;
            
            elementDiv.style.cursor = 'grabbing';
            e.preventDefault();
        });

        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            
            const deltaX = e.clientX - startX;
            const deltaY = e.clientY - startY;
            
            element.x = Math.max(0, initialX + deltaX);
            element.y = Math.max(0, initialY + deltaY);
            
            elementDiv.style.left = element.x + 'px';
            elementDiv.style.top = element.y + 'px';
        });

        document.addEventListener('mouseup', () => {
            if (isDragging) {
                isDragging = false;
                elementDiv.style.cursor = 'move';
            }
        });
    }

    selectElement(elementId) {
        // Remove previous selection
        this.deselectAll();

        const elementDiv = document.querySelector(`[data-element-id="${elementId}"]`);
        if (elementDiv) {
            elementDiv.classList.add('selected');
            this.selectedElement = elementId;
        }
    }

    deselectAll() {
        document.querySelectorAll('.canvas-element.selected').forEach(el => {
            el.classList.remove('selected');
        });
        this.selectedElement = null;
    }

    removeElement(elementId) {
        const elementIndex = this.canvasElements.findIndex(el => el.id === elementId);
        if (elementIndex > -1) {
            const element = this.canvasElements[elementIndex];
            this.canvasElements.splice(elementIndex, 1);
            
            const elementDiv = document.querySelector(`[data-element-id="${elementId}"]`);
            if (elementDiv) {
                elementDiv.remove();
            }
            
            this.updateTotalCost();
            this.showSuccessMessage(`Removed ${element.structure.nome} from canvas`);
        }
    }

    clearCanvas() {
        if (this.canvasElements.length === 0) {
            this.showWarningMessage('Canvas is already empty');
            return;
        }

        if (confirm('Are you sure you want to clear the canvas? This action cannot be undone.')) {
            this.canvasElements = [];
            const canvasElements = document.getElementById('canvas-elements');
            if (canvasElements) {
                canvasElements.innerHTML = '';
            }
            this.updateTotalCost();
            this.showSuccessMessage('Canvas cleared');
        }
    }

    updateTotalCost() {
        this.totalCost = this.canvasElements.reduce((total, element) => {
            return total + parseFloat(element.structure.custo_base || 0);
        }, 0);

        const totalCostElement = document.getElementById('total-cost');
        if (totalCostElement) {
            totalCostElement.textContent = this.formatCurrency(this.totalCost);
        }
    }

    saveConfiguration() {
        if (this.canvasElements.length === 0) {
            this.showWarningMessage('No elements to save');
            return;
        }

        const config = {
            elements: this.canvasElements.map(el => ({
                structure_id: el.structure.id,
                x: el.x,
                y: el.y,
                width: el.width,
                height: el.height
            })),
            total_cost: this.totalCost,
            timestamp: new Date().toISOString()
        };

        // For now, just save to localStorage
        localStorage.setItem('sirius_canvas_config', JSON.stringify(config));
        this.showSuccessMessage('Configuration saved locally');
    }

    async generatePDF() {
        if (this.canvasElements.length === 0) {
            this.showWarningMessage('No elements to export');
            return;
        }

        this.showInfoMessage('PDF generation feature coming soon');
    }

    zoomIn() {
        const canvasContainer = document.getElementById('canvas-container');
        if (canvasContainer) {
            const currentZoom = parseFloat(canvasContainer.style.zoom || '1');
            const newZoom = Math.min(currentZoom * 1.2, 3);
            canvasContainer.style.zoom = newZoom.toString();
        }
    }

    zoomOut() {
        const canvasContainer = document.getElementById('canvas-container');
        if (canvasContainer) {
            const currentZoom = parseFloat(canvasContainer.style.zoom || '1');
            const newZoom = Math.max(currentZoom / 1.2, 0.3);
            canvasContainer.style.zoom = newZoom.toString();
        }
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    }

    showSuccessMessage(message) {
        this.showNotification(message, 'success');
    }

    showErrorMessage(message) {
        this.showNotification(message, 'error');
    }

    showWarningMessage(message) {
        this.showNotification(message, 'warning');
    }

    showInfoMessage(message) {
        this.showNotification(message, 'info');
    }

    showNotification(message, type = 'info') {
        // Simple notification system
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 16px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            max-width: 300px;
            word-wrap: break-word;
            animation: slideIn 0.3s ease-out;
        `;

        switch (type) {
            case 'success':
                notification.style.backgroundColor = '#059669';
                break;
            case 'error':
                notification.style.backgroundColor = '#dc2626';
                break;
            case 'warning':
                notification.style.backgroundColor = '#d97706';
                break;
            default:
                notification.style.backgroundColor = '#2563eb';
        }

        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Global drag and drop handlers
function allowDrop(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
    
    const canvasContainer = document.getElementById('canvas-container');
    if (canvasContainer) {
        canvasContainer.classList.add('drag-over');
    }
}

function handleDrop(e) {
    e.preventDefault();
    
    const canvasContainer = document.getElementById('canvas-container');
    if (canvasContainer) {
        canvasContainer.classList.remove('drag-over');
    }

    try {
        const structureData = JSON.parse(e.dataTransfer.getData('text/plain'));
        const rect = canvasContainer.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        if (window.canvas) {
            window.canvas.addToCanvas(structureData, x, y);
        }
    } catch (error) {
        console.error('Error handling drop:', error);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (window.djangoData && window.djangoData.apiUrls) {
        window.canvas = new SiriusCanvas();
    } else {
        console.error('Django data not available');
    }
});

// Handle page leave events
document.addEventListener('dragover', (e) => e.preventDefault());
document.addEventListener('drop', (e) => e.preventDefault());
