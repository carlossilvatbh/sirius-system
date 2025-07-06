<template>
  <div class="input-wrapper">
    <label v-if="label" :for="inputId" class="input-label">
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1">*</span>
    </label>
    
    <div class="relative">
      <div v-if="$slots.prefix" class="input-prefix">
        <slot name="prefix"></slot>
      </div>
      
      <input
        :id="inputId"
        v-model="inputValue"
        :type="type"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :class="inputClasses"
        @blur="handleBlur"
        @focus="handleFocus"
        @input="handleInput"
      />
      
      <div v-if="$slots.suffix" class="input-suffix">
        <slot name="suffix"></slot>
      </div>
    </div>
    
    <div v-if="error || hint" class="input-message">
      <p v-if="error" class="text-red-600 text-sm">{{ error }}</p>
      <p v-else-if="hint" class="text-gray-500 text-sm">{{ hint }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { generateId } from '@/utils/helpers';

interface Props {
  modelValue?: string | number;
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search';
  label?: string;
  placeholder?: string;
  hint?: string;
  error?: string;
  disabled?: boolean;
  readonly?: boolean;
  required?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

interface Emits {
  (e: 'update:modelValue', value: string | number): void;
  (e: 'blur', event: FocusEvent): void;
  (e: 'focus', event: FocusEvent): void;
  (e: 'input', event: Event): void;
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  size: 'md',
  disabled: false,
  readonly: false,
  required: false,
});

const emit = defineEmits<Emits>();

const inputId = ref(generateId());
const isFocused = ref(false);

const inputValue = computed({
  get: () => props.modelValue ?? '',
  set: (value) => {
    const processedValue = props.type === 'number' ? Number(value) : value;
    emit('update:modelValue', processedValue);
  },
});

const inputClasses = computed(() => {
  const baseClasses = [
    'block',
    'w-full',
    'border',
    'rounded-lg',
    'transition-all',
    'duration-200',
    'focus:outline-none',
    'focus:ring-2',
    'focus:ring-offset-1',
    'disabled:opacity-50',
    'disabled:cursor-not-allowed',
    'readonly:bg-gray-50',
    'readonly:cursor-default',
  ];

  // Size classes
  const sizeClasses = {
    sm: ['px-3', 'py-1.5', 'text-sm'],
    md: ['px-3', 'py-2', 'text-sm'],
    lg: ['px-4', 'py-3', 'text-base'],
  };

  // State classes
  const stateClasses = props.error
    ? [
        'border-red-300',
        'focus:border-red-500',
        'focus:ring-red-500',
      ]
    : [
        'border-gray-300',
        'focus:border-sirius-500',
        'focus:ring-sirius-500',
      ];

  // Prefix/suffix padding
  const paddingClasses = [];
  if (props.$slots?.prefix) {
    paddingClasses.push('pl-10');
  }
  if (props.$slots?.suffix) {
    paddingClasses.push('pr-10');
  }

  return [
    ...baseClasses,
    ...sizeClasses[props.size],
    ...stateClasses,
    ...paddingClasses,
  ];
});

const handleBlur = (event: FocusEvent) => {
  isFocused.value = false;
  emit('blur', event);
};

const handleFocus = (event: FocusEvent) => {
  isFocused.value = true;
  emit('focus', event);
};

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement;
  inputValue.value = target.value;
  emit('input', event);
};
</script>

<style scoped>
.input-wrapper {
  @apply space-y-1;
}

.input-label {
  @apply block text-sm font-medium text-gray-700;
}

.input-prefix {
  @apply absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400;
}

.input-suffix {
  @apply absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400;
}

.input-message {
  @apply mt-1;
}

/* Custom focus styles */
input:focus {
  @apply ring-2 ring-offset-1;
}

/* Placeholder styles */
input::placeholder {
  @apply text-gray-400;
}

/* Number input styles */
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield;
}
</style>

