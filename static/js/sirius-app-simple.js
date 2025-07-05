// SIRIUS Vue.js Application - Simplified Version
console.log('SIRIUS Debug: JavaScript file loaded');

// Check if Vue is available
if (typeof Vue === 'undefined') {
    console.error('SIRIUS Error: Vue.js is not loaded');
    alert('Vue.js is not loaded. Please check your internet connection.');
} else {
    console.log('SIRIUS Debug: Vue.js is available');
}

// Check if window.djangoData is available
if (typeof window.djangoData === 'undefined') {
    console.error('SIRIUS Error: window.djangoData is not defined');
    alert('Django data not available. Please refresh the page.');
} else {
    console.log('SIRIUS Debug: window.djangoData is available', window.djangoData);
}

const { createApp } = Vue;

const SiriusApp = {
    data() {
        return {
            // Basic data
            estruturas: [],
            templates: [],
            elementos: [],
            loading: true,
            
            // Search and filters
            searchQuery: '',
            selectedCategory: '',
            
            // UI state
            estruturaSelecionada: null,
            
            // Pricing
            cenarioPrecificacao: 'basico',
            custoTotal: 0,
            
            // Mobile
            isMobile: false,
            mobileSidebarOpen: false,
            showMobileDetails: false,
            
            // Notifications
            notifications: [],
            notificationId: 0,
            
            // Validation
            validacao: {
                valido: true,
                erros: [],
                alertas: [],
                sugestoes: []
            }
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
        
        custoTotalSetup() {
            return this.elementos.reduce((total, elemento) => 
                total + parseFloat(elemento.estrutura.custo_base || 0), 0
            );
        }
    },
    
    async mounted() {
        console.log('SIRIUS Debug: Vue mounted() called');
        this.checkMobile();
        await this.loadData();
        this.loading = false;
    },
    
    methods: {
        async loadData() {
            console.log('SIRIUS Debug: Loading data...');
            try {
                const response = await fetch(window.djangoData.apiUrls.estruturas);
                if (response.ok) {
                    this.estruturas = await response.json();
                    console.log('SIRIUS Debug: Loaded', this.estruturas.length, 'structures');
                } else {
                    console.error('Failed to load structures:', response.status);
                }
            } catch (error) {
                console.error('Error loading structures:', error);
            }
        },
        
        checkMobile() {
            this.isMobile = window.innerWidth < 768;
            window.addEventListener('resize', () => {
                this.isMobile = window.innerWidth < 768;
            });
        },
        
        formatCurrency(value) {
            return new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD'
            }).format(value);
        },
        
        selecionarEstrutura(estrutura) {
            this.estruturaSelecionada = estrutura;
            if (this.isMobile) {
                this.showMobileDetails = true;
            }
        },
        
        iniciarDrag(estrutura, event) {
            console.log('SIRIUS Debug: Drag started for', estrutura.nome);
            if (event.dataTransfer) {
                event.dataTransfer.setData('estrutura', JSON.stringify(estrutura));
                event.dataTransfer.effectAllowed = 'copy';
            }
        },
        
        permitirDrop(event) {
            event.preventDefault();
            event.dataTransfer.dropEffect = 'copy';
        },
        
        handleDrop(event) {
            console.log('SIRIUS Debug: Drop event triggered');
            event.preventDefault();
            
            try {
                const estruturaData = JSON.parse(event.dataTransfer.getData('estrutura'));
                console.log('SIRIUS Debug: Dropped structure:', estruturaData.nome);
                
                // Calculate position
                const canvasRect = this.$refs.canvasContainer.getBoundingClientRect();
                const x = event.clientX - canvasRect.left;
                const y = event.clientY - canvasRect.top;
                
                // Create new element
                const novoElemento = {
                    id: `estrutura_${Date.now()}`,
                    estrutura_id: estruturaData.id,
                    estrutura: estruturaData,
                    position: { x: Math.max(0, x - 100), y: Math.max(0, y - 50) },
                    type: 'estrutura'
                };
                
                this.elementos.push(novoElemento);
                console.log('SIRIUS Debug: Added element to canvas');
                
            } catch (error) {
                console.error('Error handling drop:', error);
            }
        },
        
        showNotification(message, type = 'info') {
            const notification = {
                id: ++this.notificationId,
                message,
                type,
                timestamp: Date.now()
            };
            
            this.notifications.push(notification);
            
            // Auto remove after 5 seconds
            setTimeout(() => {
                this.removeNotification(notification.id);
            }, 5000);
        },
        
        removeNotification(notificationId) {
            this.notifications = this.notifications.filter(n => n.id !== notificationId);
        },
        
        // Placeholder methods
        gerarPDF() {
            this.showNotification('PDF generation coming soon', 'info');
        },
        
        salvarConfiguracao() {
            this.showNotification('Save configuration coming soon', 'info');
        }
    },
    
    template: `
        <div class="flex h-screen bg-gray-100">
            <!-- Loading -->
            <div v-if="loading" class="fixed inset-0 bg-white bg-opacity-80 flex items-center justify-center z-50">
                <div class="text-center">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p class="text-gray-600">Loading SIRIUS...</p>
                </div>
            </div>
            
            <!-- Left Sidebar -->
            <div class="w-80 bg-white shadow-lg border-r border-gray-200 overflow-hidden">
                <div class="p-4 border-b border-gray-200">
                    <h2 class="text-xl font-bold text-gray-800 mb-2">
                        <i class="fas fa-layer-group mr-2"></i>
                        Structure Library
                    </h2>
                    <p class="text-sm text-gray-600">Drag structures to the canvas</p>
                </div>
                
                <!-- Search -->
                <div class="p-4 border-b border-gray-200">
                    <input 
                        type="text" 
                        v-model="searchQuery"
                        placeholder="Search structures..."
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                </div>
                
                <!-- Structure List -->
                <div class="overflow-y-auto flex-1 p-4">
                    <div 
                        v-for="estrutura in filteredEstruturas" 
                        :key="estrutura.id"
                        class="bg-white border border-gray-200 rounded-lg p-4 mb-3 cursor-move hover:shadow-md transition-shadow"
                        draggable="true"
                        @dragstart="iniciarDrag(estrutura, $event)"
                        @click="selecionarEstrutura(estrutura)"
                    >
                        <div class="font-semibold text-gray-800 mb-1">{{ estrutura.nome }}</div>
                        <div class="text-sm text-gray-600 mb-2">{{ estrutura.tipo }}</div>
                        <div class="text-sm font-bold text-green-600">{{ formatCurrency(estrutura.custo_base) }}</div>
                    </div>
                </div>
            </div>
            
            <!-- Main Canvas Area -->
            <div class="flex-1 flex flex-col">
                <!-- Toolbar -->
                <div class="bg-white border-b border-gray-200 p-4 flex justify-between items-center">
                    <div class="flex items-center space-x-4">
                        <button 
                            @click="gerarPDF"
                            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                        >
                            <i class="fas fa-file-pdf mr-2"></i>
                            Generate PDF
                        </button>
                        <button 
                            @click="salvarConfiguracao"
                            class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
                        >
                            <i class="fas fa-save mr-2"></i>
                            Save Configuration
                        </button>
                    </div>
                    
                    <div class="text-lg font-bold text-gray-800">
                        Total: {{ formatCurrency(custoTotalSetup) }}
                    </div>
                </div>
                
                <!-- Canvas -->
                <div class="flex-1 relative">
                    <div 
                        ref="canvasContainer"
                        class="w-full h-full bg-gray-50 relative overflow-hidden"
                        @dragover="permitirDrop"
                        @drop="handleDrop"
                    >
                        <!-- Canvas Elements -->
                        <div 
                            v-for="elemento in elementos" 
                            :key="elemento.id"
                            class="absolute bg-white border border-gray-300 rounded-lg p-4 shadow-md cursor-move min-w-48"
                            :style="{ left: elemento.position.x + 'px', top: elemento.position.y + 'px' }"
                        >
                            <div class="font-semibold text-gray-800 mb-1">{{ elemento.estrutura.nome }}</div>
                            <div class="text-sm text-gray-600 mb-2">{{ elemento.estrutura.tipo }}</div>
                            <div class="text-sm font-bold text-green-600">{{ formatCurrency(elemento.estrutura.custo_base) }}</div>
                        </div>
                        
                        <!-- Drop Zone Message -->
                        <div v-if="elementos.length === 0" class="absolute inset-0 flex items-center justify-center">
                            <div class="text-center text-gray-500">
                                <i class="fas fa-mouse-pointer text-4xl mb-4"></i>
                                <p class="text-lg">Drag structures from the sidebar to start building</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Structure Details Panel -->
            <div v-if="estruturaSelecionada && !isMobile" class="w-80 bg-white border-l border-gray-200 p-4 overflow-y-auto">
                <h3 class="text-lg font-bold mb-4">{{ estruturaSelecionada.nome }}</h3>
                <p class="text-sm text-gray-600 mb-4">{{ estruturaSelecionada.descricao }}</p>
                
                <div class="space-y-3">
                    <div class="flex justify-between">
                        <span class="text-sm text-gray-500">Base Cost:</span>
                        <span class="font-semibold text-green-600">{{ formatCurrency(estruturaSelecionada.custo_base) }}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-sm text-gray-500">Implementation:</span>
                        <span class="font-semibold">{{ estruturaSelecionada.tempo_implementacao }} days</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-sm text-gray-500">Complexity:</span>
                        <span class="font-semibold">{{ estruturaSelecionada.complexidade }}/5</span>
                    </div>
                </div>
            </div>
            
            <!-- Notifications -->
            <div class="fixed top-4 right-4 z-50 space-y-2">
                <div 
                    v-for="notification in notifications" 
                    :key="notification.id"
                    class="bg-white border border-gray-200 rounded-lg p-4 shadow-lg min-w-64"
                    :class="{
                        'border-blue-500': notification.type === 'info',
                        'border-green-500': notification.type === 'success',
                        'border-red-500': notification.type === 'error'
                    }"
                >
                    <div class="flex items-center justify-between">
                        <span class="text-sm">{{ notification.message }}</span>
                        <button @click="removeNotification(notification.id)" class="text-gray-400 hover:text-gray-600">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `
};

console.log('SIRIUS Debug: About to mount Vue app');
try {
    createApp(SiriusApp).mount('#sirius-app');
    console.log('SIRIUS Debug: Vue app mounted successfully');
} catch (error) {
    console.error('SIRIUS Error: Failed to mount Vue app:', error);
    alert('Failed to initialize the application. Please check the console for details.');
}
