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
        
        this.init();
    }

    async init() {
        try {
            this.showLoading();
            await this.loadStructures();
            this.setupEventListeners();
            this.setupResponsiveHandlers();
            this.renderStructures();
            this.updateStats();
            this.showSuccessMessage('Canvas initialized successfully');
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
                if (e.target === canvasContainer) {
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

    filterByCategory(category) {
        this.currentFilter = category;
        this.filterStructures();
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
        card.className = 'structure-card fade-in';
        card.draggable = true;
        card.dataset.structureId = structure.id;

        card.innerHTML = `
            <div class="structure-header">
                <div class="structure-badge">
                    <span class="structure-type">${structure.tipo}</span>
                    <div class="complexity-indicator complexity-${structure.complexidade}"></div>
                </div>
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
            if (btn) btn.classList.add('active');
            if (indicator) indicator.style.display = 'block';
            const status = document.getElementById('connection-status');
            if (status) status.textContent = 'Click on a structure to start connecting';
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

    // History management
    undoAction() {
        this.showInfoMessage('Undo functionality coming soon');
    }

    redoAction() {
        this.showInfoMessage('Redo functionality coming soon');
    }

    clearCanvas() {
        if (this.canvasElements.length === 0) return;
        
        if (confirm('Are you sure you want to clear the canvas? This action cannot be undone.')) {
            this.canvasElements = [];
            this.connections = [];
            this.updateStats();
            this.showSuccessMessage('Canvas cleared');
        }
    }

    removeElement(elementId) {
        this.showInfoMessage('Remove element functionality coming soon');
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
            
            // Save to localStorage for now
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
            this.showSuccessMessage('PDF generation started (feature in development)');
        } catch (error) {
            console.error('Error generating PDF:', error);
            this.showErrorMessage('Failed to generate PDF');
        } finally {
            this.hideLoading();
        }
    }
}

// Global drag and drop handlers
function allowDrop(ev) {
    ev.preventDefault();
    const canvasContainer = document.getElementById('canvas-container');
    if (canvasContainer) {
        canvasContainer.classList.add('drag-over');
    }
}

function handleDragLeave(ev) {
    const canvasContainer = document.getElementById('canvas-container');
    if (canvasContainer) {
        canvasContainer.classList.remove('drag-over');
    }
}

function handleDrop(ev) {
    ev.preventDefault();
    const canvasContainer = document.getElementById('canvas-container');
    if (canvasContainer) {
        canvasContainer.classList.remove('drag-over');
    }
    
    try {
        const data = ev.dataTransfer.getData('text/plain');
        const structure = JSON.parse(data);
        
        // Calculate drop position
        const rect = canvasContainer.getBoundingClientRect();
        const x = ev.clientX - rect.left;
        const y = ev.clientY - rect.top;
        
        // For now, just show a message
        if (window.siriusCanvas) {
            window.siriusCanvas.showSuccessMessage(`Dropped ${structure.nome} at position (${Math.round(x)}, ${Math.round(y)})`);
        }
    } catch (error) {
        console.error('Error handling drop:', error);
        if (window.siriusCanvas) {
            window.siriusCanvas.showErrorMessage('Failed to add structure to canvas');
        }
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    window.siriusCanvas = new SiriusCanvas();
    
    // Make closeMobileDetails globally accessible
    window.closeMobileDetails = function() {
        if (window.siriusCanvas) {
            window.siriusCanvas.closeMobileDetails();
        }
    };
});
