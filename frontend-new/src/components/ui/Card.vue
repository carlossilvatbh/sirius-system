<template>
  <div :class="cardClasses" @click="handleClick">
    <div v-if="$slots.header" class="card-header">
      <slot name="header"></slot>
    </div>
    
    <div class="card-content">
      <slot></slot>
    </div>
    
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  variant?: 'default' | 'elevated' | 'outlined' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  clickable?: boolean;
  selected?: boolean;
  disabled?: boolean;
}

interface Emits {
  (e: 'click', event: MouseEvent): void;
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  size: 'md',
  clickable: false,
  selected: false,
  disabled: false,
});

const emit = defineEmits<Emits>();

const cardClasses = computed(() => {
  const baseClasses = [
    'rounded-lg',
    'transition-all',
    'duration-200',
  ];

  // Variant classes
  const variantClasses = {
    default: ['bg-white', 'border', 'border-gray-200'],
    elevated: ['bg-white', 'shadow-md', 'hover:shadow-lg'],
    outlined: ['bg-white', 'border-2', 'border-gray-300'],
    ghost: ['bg-transparent'],
  };

  // Size classes
  const sizeClasses = {
    sm: ['p-3'],
    md: ['p-4'],
    lg: ['p-6'],
  };

  // Interactive classes
  const interactiveClasses = [];
  if (props.clickable && !props.disabled) {
    interactiveClasses.push(
      'cursor-pointer',
      'hover:shadow-md',
      'hover:-translate-y-0.5',
      'active:translate-y-0'
    );
  }

  // State classes
  const stateClasses = [];
  if (props.selected) {
    stateClasses.push(
      'ring-2',
      'ring-sirius-500',
      'border-sirius-500'
    );
  }

  if (props.disabled) {
    stateClasses.push(
      'opacity-50',
      'cursor-not-allowed'
    );
  }

  return [
    ...baseClasses,
    ...variantClasses[props.variant],
    ...sizeClasses[props.size],
    ...interactiveClasses,
    ...stateClasses,
  ];
});

const handleClick = (event: MouseEvent) => {
  if (props.clickable && !props.disabled) {
    emit('click', event);
  }
};
</script>

<style scoped>
.card-header {
  @apply border-b border-gray-200 pb-3 mb-4;
}

.card-content {
  @apply flex-1;
}

.card-footer {
  @apply border-t border-gray-200 pt-3 mt-4;
}

/* Focus styles for accessibility */
.cursor-pointer:focus {
  @apply outline-none ring-2 ring-sirius-500 ring-offset-2;
}
</style>

