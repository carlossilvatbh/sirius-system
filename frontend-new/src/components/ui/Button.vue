<template>
  <button
    :class="buttonClasses"
    :disabled="disabled || loading"
    :type="type"
    @click="handleClick"
  >
    <span v-if="loading" class="loading-spinner"></span>
    <slot v-if="!loading" name="icon"></slot>
    <span v-if="!loading || showTextWhileLoading" class="button-text">
      <slot></slot>
    </span>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  showTextWhileLoading?: boolean;
  type?: 'button' | 'submit' | 'reset';
  fullWidth?: boolean;
}

interface Emits {
  (e: 'click', event: MouseEvent): void;
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  disabled: false,
  loading: false,
  showTextWhileLoading: false,
  type: 'button',
  fullWidth: false,
});

const emit = defineEmits<Emits>();

const buttonClasses = computed(() => {
  const baseClasses = [
    'inline-flex',
    'items-center',
    'justify-center',
    'gap-2',
    'font-medium',
    'rounded-lg',
    'transition-all',
    'duration-200',
    'focus:outline-none',
    'focus:ring-2',
    'focus:ring-offset-2',
    'disabled:opacity-50',
    'disabled:cursor-not-allowed',
  ];

  // Size classes
  const sizeClasses = {
    sm: ['px-3', 'py-1.5', 'text-sm'],
    md: ['px-4', 'py-2', 'text-sm'],
    lg: ['px-6', 'py-3', 'text-base'],
  };

  // Variant classes
  const variantClasses = {
    primary: [
      'bg-sirius-500',
      'text-white',
      'hover:bg-sirius-600',
      'focus:ring-sirius-500',
      'shadow-sm',
      'hover:shadow-md',
    ],
    secondary: [
      'bg-gray-100',
      'text-gray-700',
      'hover:bg-gray-200',
      'focus:ring-gray-500',
      'border',
      'border-gray-300',
    ],
    outline: [
      'bg-transparent',
      'text-sirius-600',
      'border',
      'border-sirius-300',
      'hover:bg-sirius-50',
      'focus:ring-sirius-500',
    ],
    ghost: [
      'bg-transparent',
      'text-gray-600',
      'hover:bg-gray-100',
      'focus:ring-gray-500',
    ],
    danger: [
      'bg-red-500',
      'text-white',
      'hover:bg-red-600',
      'focus:ring-red-500',
      'shadow-sm',
      'hover:shadow-md',
    ],
  };

  const classes = [
    ...baseClasses,
    ...sizeClasses[props.size],
    ...variantClasses[props.variant],
  ];

  if (props.fullWidth) {
    classes.push('w-full');
  }

  if (props.loading) {
    classes.push('cursor-wait');
  }

  return classes;
});

const handleClick = (event: MouseEvent) => {
  if (!props.disabled && !props.loading) {
    emit('click', event);
  }
};
</script>

<style scoped>
.loading-spinner {
  @apply w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin;
}

.button-text {
  @apply flex items-center gap-2;
}

/* Focus styles for accessibility */
button:focus-visible {
  @apply ring-2 ring-offset-2;
}

/* Hover animations */
button:not(:disabled):hover {
  @apply transform -translate-y-0.5;
}

button:not(:disabled):active {
  @apply transform translate-y-0;
}
</style>

