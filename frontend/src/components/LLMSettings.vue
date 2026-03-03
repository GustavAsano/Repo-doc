<template>
  <div class="settings-panel">
    <div class="section-label">LLM Provider</div>
    <div class="provider-pills">
      <button
        v-for="p in providers"
        :key="p.value"
        class="pill"
        :class="{ active: store.llm.provider === p.value }"
        @click="setProvider(p.value)"
      >{{ p.label }}</button>
    </div>

    <div class="field-row">
      <div class="field-group" style="flex:1">
        <div class="field-label">Model</div>
        <v-select
          v-model="store.llm.model"
          :items="store.activeModels"
          density="compact"
          variant="outlined"
          hide-details
          class="dark-select"
        />
      </div>
    </div>

    <div v-if="store.llm.provider !== 'bedrock'" class="field-row">
      <div class="field-group" style="flex:1">
        <div class="field-label">API Key</div>
        <div class="key-row">
          <v-checkbox
            v-model="store.llm.useSystemKey"
            label="Use server key"
            density="compact"
            hide-details
            color="teal"
            class="sys-check"
          />
          <v-text-field
            v-if="!store.llm.useSystemKey"
            v-model="store.llm.apiKey"
            type="password"
            placeholder="sk-..."
            density="compact"
            variant="outlined"
            hide-details
            class="dark-input flex-1"
          />
        </div>
      </div>
    </div>

    <div v-if="store.llm.provider === 'bedrock'" class="field-row">
      <div class="field-group" style="flex:1">
        <v-checkbox
          v-model="store.llm.useSystemKey"
          label="Use instance role / env credentials"
          density="compact"
          hide-details
          color="teal"
        />
        <template v-if="!store.llm.useSystemKey">
          <v-text-field
            v-model="store.llm.bedrockAccessKey"
            label="AWS Access Key ID"
            density="compact"
            variant="outlined"
            hide-details
            class="dark-input mt-2"
          />
          <v-text-field
            v-model="store.llm.bedrockSecretKey"
            label="AWS Secret Access Key"
            type="password"
            density="compact"
            variant="outlined"
            hide-details
            class="dark-input mt-2"
          />
        </template>
      </div>
    </div>

    <v-btn
      block
      :color="store.llmSaved ? 'teal' : 'white'"
      :variant="store.llmSaved ? 'flat' : 'outlined'"
      :loading="saving"
      class="save-btn mt-3"
      @click="save"
    >
      <v-icon start>{{ store.llmSaved ? 'mdi-check' : 'mdi-content-save-outline' }}</v-icon>
      {{ store.llmSaved ? 'Settings saved' : 'Save settings' }}
    </v-btn>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useToast } from 'vue-toastification';
import { useAppStore } from '@/stores/store';
import { saveLLMSettings } from '@/services/backend';
import type { LLMProvider } from '@/types/types';
import { PROVIDER_MODELS } from '@/types/types';

const store = useAppStore();
const toast = useToast();
const saving = ref(false);

const providers = [
  { value: 'gemini' as LLMProvider, label: 'Gemini' },
  { value: 'openai' as LLMProvider, label: 'OpenAI' },
  { value: 'bedrock' as LLMProvider, label: 'Bedrock' },
];

function setProvider(p: LLMProvider) {
  store.llm.provider = p;
  store.llm.model = PROVIDER_MODELS[p][0];
  store.llmSaved = false;
}

async function save() {
  saving.value = true;
  try {
    await saveLLMSettings(store.llm);
    store.llmSaved = true;
    toast.success('LLM settings saved');
  } catch (e: unknown) {
    toast.error('Failed to save: ' + String(e));
  } finally {
    saving.value = false;
  }
}
</script>

<style scoped>
.settings-panel { display: flex; flex-direction: column; gap: 12px; }
.section-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; color: #6b7280; font-family: 'JetBrains Mono', monospace; }
.provider-pills { display: flex; gap: 6px; }
.pill {
  padding: 5px 14px; border-radius: 4px; border: 1px solid #374151;
  background: transparent; color: #9ca3af; font-size: 12px; cursor: pointer;
  font-family: 'JetBrains Mono', monospace; transition: all 0.15s;
}
.pill:hover { border-color: #6b7280; color: #d1d5db; }
.pill.active { border-color: #14b8a6; color: #14b8a6; background: rgba(20,184,166,0.08); }
.field-row { display: flex; gap: 10px; }
.field-group { display: flex; flex-direction: column; gap: 6px; }
.field-label { font-size: 11px; color: #6b7280; font-family: 'JetBrains Mono', monospace; }
.key-row { display: flex; align-items: center; gap: 12px; }
.save-btn { font-family: 'JetBrains Mono', monospace !important; font-size: 12px !important; letter-spacing: 0.05em !important; }
</style>
