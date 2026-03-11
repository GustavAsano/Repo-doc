<template>
  <div class="export-panel">
    <div class="export-row">
      <button class="export-btn pdf" :class="{ loading: loadingPdf }" :disabled="!canExport" @click="doExport('pdf')">
        <v-icon size="16" class="mr-2">mdi-file-pdf-box</v-icon>
        {{ loadingPdf ? 'Building…' : 'Download PDF' }}
      </button>
      <button class="export-btn word" :class="{ loading: loadingDocx }" :disabled="!canExport" @click="doExport('docx')">
        <v-icon size="16" class="mr-2">mdi-file-word-box</v-icon>
        {{ loadingDocx ? 'Building…' : 'Download Word' }}
      </button>
    </div>
    <div v-if="store.repoState?.functional_docs_generated" class="variant-row">
      <span class="variant-label">Variant:</span>
      <button
        class="var-btn"
        :class="{ active: variant === 'technical' }"
        @click="variant = 'technical'"
      >Technical</button>
      <button
        class="var-btn"
        :class="{ active: variant === 'functional' }"
        @click="variant = 'functional'"
      >Functional</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useToast } from 'vue-toastification';
import { useAppStore } from '@/stores/store';
import { exportDoc } from '@/services/backend';

const store = useAppStore();
const toast = useToast();
const loadingPdf = ref(false);
const loadingDocx = ref(false);
const variant = ref<'technical' | 'functional'>('technical');

const canExport = computed(() => store.repoState?.docs_generated || store.repoState?.functional_docs_generated);

async function doExport(format: 'pdf' | 'docx') {
  if (!store.repoState?.repo_name) return;
  if (format === 'pdf') loadingPdf.value = true;
  else loadingDocx.value = true;

  try {
    const res = await exportDoc(store.repoState.repo_name, format, store.language, variant.value);
    // Trigger browser download from base64
    const mime = format === 'pdf' ? 'application/pdf' : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
    const blob = b64toBlob(res.data, mime);
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = res.filename;
    a.click();
    URL.revokeObjectURL(url);
    toast.success(`${format.toUpperCase()} downloaded`);
  } catch (e: unknown) {
    toast.error('Export failed: ' + String(e));
  } finally {
    loadingPdf.value = false;
    loadingDocx.value = false;
  }
}

function b64toBlob(b64: string, type: string): Blob {
  const bin = atob(b64);
  const arr = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
  return new Blob([arr], { type });
}
</script>

<style scoped>
.export-panel { display: flex; flex-direction: column; gap: 10px; }
.export-row { display: flex; gap: 8px; }
.export-btn {
  flex: 1; padding: 8px 12px; border-radius: 6px; border: 1px solid #374151;
  background: transparent; color: #9ca3af; font-size: 12px; cursor: pointer;
  font-family: 'JetBrains Mono', monospace; transition: all 0.15s;
  display: flex; align-items: center; justify-content: center;
}
.export-btn:hover:not(:disabled) { border-color: #6b7280; color: #e5e7eb; }
.export-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.export-btn.pdf:hover:not(:disabled) { border-color: #ef4444; color: #fca5a5; }
.export-btn.word:hover:not(:disabled) { border-color: #3b82f6; color: #93c5fd; }
.export-btn.loading { opacity: 0.7; cursor: wait; }
.variant-row { display: flex; align-items: center; gap: 8px; }
.variant-label { font-size: 10px; color: #6b7280; font-family: 'JetBrains Mono', monospace; }
.var-btn {
  padding: 3px 10px; border-radius: 3px; border: 1px solid #374151;
  background: transparent; color: #6b7280; font-size: 11px; cursor: pointer;
  font-family: 'JetBrains Mono', monospace; transition: all 0.12s;
}
.var-btn.active { border-color: #14b8a6; color: #14b8a6; }
</style>
