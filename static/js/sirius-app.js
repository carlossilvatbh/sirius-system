// SIRIUS Vue.js Application - Enhanced UX/UI
const { createApp } = Vue;

const SiriusApp = {
    template: `
    <div class="sirius-container">
        <!-- Loading State -->
        <div v-if="loading" class="loading-overlay">
            <div class="text-center">
                <div class="loading-spinner mx-auto mb-4"></div>
                <p class="text-gray-600 font-medium">Loading SIRIUS...</p>
            </div>
        </div>
        
        <!-- Mobile Menu Button -->
        <button 
            v-if="isMobile" 
            @click="toggleMobileSidebar"
            class="fixed top-4 left-4 z-50 btn btn-primary lg:hidden"
        >
            <i class="fas fa-bars"></i>
        </button>
        
        <!-- Mobile Overlay -->
        <div 
            v-if="isMobile && mobileSidebarOpen" 
            @click="closeMobileSidebar"
            class="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
        ></div>
        
        <!-- Left Sidebar - Structure Library -->
        <div class="sidebar" :class="{ 'open': mobileSidebarOpen }">
            <!-- Close button for mobile -->
            <button 
                v-if="isMobile"
                @click="closeMobileSidebar"
                class="absolute top-4 right-4 text-gray-500 hover:text-gray-700 z-10 lg:hidden"
            >
                <i class="fas fa-times text-xl"></i>
            </button>
            
            <!-- Sidebar Header -->
            <div class="sidebar-header">
                <h2>
                    <i class="fas fa-layer-group"></i>
                    Structure Library
                </h2>
                <p>Drag structures to the canvas to build your configuration</p>
            </div>
            
            <!-- Search and Filters -->
            <div class="search-filters">
                <div class="search-container">
                    <input 
                        type="text" 
                        v-model="searchQuery"
                        placeholder="Search structures..."
                        class="search-input"
                        @input="handleSearchInput"
                    >
                    <i class="fas fa-search search-icon"></i>
                </div>
                
                <select 
                    v-model="selectedCategory"
                    class="filter-select"
                    @change="filterStructures"
                >
                    <option value="">All Categories</option>
                    <option value="BDAO_SAC">Bahamas DAO SAC</option>
                    <option value="WYOMING_DAO_LLC">Wyoming DAO LLC</option>
                    <option value="BTS_VAULT">BTS Vault</option>
                    <option value="WYOMING_FOUNDATION">Wyoming Foundation</option>
                    <option value="WYOMING_CORP">Wyoming Corporation</option>
                    <option value="NATIONALIZATION">Nationalization</option>
                    <option value="FUND_TOKEN">Fund Token</option>
                </select>
            </div>
            
            <!-- Structure Cards -->
            <div class="p-4 space-y-3">
                <div 
                    v-for="estrutura in filteredEstruturas" 
                    :key="estrutura.id"
                    class="structure-card animate-fadeIn"
                    draggable="true"
                    @dragstart="iniciarDrag(estrutura, $event)"
                    @click="selecionarEstrutura(estrutura)"
                    :class="{ 'ring-2 ring-blue-500': estruturaSelecionada?.id === estrutura.id }"
                >
                    <div class="complexity-indicator" :class="'complexity-' + estrutura.complexidade"></div>
                    <div class="structure-type">{{ estrutura.tipo }}</div>
                    <div class="structure-name">{{ estrutura.nome }}</div>
                    <div class="structure-cost">{{ formatCurrency(estrutura.custo_base) }}</div>
                    <div class="structure-meta">
                        <span><i class="fas fa-clock mr-1"></i>{{ estrutura.tempo_implementacao }} days</span>
                        <span><i class="fas fa-shield-alt mr-1"></i>{{ estrutura.nivel_confidencialidade }}/5</span>
                    </div>
                </div>
                
                <!-- No Results State -->
                <div v-if="filteredEstruturas.length === 0" class="text-center py-8">
                    <i class="fas fa-search text-3xl text-gray-300 mb-4"></i>
                    <p class="text-gray-500 font-medium">No structures found</p>
                    <p class="text-gray-400 text-sm">Try adjusting your search criteria</p>
                </div>
            </div>
            
            <!-- Templates Section -->
            <div class="p-4 border-t border-gray-200">
                <h3 class="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
                    <i class="fas fa-clipboard-list text-blue-600"></i>
                    Quick Templates
                </h3>
                <div class="space-y-3">
                    <div 
                        v-for="template in templates" 
                        :key="template.id"
                        class="template-card cursor-pointer p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200 hover:border-blue-300 transition-all duration-300 hover:shadow-md"
                        @click="carregarTemplate(template.id)"
                    >
                        <div class="template-category text-xs font-semibold text-blue-600 uppercase tracking-wide">{{ template.categoria }}</div>
                        <div class="template-name font-bold text-gray-900 mt-1">{{ template.nome }}</div>
                        <div class="template-description text-sm text-gray-600 mt-1">{{ template.descricao }}</div>
                        <div class="template-stats flex justify-between items-center mt-3 text-sm">
                            <span class="font-semibold text-green-600">{{ formatCurrency(template.custo_total || 0) }}</span>
                            <span class="text-gray-500">{{ template.uso_count || 0 }} uses</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Main Content Area -->
        <div class="flex-1 flex flex-col">
            <!-- Top Toolbar -->
            <div class="bg-white border-b border-gray-200 p-4 shadow-sm">
                <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
                    <div class="flex flex-wrap items-center gap-2">
                        <button 
                            @click="limparCanvas"
                            class="btn btn-secondary"
                            :disabled="elementos.length === 0"
                            data-tooltip="Clear all elements"
                        >
                            <i class="fas fa-trash"></i>
                            <span class="hidden sm:inline">Clear</span>
                        </button>
                        
                        <button 
                            @click="undoAction"
                            class="btn btn-secondary tooltip"
                            :disabled="!canUndo"
                            data-tooltip="Undo (Ctrl+Z)"
                        >
                            <i class="fas fa-undo"></i>
                        </button>
                        
                        <button 
                            @click="redoAction"
                            class="btn btn-secondary tooltip"
                            :disabled="!canRedo"
                            data-tooltip="Redo (Ctrl+Y)"
                        >
                            <i class="fas fa-redo"></i>
                        </button>
                        
                        <button 
                            @click="toggleGridSnap"
                            class="btn btn-secondary tooltip"
                            :class="{ 'btn-primary': snapToGrid }"
                            data-tooltip="Toggle Grid Snap (G)"
                        >
                            <i class="fas fa-th"></i>
                        </button>
                        
                        <button 
                            @click="toggleConnectionMode"
                            class="btn btn-secondary tooltip"
                            :class="{ 'btn-primary': connectingMode }"
                            data-tooltip="Connect Structures (C)"
                        >
                            <i class="fas fa-link"></i>
                        </button>
                        
                        <button 
                            @click="fitCanvasToContent"
                            class="btn btn-secondary tooltip"
                            :disabled="elementos.length === 0"
                            data-tooltip="Fit to Content"
                        >
                            <i class="fas fa-expand-arrows-alt"></i>
                        </button>
                        
                        <div class="hidden lg:block w-px h-6 bg-gray-300"></div>
                        
                        <button 
                            @click="salvarConfiguracao"
                            class="btn btn-primary"
                            :disabled="elementos.length === 0"
                        >
                            <i class="fas fa-save"></i>
                            <span class="hidden sm:inline">Save</span>
                        </button>
                        
                        <button 
                            @click="gerarPDF"
                            class="btn btn-success"
                            :disabled="elementos.length === 0"
                        >
                            <i class="fas fa-file-pdf"></i>
                            <span class="hidden sm:inline">PDF</span>
                        </button>
                    </div>
                    
                    <div class="flex flex-col sm:flex-row items-start sm:items-center gap-3">
                        <!-- Pricing Scenario Selector -->
                        <div class="flex items-center gap-2">
                            <label class="text-sm font-medium text-gray-700">Scenario:</label>
                            <select 
                                v-model="cenarioPrecificacao"
                                class="filter-select min-w-[140px]"
                                @change="recalcularCustos"
                            >
                                <option value="basico">Basic</option>
                                <option value="completo">Complete</option>
                                <option value="premium">Premium</option>
                            </select>
                        </div>
                        
                        <!-- Total Cost Display -->
                        <div class="bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-lg px-4 py-3 shadow-sm">
                            <div class="text-xs text-green-600 font-semibold uppercase tracking-wide">Total Cost</div>
                            <div class="text-xl font-bold text-green-800">
                                {{ formatCurrency(custoTotalComCenario) }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Canvas Container -->
            <div class="flex-1 relative bg-gray-50">
                <!-- Connection Mode Indicator -->
                <div v-if="connectingMode" class="connecting-mode-indicator">
                    <i class="fas fa-link mr-2"></i>
                    Connection Mode: {{ connectionStart ? 'Select target structure' : 'Select source structure' }}
                </div>
                
                <div 
                    ref="canvasContainer"
                    class="canvas-container w-full h-full"
                    @dragover="permitirDrop"
                    @drop="handleDrop"
                    @click="deselecionarTudo"
                >
                    <!-- Connections SVG Layer -->
                    <svg 
                        class="absolute inset-0 w-full h-full pointer-events-none"
                        style="z-index: 1;"
                    >
                        <defs>
                            <marker id="arrowhead" markerWidth="10" markerHeight="7" 
                                refX="9" refY="3.5" orient="auto">
                                <polygon points="0 0, 10 3.5, 0 7" fill="#3B82F6" />
                            </marker>
                        </defs>
                        
                        <!-- Existing connections -->
                        <g v-for="connection in connections" :key="connection.id">
                            <path 
                                :d="getConnectionPath(connection)"
                                stroke="#3B82F6"
                                stroke-width="2"
                                fill="none"
                                marker-end="url(#arrowhead)"
                                class="connection-path"
                            />
                            <text 
                                :x="getConnectionMidpoint(connection).x"
                                :y="getConnectionMidpoint(connection).y - 5"
                                text-anchor="middle"
                                class="connection-label"
                                font-size="12"
                                fill="#374151"
                            >
                                {{ connection.label || 'Connection' }}
                            </text>
                        </g>
                        
                        <!-- Temporary connection while drawing -->
                        <path 
                            v-if="connectionStart && connectionEnd"
                            :d="getTempConnectionPath()"
                            stroke="#3B82F6"
                            stroke-width="2"
                            stroke-dasharray="5,5"
                            fill="none"
                            marker-end="url(#arrowhead)"
                            class="temp-connection"
                        />
                    </svg>
                    
                    <!-- Canvas Elements -->
                    <div class="relative w-full h-full p-4 sm:p-8" style="z-index: 2;">
                        <div 
                            v-for="elemento in elementos" 
                            :key="elemento.id"
                            class="canvas-element"
                            :style="{ 
                                left: elemento.position.x + 'px', 
                                top: elemento.position.y + 'px',
                                width: isMobile ? '180px' : '220px'
                            }"
                            @mousedown="iniciarArrastar(elemento, $event)"
                            @touchstart="iniciarArrastar(elemento, $event)"
                            @click.stop="handleElementClick(elemento)"
                            :class="{ 
                                'selected': elementoSelecionado?.id === elemento.id,
                                'connecting': connectingMode,
                                'connection-source': connectionStart?.id === elemento.id,
                                'connection-target': connectionEnd?.id === elemento.id
                            }"
                        >
                            <div class="flex justify-between items-start mb-2">
                                <div class="text-sm font-bold text-gray-900">{{ elemento.estrutura.nome }}</div>
                                <button 
                                    @click.stop="removerElemento(elemento.id)"
                                    class="text-red-500 hover:text-red-700 hover:bg-red-50 rounded-full p-1 transition-colors"
                                >
                                    <i class="fas fa-times text-xs"></i>
                                </button>
                            </div>
                            
                            <div class="text-xs text-gray-500 mb-2">{{ elemento.estrutura.tipo }}</div>
                            
                            <div class="flex justify-between items-center">
                                <div class="text-sm font-bold text-green-600">
                                    {{ formatCurrency(elemento.estrutura.custo_base) }}
                                </div>
                                <div class="complexity-indicator" :class="'complexity-' + elemento.estrutura.complexidade"></div>
                            </div>
                            
                            <div class="mt-2 text-xs text-gray-400 flex items-center gap-2">
                                <span><i class="fas fa-clock mr-1"></i>{{ elemento.estrutura.tempo_implementacao }}d</span>
                                <span><i class="fas fa-shield-alt mr-1"></i>{{ elemento.estrutura.nivel_confidencialidade }}/5</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Enhanced Empty State -->
                    <div v-if="elementos.length === 0" class="empty-state">
                        <div class="animate-bounce">
                            <i class="fas fa-network-wired"></i>
                        </div>
                        <h3>Start Building Your Structure</h3>
                        <p>Drag legal structures from the sidebar to begin designing your optimal configuration</p>
                        <button 
                            v-if="isMobile"
                            @click="openMobileSidebar"
                            class="btn btn-primary mt-4"
                        >
                            <i class="fas fa-plus mr-2"></i>
                            Add Structure
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- Right Sidebar - Information Panel (Desktop Only) -->
            <div v-if="!isMobile" class="w-96 bg-white shadow-lg border-l border-gray-200 overflow-y-auto">
                <!-- Structure Information -->
                <div v-if="estruturaSelecionada" class="p-6">
                    <div class="info-panel">
                        <h3>
                            <i class="fas fa-info-circle"></i>
                            Structure Details
                        </h3>
                        
                        <div class="space-y-4">
                            <div>
                                <h4 class="font-bold text-gray-900 mb-3">{{ estruturaSelecionada.nome }}</h4>
                                <p class="text-sm text-gray-600 leading-relaxed">{{ estruturaSelecionada.descricao }}</p>
                            </div>
                            
                            <div class="grid grid-cols-1 gap-2">
                                <div class="metric">
                                    <span class="metric-label">Base Cost</span>
                                    <span class="metric-value success">{{ formatCurrency(estruturaSelecionada.custo_base) }}</span>
                                </div>
                                
                                <div class="metric">
                                    <span class="metric-label">Annual Maintenance</span>
                                    <span class="metric-value">{{ formatCurrency(estruturaSelecionada.custo_manutencao) }}</span>
                                </div>
                                
                                <div class="metric">
                                    <span class="metric-label">Implementation Time</span>
                                    <span class="metric-value">{{ estruturaSelecionada.tempo_implementacao }} days</span>
                                </div>
                                
                                <div class="metric">
                                    <span class="metric-label">Complexity</span>
                                    <span class="metric-value" :class="getComplexityClass(estruturaSelecionada.complexidade)">
                                        {{ estruturaSelecionada.complexidade }}/5
                                    </span>
                                </div>
                                
                                <div class="metric">
                                    <span class="metric-label">Confidentiality Level</span>
                                    <span class="metric-value">{{ estruturaSelecionada.nivel_confidencialidade }}/5</span>
                                </div>
                                
                                <div class="metric">
                                    <span class="metric-label">Asset Protection</span>
                                    <span class="metric-value">{{ estruturaSelecionada.protecao_patrimonial }}/5</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Tax Information -->
                    <div class="info-panel">
                        <h3>
                            <i class="fas fa-calculator"></i>
                            Tax Implications
                        </h3>
                        
                        <div class="space-y-4">
                            <div>
                                <h4 class="font-semibold text-gray-900 mb-2 flex items-center gap-2">
                                    <i class="fas fa-flag-usa text-blue-600"></i>
                                    United States
                                </h4>
                                <p class="text-sm text-gray-600 leading-relaxed">{{ estruturaSelecionada.impacto_tributario_eua }}</p>
                            </div>
                            
                            <div>
                                <h4 class="font-semibold text-gray-900 mb-2 flex items-center gap-2">
                                    <i class="fas fa-flag text-green-600"></i>
                                    Brazil
                                </h4>
                                <p class="text-sm text-gray-600 leading-relaxed">{{ estruturaSelecionada.impacto_tributario_brasil }}</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Canvas Summary -->
                <div v-if="elementos.length > 0" class="p-6 border-t border-gray-200">
                    <div class="info-panel">
                        <h3>
                            <i class="fas fa-chart-line"></i>
                            Configuration Summary
                        </h3>
                        
                        <div class="space-y-3">
                            <div class="metric">
                                <span class="metric-label">Total Structures</span>
                                <span class="metric-value">{{ elementos.length }}</span>
                            </div>
                            
                            <div class="metric">
                                <span class="metric-label">Total Setup Cost</span>
                                <span class="metric-value success">{{ formatCurrency(custoTotalSetup) }}</span>
                            </div>
                            
                            <div class="metric">
                                <span class="metric-label">Annual Maintenance</span>
                                <span class="metric-value">{{ formatCurrency(custoTotalManutencao) }}</span>
                            </div>
                            
                            <div class="metric">
                                <span class="metric-label">Avg. Implementation</span>
                                <span class="metric-value">{{ tempoMedioImplementacao }} days</span>
                            </div>
                            
                            <div class="metric">
                                <span class="metric-label">Avg. Complexity</span>
                                <span class="metric-value" :class="getComplexityClass(complexidadeMedia)">
                                    {{ complexidadeMedia.toFixed(1) }}/5
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Mobile Bottom Sheet for Structure Details -->
            <div v-if="isMobile && estruturaSelecionada" class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 rounded-t-xl shadow-2xl z-30 transform transition-transform duration-300"
                 :class="{ 'translate-y-0': showMobileDetails, 'translate-y-full': !showMobileDetails }">
                <div class="p-4">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-lg font-bold text-gray-900">{{ estruturaSelecionada.nome }}</h3>
                        <button @click="closeMobileDetails" class="text-gray-500 hover:text-gray-700">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    
                    <div class="max-h-64 overflow-y-auto">
                        <p class="text-sm text-gray-600 mb-4">{{ estruturaSelecionada.descricao }}</p>
                        
                        <div class="grid grid-cols-2 gap-4 text-sm">
                            <div>
                                <span class="text-gray-500">Base Cost</span>
                                <div class="font-semibold text-green-600">{{ formatCurrency(estruturaSelecionada.custo_base) }}</div>
                            </div>
                            <div>
                                <span class="text-gray-500">Implementation</span>
                                <div class="font-semibold">{{ estruturaSelecionada.tempo_implementacao }} days</div>
                            </div>
                            <div>
                                <span class="text-gray-500">Complexity</span>
                                <div class="font-semibold">{{ estruturaSelecionada.complexidade }}/5</div>
                            </div>
                            <div>
                                <span class="text-gray-500">Confidentiality</span>
                                <div class="font-semibold">{{ estruturaSelecionada.nivel_confidencialidade }}/5</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Notifications -->
            <div class="fixed top-4 right-4 z-50 space-y-2">
                <div 
                    v-for="notification in notifications" 
                    :key="notification.id"
                    class="validation-alert animate-slideIn"
                    :class="notification.type"
                >
                    <div class="flex items-center gap-3">
                        <i :class="getNotificationIcon(notification.type)"></i>
                        <div>
                            <div class="font-semibold">{{ notification.title }}</div>
                            <div class="text-sm opacity-90">{{ notification.message }}</div>
                        </div>
                        <button @click="removeNotification(notification.id)" class="ml-auto text-gray-500 hover:text-gray-700">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `,
    
    data() {
        return {
            // Structure data
            estruturas: [],
            templates: [],
            
            // Canvas elements
            elementos: [],
            conexoes: [],
            elementoSelecionado: null,
            estruturaSelecionada: null,
            
            // UI state
            searchQuery: '',
            selectedCategory: '',
            cenarioPrecificacao: 'basico',
            loading: true,
            
            // Mobile responsiveness
            isMobile: false,
            mobileSidebarOpen: false,
            showMobileDetails: false,
            
            // Notifications
            notifications: [],
            notificationId: 0,
            
            // Undo/Redo
            history: [],
            historyIndex: -1,
            
            // Drag and drop state
            draggedElement: null,
            isDragging: false,
            dragOffset: { x: 0, y: 0 },
            
            // Connections between structures
            connections: [],
            connectingMode: false,
            connectionStart: null,
            connectionEnd: null,
            
            // Validation
            validacao: {
                valido: true,
                erros: [],
                alertas: [],
                sugestoes: []
            },
            
            // Costs and timing
            custoTotal: 0,
            tempoTotal: 0,
            analiseDetalhada: null,
            
            // Advanced canvas features
            advancedCanvas: null,
            showGrid: true,
            snapToGrid: true
        }
    },
    
    computed: {
        filteredEstruturas() {
            let filtered = this.estruturas;
            
            // Filter by search query
            if (this.searchQuery) {
                const query = this.searchQuery.toLowerCase();
                filtered = filtered.filter(estrutura => 
                    estrutura.nome.toLowerCase().includes(query) ||
                    estrutura.descricao.toLowerCase().includes(query) ||
                    estrutura.tipo.toLowerCase().includes(query)
                );
            }
            
            // Filter by category
            if (this.selectedCategory) {
                filtered = filtered.filter(estrutura => 
                    estrutura.tipo === this.selectedCategory
                );
            }
            
            return filtered;
        },
        
        custoTotalComCenario() {
            let multiplicador = 1;
            switch (this.cenarioPrecificacao) {
                case 'completo':
                    multiplicador = 1.3;
                    break;
                case 'premium':
                    multiplicador = 1.6;
                    break;
            }
            return this.custoTotalSetup * multiplicador;
        },
        
        custoTotalSetup() {
            return this.elementos.reduce((total, elemento) => 
                total + parseFloat(elemento.estrutura.custo_base || 0), 0
            );
        },
        
        custoTotalManutencao() {
            return this.elementos.reduce((total, elemento) => 
                total + parseFloat(elemento.estrutura.custo_manutencao || 0), 0
            );
        },
        
        tempoMedioImplementacao() {
            if (this.elementos.length === 0) return 0;
            const tempoTotal = this.elementos.reduce((total, elemento) => 
                total + elemento.estrutura.tempo_implementacao, 0
            );
            return Math.round(tempoTotal / this.elementos.length);
        },
        
        complexidadeMedia() {
            if (this.elementos.length === 0) return 0;
            const complexidadeTotal = this.elementos.reduce((total, elemento) => 
                total + elemento.estrutura.complexidade, 0
            );
            return complexidadeTotal / this.elementos.length;
        },
        
        canUndo() {
            return this.historyIndex > 0;
        },
        
        canRedo() {
            return this.historyIndex < this.history.length - 1;
        }
    },
    
    mounted() {
        this.initializeApp();
        this.checkMobile();
        this.configurarEventListeners();
        
        // Initialize advanced canvas features
        this.$nextTick(() => {
            if (window.SiriusCanvasAdvanced) {
                this.advancedCanvas = new window.SiriusCanvasAdvanced(this);
            }
        });
    },
    
    methods: {
        async initializeApp() {
            try {
                await this.carregarDados();
                this.configurarEventListeners();
            } catch (error) {
                console.error('Error initializing app:', error);
                this.showNotification('Failed to initialize application', 'error');
            } finally {
                this.loading = false;
            }
        },
        
        async carregarDados() {
            try {
                const [estruturasRes, templatesRes] = await Promise.all([
                    fetch(window.djangoData.apiUrls.estruturas),
                    fetch(window.djangoData.apiUrls.templates)
                ]);
                
                if (!estruturasRes.ok || !templatesRes.ok) {
                    throw new Error('Failed to fetch data');
                }
                
                this.estruturas = await estruturasRes.json();
                this.templates = await templatesRes.json();
                
                console.log('Loaded', this.estruturas.length, 'structures and', this.templates.length, 'templates');
            } catch (error) {
                console.error('Error loading data:', error);
                // Fallback to empty arrays
                this.estruturas = [];
                this.templates = [];
            }
        },
        
        configurarEventListeners() {
            // Global event listeners
            document.addEventListener('keydown', this.handleKeydown);
            window.addEventListener('resize', this.handleResize);
            
            // Mouse events for dragging
            document.addEventListener('mousemove', this.handleMouseMove);
            document.addEventListener('mouseup', this.handleMouseUp);
        },
        
        // Mobile responsiveness methods
        checkMobile() {
            this.isMobile = window.innerWidth < 768;
            window.addEventListener('resize', () => {
                this.isMobile = window.innerWidth < 768;
                if (!this.isMobile) {
                    this.mobileSidebarOpen = false;
                    this.showMobileDetails = false;
                }
            });
        },
        
        toggleMobileSidebar() {
            this.mobileSidebarOpen = !this.mobileSidebarOpen;
        },
        
        openMobileSidebar() {
            this.mobileSidebarOpen = true;
        },
        
        closeMobileSidebar() {
            this.mobileSidebarOpen = false;
        },
        
        closeMobileDetails() {
            this.showMobileDetails = false;
            this.estruturaSelecionada = null;
        },
        
        // Enhanced search functionality
        handleSearchInput() {
            // Add debouncing for better performance
            clearTimeout(this.searchTimeout);
            this.searchTimeout = setTimeout(() => {
                if (this.searchQuery.length === 0) {
                    this.selectedCategory = '';
                }
            }, 300);
        },
        
        filterStructures() {
            // This will trigger the computed property
            this.$forceUpdate();
        },
        
        // Notification system
        showNotification(message, type = 'info', title = '') {
            const notification = {
                id: this.notificationId++,
                message,
                type,
                title: title || this.getNotificationTitle(type),
                timestamp: Date.now()
            };
            
            this.notifications.push(notification);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                this.removeNotification(notification.id);
            }, 5000);
        },
        
        removeNotification(id) {
            const index = this.notifications.findIndex(n => n.id === id);
            if (index > -1) {
                this.notifications.splice(index, 1);
            }
        },
        
        getNotificationTitle(type) {
            const titles = {
                success: 'Success',
                error: 'Error',
                warning: 'Warning',
                info: 'Information'
            };
            return titles[type] || 'Notification';
        },
        
        getNotificationIcon(type) {
            const icons = {
                success: 'fas fa-check-circle',
                error: 'fas fa-exclamation-triangle',
                warning: 'fas fa-exclamation-circle',
                info: 'fas fa-info-circle'
            };
            return icons[type] || 'fas fa-info-circle';
        },
        
        // History management for undo/redo
        saveToHistory() {
            // Remove future history if we're in the middle
            if (this.historyIndex < this.history.length - 1) {
                this.history.splice(this.historyIndex + 1);
            }
            
            // Add current state to history
            this.history.push(JSON.parse(JSON.stringify(this.elementos)));
            this.historyIndex++;
            
            // Limit history size
            if (this.history.length > 50) {
                this.history.shift();
                this.historyIndex--;
            }
        },
        
        undoAction() {
            if (this.canUndo) {
                this.historyIndex--;
                this.elementos = JSON.parse(JSON.stringify(this.history[this.historyIndex]));
                this.showNotification('Action undone', 'info');
            }
        },
        
        redoAction() {
            if (this.canRedo) {
                this.historyIndex++;
                this.elementos = JSON.parse(JSON.stringify(this.history[this.historyIndex]));
                this.showNotification('Action redone', 'info');
            }
        },
        
        // Drag and Drop Methods
        iniciarDrag(estrutura, event) {
            this.draggedElement = estrutura;
            
            // Set drag data
            if (event.dataTransfer) {
                event.dataTransfer.setData('estrutura', JSON.stringify(estrutura));
                event.dataTransfer.effectAllowed = 'copy';
                
                // Set drag image for better UX
                const dragImage = event.target.cloneNode(true);
                dragImage.style.transform = 'rotate(5deg)';
                dragImage.style.opacity = '0.8';
                event.dataTransfer.setDragImage(dragImage, 50, 50);
            }
            
            if (this.isMobile) {
                this.closeMobileSidebar();
            }
        },
        
        permitirDrop(event) {
            event.preventDefault();
            event.dataTransfer.dropEffect = 'copy';
        },
        
        async handleDrop(event) {
            event.preventDefault();
            
            try {
                let estruturaData;
                
                // Try to get data from dataTransfer first
                try {
                    estruturaData = JSON.parse(event.dataTransfer.getData('estrutura'));
                } catch (e) {
                    // Fallback to draggedElement if dataTransfer fails
                    if (this.draggedElement) {
                        estruturaData = this.draggedElement;
                    } else {
                        throw new Error('No structure data available');
                    }
                }
                
                // Calculate position relative to canvas
                const canvasRect = this.$refs.canvasContainer.getBoundingClientRect();
                const x = event.clientX - canvasRect.left;
                const y = event.clientY - canvasRect.top;
                
                // Create new element
                const novoElemento = {
                    id: `estrutura_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
                    estrutura_id: estruturaData.id,
                    estrutura: estruturaData,
                    position: { x: Math.max(0, x - 100), y: Math.max(0, y - 50) },
                    type: 'estrutura'
                };
                
                this.elementos.push(novoElemento);
                this.saveToHistory();
                this.calcularTotais();
                await this.validarConfiguracao();
                
                this.showNotification(`Added ${estruturaData.nome} to canvas`, 'success');
                
                // Clear dragged element
                this.draggedElement = null;
                
            } catch (error) {
                console.error('Error handling drop:', error);
                this.showNotification('Failed to add structure to canvas', 'error');
            }
        },
        
        // Element Management
        selecionarEstrutura(estrutura) {
            this.estruturaSelecionada = estrutura;
            
            if (this.isMobile) {
                this.showMobileDetails = true;
                this.closeMobileSidebar();
            }
        },
        
        handleElementClick(elemento) {
            if (this.connectingMode) {
                this.handleConnectionClick(elemento);
            } else {
                this.selecionarElemento(elemento);
            }
        },
        
        selecionarElemento(elemento) {
            this.elementoSelecionado = elemento;
            this.estruturaSelecionada = elemento.estrutura;
            
            if (this.isMobile) {
                this.showMobileDetails = true;
            }
        },
        
        // Connection Management
        toggleConnectionMode() {
            this.connectingMode = !this.connectingMode;
            
            if (this.connectingMode) {
                this.showNotification('Connection mode enabled. Click two structures to connect them.', 'info');
                this.connectionStart = null;
                this.connectionEnd = null;
            } else {
                this.showNotification('Connection mode disabled.', 'info');
                this.connectionStart = null;
                this.connectionEnd = null;
            }
        },
        
        handleConnectionClick(elemento) {
            if (!this.connectionStart) {
                // First click - set source
                this.connectionStart = elemento;
                this.showNotification(`Selected ${elemento.estrutura.nome} as connection source.`, 'info');
            } else if (this.connectionStart.id === elemento.id) {
                // Same element clicked - deselect
                this.connectionStart = null;
                this.showNotification('Connection source deselected.', 'info');
            } else {
                // Second click - create connection
                this.connectionEnd = elemento;
                this.createConnection();
            }
        },
        
        createConnection() {
            if (!this.connectionStart || !this.connectionEnd) return;
            
            // Check if connection already exists
            const existingConnection = this.connections.find(conn => 
                (conn.from === this.connectionStart.id && conn.to === this.connectionEnd.id) ||
                (conn.from === this.connectionEnd.id && conn.to === this.connectionStart.id)
            );
            
            if (existingConnection) {
                this.showNotification('Connection already exists between these structures.', 'warning');
                this.connectionStart = null;
                this.connectionEnd = null;
                return;
            }
            
            // Create new connection
            const connection = {
                id: `connection_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
                from: this.connectionStart.id,
                to: this.connectionEnd.id,
                label: this.getConnectionLabel(this.connectionStart.estrutura, this.connectionEnd.estrutura),
                type: 'flow'
            };
            
            this.connections.push(connection);
            this.saveToHistory();
            
            this.showNotification(`Connected ${this.connectionStart.estrutura.nome} to ${this.connectionEnd.estrutura.nome}`, 'success');
            
            // Reset connection state
            this.connectionStart = null;
            this.connectionEnd = null;
        },
        
        getConnectionLabel(estrutura1, estrutura2) {
            // Generate intelligent connection labels based on structure types
            const type1 = estrutura1.tipo;
            const type2 = estrutura2.tipo;
            
            if (type1.includes('DAO') && type2.includes('VAULT')) {
                return 'Asset Flow';
            } else if (type1.includes('FOUNDATION') && type2.includes('CORP')) {
                return 'Ownership';
            } else if (type1.includes('FUND') && type2.includes('TOKEN')) {
                return 'Investment';
            } else {
                return 'Connection';
            }
        },
        
        getConnectionPath(connection) {
            const fromElement = this.elementos.find(el => el.id === connection.from);
            const toElement = this.elementos.find(el => el.id === connection.to);
            
            if (!fromElement || !toElement) return '';
            
            const fromCenter = this.getElementCenter(fromElement);
            const toCenter = this.getElementCenter(toElement);
            
            // Create curved connection path
            const dx = toCenter.x - fromCenter.x;
            const dy = toCenter.y - fromCenter.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            const controlOffset = Math.min(distance * 0.3, 100);
            const controlX1 = fromCenter.x + controlOffset;
            const controlY1 = fromCenter.y;
            const controlX2 = toCenter.x - controlOffset;
            const controlY2 = toCenter.y;
            
            return `M ${fromCenter.x} ${fromCenter.y} C ${controlX1} ${controlY1}, ${controlX2} ${controlY2}, ${toCenter.x} ${toCenter.y}`;
        },
        
        getTempConnectionPath() {
            if (!this.connectionStart || !this.connectionEnd) return '';
            
            const fromCenter = this.getElementCenter(this.connectionStart);
            const toCenter = this.getElementCenter(this.connectionEnd);
            
            return `M ${fromCenter.x} ${fromCenter.y} L ${toCenter.x} ${toCenter.y}`;
        },
        
        getConnectionMidpoint(connection) {
            const fromElement = this.elementos.find(el => el.id === connection.from);
            const toElement = this.elementos.find(el => el.id === connection.to);
            
            if (!fromElement || !toElement) return { x: 0, y: 0 };
            
            const fromCenter = this.getElementCenter(fromElement);
            const toCenter = this.getElementCenter(toElement);
            
            return {
                x: (fromCenter.x + toCenter.x) / 2,
                y: (fromCenter.y + toCenter.y) / 2
            };
        },
        
        getElementCenter(elemento) {
            const width = this.isMobile ? 180 : 220;
            const height = 120; // Approximate height of canvas element
            
            return {
                x: elemento.position.x + width / 2,
                y: elemento.position.y + height / 2
            };
        },
        
        removeConnection(connectionId) {
            this.connections = this.connections.filter(conn => conn.id !== connectionId);
            this.saveToHistory();
            this.showNotification('Connection removed', 'info');
        },
        
        // Canvas Management
        limparCanvas() {
            if (this.elementos.length === 0) return;
            
            if (confirm('Are you sure you want to clear the canvas?')) {
                this.elementos = [];
                this.connections = [];
                this.elementoSelecionado = null;
                this.estruturaSelecionada = null;
                this.connectingMode = false;
                this.connectionStart = null;
                this.connectionEnd = null;
                this.calcularTotais();
                this.validacao = {
                    valido: true,
                    erros: [],
                    alertas: [],
                    sugestoes: []
                };
                
                this.showNotification('Canvas cleared', 'info');
                this.saveToHistory();
            }
        },
        
        // Method to handle clicking outside to deselect
        deselecionarTudo() {
            if (this.connectingMode) {
                this.connectionStart = null;
                this.connectionEnd = null;
            } else {
                this.elementoSelecionado = null;
                this.estruturaSelecionada = null;
            }
        },
        
        // Keyboard shortcuts
        handleKeydown(event) {
            if (event.ctrlKey || event.metaKey) {
                switch (event.key) {
                    case 'z':
                        event.preventDefault();
                        this.undoAction();
                        break;
                    case 'y':
                        event.preventDefault();
                        this.redoAction();
                        break;
                    case 's':
                        event.preventDefault();
                        if (this.elementos.length > 0) {
                            this.salvarConfiguracao();
                        }
                        break;
                }
            } else {
                switch (event.key) {
                    case 'c':
                        this.toggleConnectionMode();
                        break;
                    case 'g':
                        this.toggleGridSnap();
                        break;
                    case 'Escape':
                        if (this.connectingMode) {
                            this.toggleConnectionMode();
                        }
                        break;
                    case 'Delete':
                    case 'Backspace':
                        if (this.elementoSelecionado) {
                            event.preventDefault();
                            this.removerElemento(this.elementoSelecionado.id);
                        }
                        break;
                }
            }
        },
        
        // Other missing methods
        toggleGridSnap() {
            this.snapToGrid = !this.snapToGrid;
            this.showNotification(`Grid snap ${this.snapToGrid ? 'enabled' : 'disabled'}`, 'info');
        },
        
        fitCanvasToContent() {
            if (this.elementos.length === 0) return;
            this.showNotification('Fit to content - feature coming soon', 'info');
        },
        
        removerElemento(elementId) {
            this.elementos = this.elementos.filter(el => el.id !== elementId);
            
            // Remove any connections involving this element
            this.connections = this.connections.filter(conn => 
                conn.from !== elementId && conn.to !== elementId
            );
            
            this.elementoSelecionado = null;
            this.estruturaSelecionada = null;
            this.calcularTotais();
            this.saveToHistory();
            this.showNotification('Element removed', 'info');
        },
    }
};

createApp(SiriusApp).mount('#sirius-app');

