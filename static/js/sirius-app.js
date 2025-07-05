// SIRIUS Vue.js Application
const { createApp } = Vue;

const SiriusApp = {
    template: `
    <div class="min-h-screen bg-gray-50">
        <!-- Loading State -->
        <div v-if="loading" class="fixed inset-0 bg-gray-50 bg-opacity-75 flex items-center justify-center z-50">
            <div class="text-center">
                <div class="loading-spinner mx-auto mb-4"></div>
                <p class="text-gray-600">Loading SIRIUS...</p>
            </div>
        </div>
        
        <!-- Main Canvas Interface -->
        <div class="flex h-screen" v-show="!loading">
            <!-- Left Sidebar - Structure Library -->
            <div class="w-80 bg-white shadow-lg border-r border-gray-200 overflow-y-auto">
                <!-- Sidebar Header -->
                <div class="p-6 border-b border-gray-200">
                    <h2 class="text-lg font-bold text-gray-900 mb-2">Structure Library</h2>
                    <p class="text-sm text-gray-600">Drag structures to the canvas</p>
                </div>
                
                <!-- Search and Filters -->
                <div class="p-4 border-b border-gray-200">
                    <div class="relative mb-4">
                        <input 
                            type="text" 
                            v-model="searchQuery"
                            placeholder="Search structures..."
                            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sirius-blue focus:border-transparent"
                        >
                        <i class="fas fa-search absolute left-3 top-3 text-gray-400"></i>
                    </div>
                    
                    <select 
                        v-model="selectedCategory"
                        class="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sirius-blue focus:border-transparent"
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
                <div class="p-4">
                    <div 
                        v-for="estrutura in filteredEstruturas" 
                        :key="estrutura.id"
                        class="structure-card"
                        draggable="true"
                        @dragstart="iniciarDrag(estrutura, $event)"
                        @click="selecionarEstrutura(estrutura)"
                        :class="{ 'ring-2 ring-sirius-blue': estruturaSelecionada?.id === estrutura.id }"
                    >
                        <div class="complexity-indicator" :class="'complexity-' + estrutura.complexidade"></div>
                        <div class="structure-type">{{ estrutura.tipo }}</div>
                        <div class="structure-name">{{ estrutura.nome }}</div>
                        <div class="structure-cost">{{ formatCurrency(estrutura.custo_base) }}</div>
                        <div class="text-xs text-gray-500 mt-2">
                            <i class="fas fa-clock mr-1"></i>{{ estrutura.tempo_implementacao }} days
                        </div>
                    </div>
                </div>
                
                <!-- Templates Section -->
                <div class="p-4 border-t border-gray-200">
                    <h3 class="text-md font-semibold text-gray-900 mb-3">Quick Templates</h3>
                    <div 
                        v-for="template in templates" 
                        :key="template.id"
                        class="template-card cursor-pointer"
                        @click="carregarTemplate(template.id)"
                    >
                        <div class="template-category">{{ template.categoria }}</div>
                        <div class="template-name">{{ template.nome }}</div>
                        <div class="template-description">{{ template.descricao }}</div>
                        <div class="template-stats">
                            <span>{{ formatCurrency(template.custo_total || 0) }}</span>
                            <span>{{ template.uso_count || 0 }} uses</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Main Canvas Area -->
            <div class="flex-1 flex flex-col">
                <!-- Canvas Toolbar -->
                <div class="bg-white border-b border-gray-200 p-4">
                    <div class="flex justify-between items-center">
                        <div class="flex items-center space-x-4">
                            <button 
                                @click="limparCanvas"
                                class="btn-secondary"
                                :disabled="elementos.length === 0"
                            >
                                <i class="fas fa-trash"></i>
                                Clear Canvas
                            </button>
                            
                            <button 
                                @click="undoAction"
                                class="btn-secondary"
                                title="Undo (Ctrl+Z)"
                            >
                                <i class="fas fa-undo"></i>
                            </button>
                            
                            <button 
                                @click="redoAction"
                                class="btn-secondary"
                                title="Redo (Ctrl+Y)"
                            >
                                <i class="fas fa-redo"></i>
                            </button>
                            
                            <button 
                                @click="toggleGridSnap"
                                class="btn-secondary"
                                :class="{ 'bg-sirius-blue text-white': snapToGrid }"
                                title="Toggle Grid Snap (G)"
                            >
                                <i class="fas fa-th"></i>
                            </button>
                            
                            <button 
                                @click="fitCanvasToContent"
                                class="btn-secondary"
                                :disabled="elementos.length === 0"
                                title="Fit to Content"
                            >
                                <i class="fas fa-expand-arrows-alt"></i>
                            </button>
                            
                            <button 
                                @click="resetCanvasView"
                                class="btn-secondary"
                                title="Reset View"
                            >
                                <i class="fas fa-home"></i>
                            </button>
                            
                            <button 
                                @click="salvarTemplate"
                                class="btn-primary"
                                :disabled="elementos.length === 0"
                            >
                                <i class="fas fa-save"></i>
                                Save Template
                            </button>
                            
                            <button 
                                @click="gerarPDF"
                                class="btn-primary"
                                :disabled="elementos.length === 0"
                            >
                                <i class="fas fa-file-pdf"></i>
                                Generate PDF
                            </button>
                        </div>
                        
                        <div class="flex items-center space-x-4">
                            <!-- Pricing Scenario Selector -->
                            <select 
                                v-model="cenarioPrecificacao"
                                class="p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-sirius-blue"
                            >
                                <option value="basico">Basic Scenario</option>
                                <option value="completo">Complete Scenario</option>
                                <option value="premium">Premium Scenario</option>
                            </select>
                            
                            <!-- Total Cost Display -->
                            <div class="bg-green-50 border border-green-200 rounded-lg px-4 py-2">
                                <div class="text-sm text-green-600 font-medium">Total Cost</div>
                                <div class="text-lg font-bold text-green-800">
                                    {{ formatCurrency(custoTotalComCenario) }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Canvas Container -->
                <div class="flex-1 relative">
                    <div 
                        ref="canvasContainer"
                        class="canvas-container w-full h-full"
                        @dragover="permitirDrop"
                        @drop="handleDrop"
                    >
                        <!-- Canvas Elements -->
                        <div class="relative w-full h-full p-8">
                            <div 
                                v-for="elemento in elementos" 
                                :key="elemento.id"
                                class="absolute bg-white rounded-lg shadow-lg border-2 border-gray-200 p-4 cursor-move"
                                :style="{ 
                                    left: elemento.position.x + 'px', 
                                    top: elemento.position.y + 'px',
                                    width: '200px'
                                }"
                                @mousedown="iniciarArrastar(elemento, $event)"
                                @click="selecionarElemento(elemento)"
                                :class="{ 'border-sirius-blue': elementoSelecionado?.id === elemento.id }"
                            >
                                <div class="text-sm font-semibold text-gray-900">{{ elemento.estrutura.nome }}</div>
                                <div class="text-xs text-gray-500 mt-1">{{ elemento.estrutura.tipo }}</div>
                                <div class="text-sm font-bold text-green-600 mt-2">
                                    {{ formatCurrency(elemento.estrutura.custo_base) }}
                                </div>
                                <button 
                                    @click.stop="removerElemento(elemento.id)"
                                    class="absolute top-2 right-2 text-red-500 hover:text-red-700"
                                >
                                    <i class="fas fa-times text-xs"></i>
                                </button>
                            </div>
                        </div>
                        
                        <!-- Empty State -->
                        <div v-if="elementos.length === 0" class="absolute inset-0 flex items-center justify-center">
                            <div class="text-center">
                                <i class="fas fa-network-wired text-6xl text-gray-300 mb-4"></i>
                                <h3 class="text-xl font-semibold text-gray-500 mb-2">Start Building Your Structure</h3>
                                <p class="text-gray-400">Drag legal structures from the sidebar to begin</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Right Sidebar - Information Panel -->
            <div class="w-96 bg-white shadow-lg border-l border-gray-200 overflow-y-auto">
                <!-- Structure Information -->
                <div v-if="estruturaSelecionada" class="p-6">
                    <div class="info-panel">
                        <h3>
                            <i class="fas fa-info-circle text-sirius-blue"></i>
                            Structure Details
                        </h3>
                        
                        <div class="space-y-4">
                            <div>
                                <h4 class="font-semibold text-gray-900 mb-2">{{ estruturaSelecionada.nome }}</h4>
                                <p class="text-sm text-gray-600">{{ estruturaSelecionada.descricao }}</p>
                            </div>
                            
                            <div class="metric">
                                <span class="metric-label">Base Cost</span>
                                <span class="metric-value">{{ formatCurrency(estruturaSelecionada.custo_base) }}</span>
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
                                <span class="metric-value">{{ estruturaSelecionada.complexidade }}/5</span>
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
                    
                    <!-- Tax Information -->
                    <div class="info-panel mt-6">
                        <h3>
                            <i class="fas fa-calculator text-sirius-blue"></i>
                            Tax Implications
                        </h3>
                        
                        <div class="space-y-4">
                            <div>
                                <h4 class="font-semibold text-gray-900 mb-2">United States</h4>
                                <p class="text-sm text-gray-600">{{ estruturaSelecionada.impacto_tributario_eua }}</p>
                            </div>
                            
                            <div>
                                <h4 class="font-semibold text-gray-900 mb-2">Brazil</h4>
                                <p class="text-sm text-gray-600">{{ estruturaSelecionada.impacto_tributario_brasil }}</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Privacy Information -->
                    <div class="info-panel mt-6">
                        <h3>
                            <i class="fas fa-shield-alt text-sirius-blue"></i>
                            Privacy & Protection
                        </h3>
                        
                        <p class="text-sm text-gray-600">{{ estruturaSelecionada.impacto_privacidade }}</p>
                    </div>
                </div>
                
                <!-- Configuration Summary -->
                <div v-if="elementos.length > 0" class="p-6 border-t border-gray-200">
                    <div class="info-panel">
                        <h3>
                            <i class="fas fa-chart-line text-sirius-blue"></i>
                            Configuration Summary
                        </h3>
                        
                        <div class="metric">
                            <span class="metric-label">Total Structures</span>
                            <span class="metric-value">{{ elementos.length }}</span>
                        </div>
                        
                        <div class="metric">
                            <span class="metric-label">Base Cost</span>
                            <span class="metric-value">{{ formatCurrency(custoTotal) }}</span>
                        </div>
                        
                        <div class="metric">
                            <span class="metric-label">Total Cost</span>
                            <span class="metric-value">{{ formatCurrency(custoTotalComCenario) }}</span>
                        </div>
                        
                        <div class="metric">
                            <span class="metric-label">Max Implementation Time</span>
                            <span class="metric-value">{{ tempoTotal }} days</span>
                        </div>
                    </div>
                </div>
                
                <!-- Validation Results -->
                <div v-if="validacao.erros.length > 0 || validacao.alertas.length > 0 || validacao.sugestoes.length > 0" 
                     class="p-6 border-t border-gray-200">
                    <h3 class="text-lg font-semibold text-gray-900 mb-4">
                        <i class="fas fa-exclamation-triangle text-yellow-500"></i>
                        Validation Results
                    </h3>
                    
                    <!-- Errors -->
                    <div v-for="erro in validacao.erros" :key="erro.mensagem" class="validation-alert error">
                        <i class="fas fa-times-circle alert-icon"></i>
                        {{ erro.mensagem }}
                    </div>
                    
                    <!-- Warnings -->
                    <div v-for="alerta in validacao.alertas" :key="alerta.mensagem" class="validation-alert warning">
                        <i class="fas fa-exclamation-triangle alert-icon"></i>
                        {{ alerta.mensagem }}
                    </div>
                    
                    <!-- Suggestions -->
                    <div v-for="sugestao in validacao.sugestoes" :key="sugestao.mensagem" class="validation-alert info">
                        <i class="fas fa-lightbulb alert-icon"></i>
                        {{ sugestao.mensagem }}
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
            
            // Drag and drop state
            draggedElement: null,
            isDragging: false,
            dragOffset: { x: 0, y: 0 },
            
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
            if (this.cenarioPrecificacao === 'completo') multiplicador = 1.5;
            if (this.cenarioPrecificacao === 'premium') multiplicador = 2.2;
            return this.custoTotal * multiplicador;
        }
    },
    
    mounted() {
        this.initializeApp();
        
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
        
        // Drag and Drop Methods
        iniciarDrag(estrutura, event) {
            event.dataTransfer.setData('estrutura', JSON.stringify(estrutura));
            event.dataTransfer.effectAllowed = 'copy';
            
            // Visual feedback
            event.target.style.opacity = '0.5';
            setTimeout(() => {
                if (event.target) event.target.style.opacity = '1';
            }, 100);
        },
        
        permitirDrop(event) {
            event.preventDefault();
            event.dataTransfer.dropEffect = 'copy';
        },
        
        async handleDrop(event) {
            event.preventDefault();
            
            try {
                const estruturaData = JSON.parse(event.dataTransfer.getData('estrutura'));
                
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
                this.calcularTotais();
                await this.validarConfiguracao();
                
                this.showNotification(`Added ${estruturaData.nome} to canvas`, 'success');
            } catch (error) {
                console.error('Error handling drop:', error);
                this.showNotification('Failed to add structure to canvas', 'error');
            }
        },
        
        // Element Management
        selecionarEstrutura(estrutura) {
            this.estruturaSelecionada = estrutura;
        },
        
        selecionarElemento(elemento) {
            this.elementoSelecionado = elemento;
            this.estruturaSelecionada = elemento.estrutura;
        },
        
        removerElemento(elementoId) {
            const index = this.elementos.findIndex(el => el.id === elementoId);
            if (index !== -1) {
                const elemento = this.elementos[index];
                this.elementos.splice(index, 1);
                this.calcularTotais();
                this.validarConfiguracao();
                
                if (this.elementoSelecionado?.id === elementoId) {
                    this.elementoSelecionado = null;
                }
                
                this.showNotification(`Removed ${elemento.estrutura.nome}`, 'info');
            }
        },
        
        // Dragging for canvas elements
        iniciarArrastar(elemento, event) {
            this.draggedElement = elemento;
            this.isDragging = true;
            
            const rect = event.target.getBoundingClientRect();
            this.dragOffset = {
                x: event.clientX - rect.left,
                y: event.clientY - rect.top
            };
            
            event.preventDefault();
        },
        
        handleMouseMove(event) {
            if (this.isDragging && this.draggedElement) {
                const canvasRect = this.$refs.canvasContainer.getBoundingClientRect();
                const x = event.clientX - canvasRect.left - this.dragOffset.x;
                const y = event.clientY - canvasRect.top - this.dragOffset.y;
                
                this.draggedElement.position = {
                    x: Math.max(0, Math.min(x, canvasRect.width - 200)),
                    y: Math.max(0, Math.min(y, canvasRect.height - 100))
                };
            }
        },
        
        handleMouseUp() {
            this.isDragging = false;
            this.draggedElement = null;
        },
        
        // Calculations
        async calcularTotais() {
            if (this.elementos.length === 0) {
                this.custoTotal = 0;
                this.tempoTotal = 0;
                this.validacao = {
                    valido: true,
                    erros: [],
                    alertas: [],
                    sugestoes: []
                };
                return;
            }
            
            try {
                // Calculate advanced costs
                const costResponse = await fetch('/api/calcular-custos/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': window.csrfToken
                    },
                    body: JSON.stringify({
                        elementos: this.elementos,
                        cenario: this.cenarioSelecionado,
                        incluir_analise_risco: true
                    })
                });
                
                if (costResponse.ok) {
                    const costData = await costResponse.json();
                    this.custoTotal = costData.risk_adjusted_cost || 0;
                    this.tempoTotal = costData.time_to_implementation || 0;
                    this.analiseDetalhada = costData;
                    
                    // Perform advanced validation
                    const validationResponse = await fetch('/api/validar-configuracao/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': window.csrfToken
                        },
                        body: JSON.stringify({
                            elementos: this.elementos,
                            analise_custos: costData
                        })
                    });
                    
                    if (validationResponse.ok) {
                        const validationData = await validationResponse.json();
                        this.validacao = {
                            valido: validationData.is_valid,
                            erros: validationData.results.filter(r => r.level === 'error').map(r => r.message),
                            alertas: validationData.results.filter(r => r.level === 'warning').map(r => r.message),
                            sugestoes: validationData.results.filter(r => r.level === 'info').map(r => r.message),
                            detalhes: validationData
                        };
                    }
                } else {
                    // Fallback to simple calculation
                    this.calcularTotaisSimples();
                }
                
            } catch (error) {
                console.error('Error calculating costs:', error);
                // Fallback to simple calculation
                this.calcularTotaisSimples();
            }
        },
        
        calcularTotaisSimples() {
            // Simple fallback calculation
            let custoTotal = 0;
            let tempoMaximo = 0;
            
            this.elementos.forEach(elemento => {
                const estrutura = elemento.estrutura;
                let custo = estrutura.custo_base;
                
                // Apply scenario multiplier
                const multiplicador = this.cenarioMultiplicadores[this.cenarioSelecionado] || 1;
                custo *= multiplicador;
                
                custoTotal += custo;
                tempoMaximo = Math.max(tempoMaximo, estrutura.tempo_implementacao);
            });
            
            this.custoTotal = custoTotal;
            this.tempoTotal = tempoMaximo;
        },
        
        // Validation
        async validarConfiguracao() {
            if (this.elementos.length === 0) {
                this.validacao = {
                    valido: true,
                    erros: [],
                    alertas: [],
                    sugestoes: []
                };
                return;
            }
            
            try {
                const response = await fetch(window.djangoData.apiUrls.validar, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': window.djangoData.csrfToken
                    },
                    body: JSON.stringify({
                        configuracao: {
                            elementos: this.elementos.map(el => ({
                                estrutura_id: el.estrutura_id,
                                position: el.position
                            }))
                        }
                    })
                });
                
                if (!response.ok) {
                    throw new Error('Validation request failed');
                }
                
                this.validacao = await response.json();
            } catch (error) {
                console.error('Error validating configuration:', error);
                this.showNotification('Validation failed', 'error');
            }
        },
        
        // Template Management
        async salvarTemplate() {
            const nome = prompt('Template name:');
            if (!nome) return;
            
            const categoria = prompt('Category (TECH/REAL_ESTATE/TRADING/FAMILY_OFFICE/GENERAL):') || 'GENERAL';
            const descricao = prompt('Description (optional):') || '';
            
            try {
                const response = await fetch(window.djangoData.apiUrls.salvarTemplate, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': window.djangoData.csrfToken
                    },
                    body: JSON.stringify({
                        nome,
                        categoria,
                        descricao,
                        configuracao: {
                            elementos: this.elementos,
                            conexoes: this.conexoes
                        }
                    })
                });
                
                if (!response.ok) {
                    throw new Error('Failed to save template');
                }
                
                const result = await response.json();
                this.showNotification('Template saved successfully!', 'success');
                
                // Reload templates
                await this.carregarDados();
            } catch (error) {
                console.error('Error saving template:', error);
                this.showNotification('Failed to save template', 'error');
            }
        },
        
        async carregarTemplate(templateId) {
            try {
                const response = await fetch(`/api/template/${templateId}/`);
                
                if (!response.ok) {
                    throw new Error('Failed to load template');
                }
                
                const template = await response.json();
                
                this.elementos = template.configuracao.elementos || [];
                this.conexoes = template.configuracao.conexoes || [];
                
                // Ensure all elements have the full structure data
                for (let elemento of this.elementos) {
                    const estrutura = this.estruturas.find(e => e.id === elemento.estrutura_id);
                    if (estrutura) {
                        elemento.estrutura = estrutura;
                    }
                }
                
                this.calcularTotais();
                await this.validarConfiguracao();
                
                this.showNotification(`Loaded template: ${template.nome}`, 'success');
            } catch (error) {
                console.error('Error loading template:', error);
                this.showNotification('Failed to load template', 'error');
            }
        },
        
        // PDF Generation
        async gerarPDF() {
            try {
                this.loading = true;
                
                // Capture canvas
                const canvas = await html2canvas(this.$refs.canvasContainer, {
                    backgroundColor: '#ffffff',
                    scale: 2
                });
                
                // Create PDF
                const { jsPDF } = window.jspdf;
                const pdf = new jsPDF('l', 'mm', 'a4'); // landscape
                
                // Add title
                pdf.setFontSize(20);
                pdf.text('SIRIUS - Legal Structure Configuration', 20, 20);
                
                // Add canvas image
                const imgData = canvas.toDataURL('image/png');
                const imgWidth = 250;
                const imgHeight = (canvas.height * imgWidth) / canvas.width;
                pdf.addImage(imgData, 'PNG', 20, 30, imgWidth, Math.min(imgHeight, 140));
                
                // Add configuration details
                let yPosition = Math.max(180, 30 + imgHeight + 10);
                
                pdf.setFontSize(14);
                pdf.text(`Total Cost (${this.cenarioPrecificacao}): ${this.formatCurrency(this.custoTotalComCenario)}`, 20, yPosition);
                pdf.text(`Implementation Time: ${this.tempoTotal} days`, 20, yPosition + 10);
                pdf.text(`Number of Structures: ${this.elementos.length}`, 20, yPosition + 20);
                
                // Add structure list
                pdf.setFontSize(12);
                pdf.text('Included Structures:', 20, yPosition + 35);
                
                let listY = yPosition + 45;
                this.elementos.forEach((elemento, index) => {
                    if (listY > 280) { // New page if needed
                        pdf.addPage();
                        listY = 20;
                    }
                    pdf.text(`• ${elemento.estrutura.nome} - ${this.formatCurrency(elemento.estrutura.custo_base)}`, 25, listY);
                    listY += 8;
                });
                
                // Save PDF
                pdf.save(`sirius_configuration_${Date.now()}.pdf`);
                
                this.showNotification('PDF generated successfully!', 'success');
            } catch (error) {
                console.error('Error generating PDF:', error);
                this.showNotification('Failed to generate PDF', 'error');
            } finally {
                this.loading = false;
            }
        },
        
        // Canvas Management
        limparCanvas() {
            if (this.elementos.length === 0) return;
            
            if (confirm('Are you sure you want to clear the canvas?')) {
                this.elementos = [];
                this.conexoes = [];
                this.elementoSelecionado = null;
                this.estruturaSelecionada = null;
                this.calcularTotais();
                this.validacao = {
                    valido: true,
                    erros: [],
                    alertas: [],
                    sugestoes: []
                };
                
                if (this.advancedCanvas) {
                    this.advancedCanvas.saveState();
                }
                
                this.showNotification('Canvas cleared', 'info');
            }
        },
        
        // Advanced Canvas Controls
        resetCanvasView() {
            if (this.advancedCanvas) {
                this.advancedCanvas.resetView();
            }
        },
        
        fitCanvasToContent() {
            if (this.advancedCanvas) {
                this.advancedCanvas.fitToContent();
            }
        },
        
        toggleGridSnap() {
            this.snapToGrid = !this.snapToGrid;
            if (this.advancedCanvas) {
                this.advancedCanvas.snapToGrid = this.snapToGrid;
            }
            this.showNotification(
                `Grid snap ${this.snapToGrid ? 'enabled' : 'disabled'}`,
                'info'
            );
        },
        
        undoAction() {
            if (this.advancedCanvas) {
                this.advancedCanvas.undo();
            }
        },
        
        redoAction() {
            if (this.advancedCanvas) {
                this.advancedCanvas.redo();
            }
        },
        
        createConnection(fromElement, toElement, type = 'default') {
            if (this.advancedCanvas) {
                return this.advancedCanvas.createConnection(fromElement, toElement, type);
            }
        },
        
        removeConnection(connectionId) {
            if (this.advancedCanvas) {
                this.advancedCanvas.removeConnection(connectionId);
            }
        },
        
        // Event Handlers
        handleKeydown(event) {
            // Keyboard shortcuts
            if (event.ctrlKey || event.metaKey) {
                switch (event.key) {
                    case 's':
                        event.preventDefault();
                        if (this.elementos.length > 0) {
                            this.salvarTemplate();
                        }
                        break;
                    case 'p':
                        event.preventDefault();
                        if (this.elementos.length > 0) {
                            this.gerarPDF();
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
        
        handleResize() {
            // Handle window resize if needed
            this.$nextTick(() => {
                // Recalculate canvas dimensions if necessary
            });
        },
        
        // Utility Methods
        formatCurrency(amount) {
            return new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD'
            }).format(amount || 0);
        },
        
        showNotification(message, type = 'info') {
            // Use global notification system
            if (window.SiriusUtils && window.SiriusUtils.showNotification) {
                window.SiriusUtils.showNotification(message, type);
            } else {
                // Fallback
                console.log(`[${type.toUpperCase()}] ${message}`);
            }
        }
    },
    
    // Watchers
    watch: {
        cenarioPrecificacao() {
            // Recalculate when pricing scenario changes
            this.$nextTick(() => {
                // Any additional calculations needed
            });
        },
        
        elementos: {
            handler() {
                // Auto-validate when elements change
                this.$nextTick(() => {
                    this.validarConfiguracao();
                });
            },
            deep: true
        }
    },
    
    // Cleanup
    beforeUnmount() {
        document.removeEventListener('keydown', this.handleKeydown);
        window.removeEventListener('resize', this.handleResize);
        document.removeEventListener('mousemove', this.handleMouseMove);
        document.removeEventListener('mouseup', this.handleMouseUp);
        
        // Cleanup advanced canvas
        if (this.advancedCanvas) {
            this.advancedCanvas.destroy();
        }
    }
};

// Mount the Vue app
createApp(SiriusApp).mount('#app');

