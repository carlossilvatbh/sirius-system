// SIRIUS Main Application - Vue.js 3
const { createApp } = Vue;

createApp({
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
            loading: false,
            vueFlowAvailable: false,
            
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
            tempoTotal: 0
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
                    estrutura.tipo_display.toLowerCase().includes(query)
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
    },
    
    methods: {
        async initializeApp() {
            this.loading = true;
            try {
                await this.carregarDados();
                this.configurarEventListeners();
                this.checkVueFlowAvailability();
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
                    fetch('/api/estruturas/'),
                    fetch('/api/templates/')
                ]);
                
                if (!estruturasRes.ok || !templatesRes.ok) {
                    throw new Error('Failed to fetch data');
                }
                
                this.estruturas = await estruturasRes.json();
                this.templates = await templatesRes.json();
                
                console.log('Loaded', this.estruturas.length, 'structures and', this.templates.length, 'templates');
            } catch (error) {
                console.error('Error loading data:', error);
                throw error;
            }
        },
        
        configurarEventListeners() {
            // Global event listeners
            document.addEventListener('keydown', this.handleKeydown);
            window.addEventListener('resize', this.handleResize);
            
            // Mouse events for dragging (fallback when Vue Flow is not available)
            document.addEventListener('mousemove', this.handleMouseMove);
            document.addEventListener('mouseup', this.handleMouseUp);
        },
        
        checkVueFlowAvailability() {
            // Check if Vue Flow is available
            this.vueFlowAvailable = typeof VueFlow !== 'undefined';
            if (this.vueFlowAvailable) {
                this.initializeVueFlow();
            }
        },
        
        initializeVueFlow() {
            // Initialize Vue Flow if available
            // This would be implemented when Vue Flow is properly loaded
            console.log('Vue Flow would be initialized here');
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
        
        // Dragging for fallback mode
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
        calcularTotais() {
            this.custoTotal = this.elementos.reduce((total, el) => 
                total + parseFloat(el.estrutura.custo_base), 0);
            
            this.tempoTotal = this.elementos.length > 0 ? 
                Math.max(...this.elementos.map(el => 
                    parseInt(el.estrutura.tempo_implementacao))) : 0;
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
                const response = await fetch('/api/validar/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': window.csrfToken || ''
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
                const response = await fetch('/api/salvar-template/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': window.csrfToken || ''
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
                
                this.showNotification('Canvas cleared', 'info');
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
            }).format(amount);
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
    }
}).mount('#app');

