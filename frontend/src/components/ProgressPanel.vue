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
    <div class="gen-btn-row">
      <button
        v-if="!store.generating"
        class="gen-btn"
        :disabled="!canGenerate || store.loading"
        @click="generate"
      >
        <v-icon size="14" class="mr-1">mdi-file-document-edit-outline</v-icon>
        Generate docs
      </button>
      <button
        v-else
        class="gen-btn cancel-btn"
        @click="cancel"
      >
        <v-icon size="14" class="mr-1">mdi-stop-circle-outline</v-icon>
        Cancel
      </button>
    </div>

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
function sectionLabel(ev: Record<string, unknown>): string {
  const phase = String(ev.phase ?? '');
  const section = ev.section != null ? String(ev.section).toUpperCase() : null;
  const sidx = ev.section_index != null ? ev.section_index : null;
  const stotal = ev.total_sections != null ? ev.total_sections : null;
  const isFunctional = phase.startsWith('functional_');
  const typePrefix = isFunctional ? 'Functional · ' : '';
  if (section && sidx != null && stotal != null)
    return `${typePrefix}Writing ${section} (${sidx}/${stotal})`;
  if (section)
    return `${typePrefix}Writing ${section}`;
  if (phase === 'section_writing' || phase === 'functional_section_writing')
    return `${typePrefix}Writing section`;
  if (phase === 'final_cleanup' || phase === 'functional_final_cleanup')
    return `${typePrefix}Final cleanup`;
  if (phase === 'evidence_extraction' || phase === 'functional_chunk_extraction')
    return 'Extracting evidence';
  return phase;
}

function eventLabel(ev: Record<string, unknown>) {
  if (ev.event === 'plan') return `Plan: ${ev.total_calls} calls`;
  if (ev.event === 'call_start') return `[${ev.current_call}/${ev.total_calls}] ${sectionLabel(ev)}`;
  if (ev.event === 'call_end') {
    const cost = ev.call_cost_usd != null ? ` · $${(ev.call_cost_usd as number).toFixed(4)}` : '';
    return `✓ ${sectionLabel(ev)} [${ev.current_call}/${ev.total_calls}]${cost}`;
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
.gen-btn-row { display: flex; }
.gen-btn {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 7px 18px; border-radius: 6px; border: 1px solid #14b8a6;
  background: rgba(20,184,166,0.12); color: #14b8a6;
  font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 600;
  cursor: pointer; transition: background 0.15s, border-color 0.15s;
  letter-spacing: 0.04em;
}
.gen-btn:hover:not(:disabled) { background: rgba(20,184,166,0.22); }
.gen-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.cancel-btn { border-color: #f87171; background: rgba(248,113,113,0.1); color: #f87171; }
.cancel-btn:hover { background: rgba(248,113,113,0.2); }
.progress-panel { flex: 1; }
.event-log {
  flex: 1; min-height: 120px; max-height: 480px; overflow-y: auto; background: #0d1117;
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

<style>
.v-theme--light .prog-title { color: #475569; }
.v-theme--light .pulse-dot { background: #cbd5e1; }
.v-theme--light .cost-badge { color: #0f766e; background: rgba(15,118,110,0.1); }
.v-theme--light .prog-bar-wrap { background: #e2e8f0; }
.v-theme--light .prog-counts { color: #94a3b8; }
.v-theme--light .prog-phase { color: #64748b; }
.v-theme--light .gen-btn { border-color: #0f766e; background: rgba(15,118,110,0.08); color: #0f766e; }
.v-theme--light .gen-btn:hover:not(:disabled) { background: rgba(15,118,110,0.15); }
.v-theme--light .event-log { background: #f8fafc; border-color: #e2e8f0; }
.v-theme--light .ev-line { color: #94a3b8; }
.v-theme--light .ev-line.plan .ev-msg { color: #6366f1; }
.v-theme--light .ev-line.call_start .ev-msg { color: #475569; }
.v-theme--light .ev-line.call_end .ev-msg { color: #94a3b8; }
.v-theme--light .ev-line.done .ev-msg { color: #059669; }
.v-theme--light .ev-line.error .ev-msg { color: #dc2626; }
</style>
