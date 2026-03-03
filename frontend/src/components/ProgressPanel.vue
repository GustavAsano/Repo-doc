<template>
  <div class="progress-panel">
    <!-- Header -->
    <div class="prog-header">
      <div class="prog-title">
        <div class="pulse-dot" :class="{ active: store.generating }"></div>
        <span>{{ store.generating ? 'Generating documentation…' : (store.repoState?.docs_generated ? 'Done' : 'Ready') }}</span>
      </div>
      <div v-if="store.progressCost !== null" class="cost-badge">
        ${{ store.progressCost.toFixed(4) }}
      </div>
    </div>

    <!-- Progress bar -->
    <div class="prog-bar-wrap">
      <div
        class="prog-bar-fill"
        :style="{ width: barPct + '%', transition: 'width 0.4s ease' }"
        :class="{ done: !store.generating && store.repoState?.docs_generated }"
      ></div>
    </div>
    <div class="prog-counts">
      <span v-if="store.progressTotal > 0">
        {{ store.progressCurrent }} / {{ store.progressTotal }} LLM calls
      </span>
      <span v-if="store.progressPhase" class="prog-phase">{{ store.progressPhase }}</span>
    </div>

    <!-- Generate button -->
    <v-btn
      v-if="!store.generating"
      block
      color="teal"
      :loading="store.loading"
      :disabled="!canGenerate || store.generating"
      class="gen-btn"
      @click="generate"
    >
      <v-icon start>mdi-file-document-edit-outline</v-icon>
      Generate docs
    </v-btn>
    <v-btn
      v-else
      block
      variant="outlined"
      color="red-lighten-2"
      class="gen-btn"
      @click="cancel"
    >
      <v-icon start>mdi-stop-circle-outline</v-icon>
      Cancel
    </v-btn>

    <!-- Event log -->
    <div v-if="store.progressEvents.length > 0" class="event-log" ref="logEl">
      <div
        v-for="(ev, i) in store.progressEvents"
        :key="i"
        class="ev-line"
        :class="ev.event"
      >
        <span class="ev-icon">{{ eventIcon(String(ev.event)) }}</span>
        <span class="ev-msg">{{ eventLabel(ev) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, watch } from 'vue';
import { useToast } from 'vue-toastification';
import { useAppStore } from '@/stores/store';
import { generateDocs, getDocsServer } from '@/services/backend';

const store = useAppStore();
const toast = useToast();
const logEl = ref<HTMLElement | null>(null);
let abortCtrl: AbortController | null = null;

const canGenerate = computed(() =>
  !!store.repoState?.repo_name && store.llmSaved,
);

const barPct = computed(() => {
  if (!store.generating && store.repoState?.docs_generated) return 100;
  if (store.progressTotal === 0) return 0;
  return Math.min(99, Math.round((store.progressCurrent / store.progressTotal) * 100));
});

function eventIcon(event: string) {
  const m: Record<string, string> = { plan: '⚡', call_start: '→', call_end: '✓', done: '✦', error: '✗' };
  return m[event] ?? '·';
}
function eventLabel(ev: Record<string, unknown>) {
  if (ev.event === 'plan') return `Plan: ${ev.total_calls} calls`;
  if (ev.event === 'call_start') return `[${ev.current_call}/${ev.total_calls}] ${ev.phase ?? ''}`;
  if (ev.event === 'call_end') {
    const cost = ev.call_cost_usd != null ? ` · $${(ev.call_cost_usd as number).toFixed(4)}` : '';
    return `Done [${ev.current_call}/${ev.total_calls}]${cost}`;
  }
  if (ev.event === 'done') return 'Documentation complete';
  if (ev.event === 'error') return `Error: ${ev.message}`;
  return String(ev.message ?? ev.event ?? '');
}

async function scrollLog() {
  await nextTick();
  if (logEl.value) logEl.value.scrollTop = logEl.value.scrollHeight;
}

watch(() => store.progressEvents.length, scrollLog);

async function generate() {
  if (!store.repoState?.repo_name) return;
  store.generating = true;
  store.resetProgress();

  const showFunc = ['technical_and_functional', 'functional_only'].includes(store.generationMode);

  abortCtrl = generateDocs(
    {
      repo_name: store.repoState.repo_name,
      language: store.language,
      generation_mode: store.generationMode,
      provider: store.llm.provider,
      model: store.llm.model,
      use_system_key: store.llm.useSystemKey,
      api_key: store.llm.apiKey,
      documentation_sections: store.enabledTechSections,
      functional_sections: showFunc ? store.enabledFuncSections : undefined,
    },
    (ev) => store.pushProgressEvent(ev),
    async () => {
      store.generating = false;
      if (store.repoState) {
        store.repoState.docs_generated = true;
      }
      // Fetch docs server URL — use the backend proxy path so the iframe
      // works inside Docker (browser can't reach 127.0.0.1:<container-port>)
      try {
        const srv = await getDocsServer();
        store.mkdocsPort = srv.port;
        // Always route through the backend proxy: /docs/preview/
        store.docsUrl = '/docs/preview/';
      } catch { /* not critical */ }
      toast.success('Documentation generated!');
    },
    (msg) => {
      store.generating = false;
      toast.error(msg);
    },
  );
}

function cancel() {
  abortCtrl?.abort();
  store.generating = false;
  toast.warning('Generation cancelled');
}
</script>

<style scoped>
.progress-panel { display: flex; flex-direction: column; gap: 12px; }
.prog-header { display: flex; align-items: center; justify-content: space-between; }
.prog-title { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #9ca3af; font-family: 'JetBrains Mono', monospace; }
.pulse-dot { width: 8px; height: 8px; border-radius: 50%; background: #374151; flex-shrink: 0; }
.pulse-dot.active { background: #14b8a6; animation: pulse 1.2s infinite; }
@keyframes pulse { 0%,100% { opacity:1; transform:scale(1); } 50% { opacity:0.5; transform:scale(1.3); } }
.cost-badge { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #14b8a6; background: rgba(20,184,166,0.12); padding: 2px 8px; border-radius: 10px; }
.prog-bar-wrap { height: 4px; background: #1f2937; border-radius: 2px; overflow: hidden; }
.prog-bar-fill { height: 100%; background: #14b8a6; border-radius: 2px; }
.prog-bar-fill.done { background: #10b981; }
.prog-counts { display: flex; justify-content: space-between; font-size: 10px; color: #4b5563; font-family: 'JetBrains Mono', monospace; }
.prog-phase { color: #6b7280; font-style: italic; }
.gen-btn { font-family: 'JetBrains Mono', monospace !important; font-size: 12px !important; }
.event-log {
  max-height: 200px; overflow-y: auto; background: #0d1117;
  border: 1px solid #1f2937; border-radius: 6px; padding: 8px;
  display: flex; flex-direction: column; gap: 3px;
}
.ev-line { display: flex; gap: 8px; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #6b7280; }
.ev-icon { flex-shrink: 0; width: 14px; text-align: center; }
.ev-line.plan .ev-msg { color: #818cf8; }
.ev-line.call_start .ev-msg { color: #9ca3af; }
.ev-line.call_end .ev-msg { color: #4b5563; }
.ev-line.done .ev-msg { color: #10b981; font-weight: 600; }
.ev-line.error .ev-msg { color: #f87171; }
</style>
