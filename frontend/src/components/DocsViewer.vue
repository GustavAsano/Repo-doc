<template>
  <div class="docs-viewer">
    <div class="docs-toolbar">
      <span class="docs-label">
        <v-icon size="14" class="mr-1" color="teal">mdi-book-open-page-variant-outline</v-icon>
        Documentation
      </span>
      <div class="docs-actions">
        <button v-if="store.docsUrl" class="tool-btn" title="Open in new tab" @click="openTab">
          <v-icon size="15">mdi-open-in-new</v-icon>
        </button>
        <button class="tool-btn" title="Refresh" @click="refresh">
          <v-icon size="15">mdi-refresh</v-icon>
        </button>
        <div v-if="store.mkdocsPort" class="port-badge">:{{ store.mkdocsPort }}</div>
      </div>
    </div>

    <div v-if="!store.docsUrl" class="docs-placeholder">
      <v-icon size="40" color="#374151">mdi-file-document-outline</v-icon>
      <span class="ph-text">Generate documentation to preview it here</span>
    </div>

    <iframe
      v-else
      ref="iframeEl"
      :src="iframeSrc"
      class="docs-iframe"
      frameborder="0"
      @load="iframeLoaded = true"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useAppStore } from '@/stores/store';

const store = useAppStore();
const iframeEl = ref<HTMLIFrameElement | null>(null);
const iframeLoaded = ref(false);
const bust = ref(0);

const iframeSrc = computed(() => {
  if (!store.docsUrl) return '';
  const url = new URL(store.docsUrl);
  if (bust.value > 0) url.searchParams.set('_v', String(bust.value));
  return url.toString();
});

function openTab() { window.open(store.docsUrl, '_blank'); }
function refresh() { bust.value++; iframeLoaded.value = false; }

watch(() => store.docsUrl, () => { iframeLoaded.value = false; });
</script>

<style scoped>
.docs-viewer { display: flex; flex-direction: column; height: 100%; }
.docs-toolbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 12px; background: #0d1117; border-bottom: 1px solid #1f2937; flex-shrink: 0;
}
.docs-label { display: flex; align-items: center; font-size: 12px; color: #9ca3af; font-family: 'JetBrains Mono', monospace; }
.docs-actions { display: flex; align-items: center; gap: 6px; }
.tool-btn {
  width: 28px; height: 28px; border-radius: 4px; border: 1px solid #374151;
  background: transparent; color: #6b7280; cursor: pointer;
  display: flex; align-items: center; justify-content: center; transition: all 0.15s;
}
.tool-btn:hover { border-color: #6b7280; color: #d1d5db; }
.port-badge { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #4b5563; }
.docs-placeholder { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; background: #0d1117; }
.ph-text { font-size: 12px; color: #4b5563; font-family: 'JetBrains Mono', monospace; text-align: center; max-width: 260px; }
.docs-iframe { flex: 1; width: 100%; border: none; background: #fff; }
</style>
