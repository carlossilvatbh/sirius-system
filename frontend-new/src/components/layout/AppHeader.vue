<template>
  <header class="app-header">
    <div class="header-content">
      <div class="header-left">
        <button
          @click="toggleSidebar"
          class="sidebar-toggle"
        >
          ☰
        </button>
        <div class="logo">
          <h1 class="logo-text">Sirius</h1>
        </div>
      </div>
      
      <div class="header-center">
        <h2 class="page-title">Legal Structure Configuration</h2>
      </div>
      
      <div class="header-right">
        <Button variant="outline" size="sm">
          Save Configuration
        </Button>
        <Button variant="primary" size="sm">
          Generate PDF
        </Button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useSiriusStore } from '@/stores';
import Button from '@/components/ui/Button.vue';

const store = useSiriusStore();

const toggleSidebar = () => {
  store.toggleSidebar();
};
</script>

<style scoped>
.app-header {
  @apply bg-white border-b border-gray-200 px-4 py-3;
}

.header-content {
  @apply flex items-center justify-between;
}

.header-left {
  @apply flex items-center gap-4;
}

.sidebar-toggle {
  @apply p-2 rounded-lg hover:bg-gray-100 transition-colors;
}

.logo-text {
  @apply text-xl font-bold text-sirius-600;
}

.page-title {
  @apply text-lg font-medium text-gray-700;
}

.header-right {
  @apply flex items-center gap-2;
}
</style>

