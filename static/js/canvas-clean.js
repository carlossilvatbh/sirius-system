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

    // Canvas interaction methods
    deselectAll() {
        this.selectedElement = null;
        this.selectedStructure = null;
        
        // Clear UI selections
        document.querySelectorAll('.structure-card, .canvas-element').forEach(el => {
            el.classList.remove('selected');
        });
        
        this.exitConnectionMode();
    }

    // Connection mode functionality
    toggleConnectionMode() {
        this.connectionMode = !this.connectionMode;
        const btn = document.getElementById('connection-mode-btn');
        const indicator = document.getElementById('connection-indicator');
        
        if (this.connectionMode) {
            btn.classList.add('active');
            indicator.style.display = 'block';
            document.getElementById('connection-status').textContent = 'Click on a structure to start connecting';
            this.showInfoMessage('Connection mode enabled. Click two structures to connect them.');
        } else {
            this.exitConnectionMode();
        }
    }

    exitConnectionMode() {
        this.connectionMode = false;
        this.connectionSource = null;
        
        const btn = document.getElementById('connection-mode-btn');
        const indicator = document.getElementById('connection-indicator');
        
        if (btn) btn.classList.remove('active');
        if (indicator) indicator.style.display = 'none';
        
        // Remove connection-related classes
        document.querySelectorAll('.canvas-element').forEach(el => {
            el.classList.remove('connection-source', 'connection-target');
        });
    }

    // Zoom functionality
    zoomIn() {
        this.zoomLevel = Math.min(this.zoomLevel + 0.1, 2);
        this.applyZoom();
    }

    zoomOut() {
        this.zoomLevel = Math.max(this.zoomLevel - 0.1, 0.5);
        this.applyZoom();
    }

    resetZoom() {
        this.zoomLevel = 1;
        this.applyZoom();
    }

    applyZoom() {
        const canvasContent = document.querySelector('.canvas-content');
        const canvasGrid = document.getElementById('canvas-grid');
        const zoomLevelDisplay = document.getElementById('zoom-level');
        
        if (canvasContent) {
            canvasContent.style.transform = `scale(${this.zoomLevel})`;
        }
        
        if (canvasGrid) {
            canvasGrid.style.transform = `scale(${this.zoomLevel})`;
        }
        
        if (zoomLevelDisplay) {
            zoomLevelDisplay.textContent = `${Math.round(this.zoomLevel * 100)}%`;
        }
    }

    // History management for undo/redo
    saveToHistory() {
        const state = {
            elements: JSON.parse(JSON.stringify(this.canvasElements)),
            connections: JSON.parse(JSON.stringify(this.connections)),
            timestamp: Date.now()
        };
        
        // Remove any history after current index
        this.history = this.history.slice(0, this.historyIndex + 1);
        
        // Add new state
        this.history.push(state);
        this.historyIndex++;
        
        // Limit history size
        if (this.history.length > 50) {
            this.history.shift();
            this.historyIndex--;
        }
        
        this.updateHistoryButtons();
    }

    undoAction() {
        if (this.historyIndex > 0) {
            this.historyIndex--;
            this.restoreFromHistory();
            this.showInfoMessage('Action undone');
        }
    }

    redoAction() {
        if (this.historyIndex < this.history.length - 1) {
            this.historyIndex++;
            this.restoreFromHistory();
            this.showInfoMessage('Action redone');
        }
    }

    restoreFromHistory() {
        if (this.history[this.historyIndex]) {
            const state = this.history[this.historyIndex];
            this.canvasElements = JSON.parse(JSON.stringify(state.elements));
            this.connections = JSON.parse(JSON.stringify(state.connections));
            this.renderCanvasElements();
            this.updateStats();
            this.updateHistoryButtons();
        }
    }

    updateHistoryButtons() {
        const undoBtn = document.getElementById('undo-btn');
        const redoBtn = document.getElementById('redo-btn');
        
        if (undoBtn) {
            undoBtn.disabled = this.historyIndex <= 0;
        }
        
        if (redoBtn) {
            redoBtn.disabled = this.historyIndex >= this.history.length - 1;
        }
    }

    // Canvas element management
    addElementToCanvas(structure, position) {
        const element = {
            id: `element_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            structure: structure,
            position: position,
            selected: false
        };
        
        this.canvasElements.push(element);
        this.saveToHistory();
        this.renderCanvasElements();
        this.updateStats();
        this.showSuccessMessage(`Added ${structure.nome} to canvas`);
    }

    removeElement(elementId) {
        const elementIndex = this.canvasElements.findIndex(el => el.id === elementId);
        if (elementIndex !== -1) {
            const element = this.canvasElements[elementIndex];
            this.canvasElements.splice(elementIndex, 1);
            
            // Remove related connections
            this.connections = this.connections.filter(conn => 
                conn.from !== elementId && conn.to !== elementId
            );
            
            this.saveToHistory();
            this.renderCanvasElements();
            this.updateStats();
            this.showSuccessMessage(`Removed ${element.structure.nome} from canvas`);
        }
    }

    clearCanvas() {
        if (this.canvasElements.length === 0) return;
        
        if (confirm('Are you sure you want to clear the canvas? This action cannot be undone.')) {
            this.canvasElements = [];
            this.connections = [];
            this.saveToHistory();
            this.renderCanvasElements();
            this.updateStats();
            this.showSuccessMessage('Canvas cleared');
        }
    }

    renderCanvasElements() {
        const canvasElements = document.getElementById('canvas-elements');
        const canvasEmpty = document.getElementById('canvas-empty');
        
        if (!canvasElements || !canvasEmpty) return;
        
        if (this.canvasElements.length === 0) {
            canvasElements.innerHTML = '';
            canvasEmpty.style.display = 'block';
            return;
        }
        
        canvasEmpty.style.display = 'none';
        canvasElements.innerHTML = '';
        
        this.canvasElements.forEach(element => {
            const elementDiv = this.createCanvasElement(element);
            canvasElements.appendChild(elementDiv);
        });
    }

    createCanvasElement(element) {
        const elementDiv = document.createElement('div');
        elementDiv.className = 'canvas-element';
        elementDiv.dataset.elementId = element.id;
        elementDiv.style.left = element.position.x + 'px';
        elementDiv.style.top = element.position.y + 'px';
        
        elementDiv.innerHTML = `
            <div class="canvas-element-header">
                <div class="element-type">${element.structure.tipo}</div>
                <div class="complexity-indicator complexity-${element.structure.complexidade}"></div>
                <button class="canvas-element-remove" onclick="siriusCanvas.removeElement('${element.id}')">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <h3 class="canvas-element-title">${element.structure.nome}</h3>
            <div class="canvas-element-cost">${this.formatCurrency(element.structure.custo_base)}</div>
            <div class="canvas-element-meta">
                <span><i class="fas fa-clock"></i>${element.structure.tempo_implementacao}d</span>
                <span><i class="fas fa-shield-alt"></i>${element.structure.nivel_confidencialidade}/5</span>
            </div>
        `;
        
        // Add event listeners
        elementDiv.addEventListener('mousedown', (e) => this.startDragElement(element, e));
        elementDiv.addEventListener('click', (e) => this.selectElement(element, e));
        
        return elementDiv;
    }

    startDragElement(element, e) {
        if (e.target.classList.contains('canvas-element-remove')) return;
        
        this.isDragging = true;
        this.draggedElement = element;
        
        const rect = e.target.getBoundingClientRect();
        const canvasRect = document.getElementById('canvas-container').getBoundingClientRect();
        
        this.dragOffset = {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };
        
        e.target.classList.add('dragging');
        
        const handleMouseMove = (moveEvent) => {
            if (!this.isDragging) return;
            
            const x = moveEvent.clientX - canvasRect.left - this.dragOffset.x;
            const y = moveEvent.clientY - canvasRect.top - this.dragOffset.y;
            
            element.position.x = Math.max(0, x);
            element.position.y = Math.max(0, y);
            
            e.target.style.left = element.position.x + 'px';
            e.target.style.top = element.position.y + 'px';
        };
        
        const handleMouseUp = () => {
            if (this.isDragging) {
                this.isDragging = false;
                this.draggedElement = null;
                e.target.classList.remove('dragging');
                
                document.removeEventListener('mousemove', handleMouseMove);
                document.removeEventListener('mouseup', handleMouseUp);
                
                this.saveToHistory();
            }
        };
        
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);
    }

    selectElement(element, e) {
        if (e.target.classList.contains('canvas-element-remove')) return;
        
        this.selectedElement = element;
        
        // Update UI selection
        document.querySelectorAll('.canvas-element').forEach(el => {
            el.classList.remove('selected');
        });
        
        const selectedEl = document.querySelector(`[data-element-id="${element.id}"]`);
        if (selectedEl) {
            selectedEl.classList.add('selected');
        }
    }

    // Utility methods
    updateStats() {
        const elementCount = document.getElementById('element-count');
        const totalCost = document.getElementById('total-cost');
        
        if (elementCount) {
            elementCount.textContent = this.canvasElements.length;
        }
        
        if (totalCost) {
            const cost = this.calculateTotalCost();
            totalCost.textContent = this.formatCurrency(cost);
        }
    }

    calculateTotalCost() {
        return this.canvasElements.reduce((total, element) => {
            return total + element.structure.custo_base;
        }, 0);
    }

    recalculateCosts() {
        this.updateStats();
        this.showInfoMessage(`Costs recalculated for ${this.pricingScenario} scenario`);
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    }

    // Mobile functionality
    showMobileDetails(structure) {
        const modal = document.getElementById('mobile-details-modal');
        const modalBody = document.getElementById('mobile-details-body');
        
        if (!modal || !modalBody) return;
        
        modalBody.innerHTML = `
            <div class="structure-details">
                <h4>${structure.nome}</h4>
                <p>${structure.descricao}</p>
                
                <div class="details-grid">
                    <div class="detail-item">
                        <span class="label">Base Cost</span>
                        <span class="value success">${this.formatCurrency(structure.custo_base)}</span>
                    </div>
                    <div class="detail-item">
                        <span class="label">Maintenance</span>
                        <span class="value">${this.formatCurrency(structure.custo_manutencao)}</span>
                    </div>
                    <div class="detail-item">
                        <span class="label">Implementation</span>
                        <span class="value">${structure.tempo_implementacao} days</span>
                    </div>
                    <div class="detail-item">
                        <span class="label">Complexity</span>
                        <span class="value">${structure.complexidade}/5</span>
                    </div>
                </div>
            </div>
        `;
        
        modal.style.display = 'block';
    }

    closeMobileDetails() {
        const modal = document.getElementById('mobile-details-modal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    closeMobileSidebar() {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        
        if (sidebar) sidebar.classList.remove('open');
        if (overlay) overlay.classList.remove('active');
    }

    // Notification system
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
        const container = document.getElementById('messages-container');
        if (!container) return;
        
        const notification = document.createElement('div');
        notification.className = `notification notification-${type} animate-slideIn`;
        notification.innerHTML = `
            <div class="notification-content">
                <div class="notification-icon">
                    <i class="${this.getNotificationIcon(type)}"></i>
                </div>
                <div class="notification-text">
                    <div class="notification-message">${message}</div>
                </div>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        container.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    getNotificationIcon(type) {
        const icons = {
            'success': 'fas fa-check-circle',
            'error': 'fas fa-exclamation-triangle',
            'warning': 'fas fa-exclamation-circle',
            'info': 'fas fa-info-circle'
        };
        return icons[type] || icons.info;
    }

    // Loading states
    showLoading() {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.style.display = 'flex';
        }
    }

    hideLoading() {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
        }
    }

    // Configuration management
    async saveConfiguration() {
        try {
            this.showLoading();
            
            const configuration = {
                elements: this.canvasElements,
                connections: this.connections,
                scenario: this.pricingScenario,
                totalCost: this.calculateTotalCost(),
                timestamp: new Date().toISOString()
            };
            
            // Here you would typically send to your Django backend
            // const response = await fetch(window.djangoData.apiUrls.salvarConfiguracao, {
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/json',
            //         'X-CSRFToken': window.djangoData.csrfToken
            //     },
            //     body: JSON.stringify(configuration)
            // });
            
            // For now, just save to localStorage
            localStorage.setItem('sirius-configuration', JSON.stringify(configuration));
            
            this.showSuccessMessage('Configuration saved successfully');
        } catch (error) {
            console.error('Error saving configuration:', error);
            this.showErrorMessage('Failed to save configuration');
        } finally {
            this.hideLoading();
        }
    }

    async generatePDF() {
        try {
            this.showLoading();
            
            // Simple PDF generation using the canvas
            const canvasContainer = document.getElementById('canvas-container');
            if (!canvasContainer) {
                throw new Error('Canvas container not found');
            }
            
            // Here you would typically use html2canvas and jsPDF
            this.showSuccessMessage('PDF generation started (feature in development)');
            
        } catch (error) {
            console.error('Error generating PDF:', error);
            this.showErrorMessage('Failed to generate PDF');
        } finally {
            this.hideLoading();
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (window.djangoData && window.djangoData.apiUrls) {
        window.siriusCanvas = new SiriusCanvas();
    } else {
        console.error('Django data not available');
    }
});
