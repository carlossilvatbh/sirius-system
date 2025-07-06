import { createApp } from 'vue'
import { createPinia } from 'pinia'
import SiriusApp from './SiriusApp.vue'
import './styles/sirius.css'

// Font Awesome (temporary via CDN)
const fontAwesome = document.createElement('link')
fontAwesome.rel = 'stylesheet'
fontAwesome.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
document.head.appendChild(fontAwesome)

// Create Vue app
const app = createApp(SiriusApp)

// Create Pinia store
const pinia = createPinia()
app.use(pinia)

// Mount app
app.mount('#app')

console.log('🚀 SIRIUS Canvas v2.0 - Initialized successfully!')

