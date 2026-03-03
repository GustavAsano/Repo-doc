<template>
  <div class="sections-editor">
    <div class="tabs-row">
      <button
        class="sec-tab"
        :class="{ active: activeTab === 'tech' }"
        :style="showFuncTab ? '' : 'display:none'"
        @click="activeTab = 'tech'"
      >Technical</button>
      <button
        v-if="showFuncTab"
        class="sec-tab"
        :class="{ active: activeTab === 'func' }"
        @click="activeTab = 'func'"
      >Functional</button>
    </div>

    <div class="sec-table">
      <div class="sec-header">
        <span style="width:32px"></span>
        <span class="col-title">Section</span>
        <span class="col-desc">Description</span>
      </div>
      <div
        v-for="(sec, key) in activeSections"
        :key="key"
        class="sec-row"
        :class="{ disabled: !sec.enabled }"
      >
        <v-checkbox
          v-model="sec.enabled"
          density="compact"
          hide-details
          color="teal"
          style="flex-shrink:0; width:32px"
        />
        <v-text-field
          v-model="sec.title"
          density="compact"
          variant="plain"
          hide-details
          class="sec-title-input"
          :disabled="!sec.enabled"
        />
        <v-text-field
          v-model="sec.description"
          density="compact"
          variant="plain"
          hide-details
          class="sec-desc-input"
          :disabled="!sec.enabled"
        />
      </div>
    </div>

    <div class="actions-row">
      <v-btn size="small" variant="text" color="teal" prepend-icon="mdi-refresh" @click="reset">
        Reset to defaults
      </v-btn>
      <span class="enabled-count">{{ enabledCount }} / {{ totalCount }} enabled</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useAppStore } from '@/stores/store';

const store = useAppStore();
const props = defineProps<{ showFuncTab?: boolean }>();
const activeTab = ref<'tech' | 'func'>('tech');

const activeSections = computed(() =>
  activeTab.value === 'tech' ? store.techSections : store.funcSections,
);

const enabledCount = computed(() =>
  Object.values(activeSections.value).filter((s) => s.enabled).length,
);
const totalCount = computed(() => Object.keys(activeSections.value).length);

function reset() {
  if (activeTab.value === 'tech') {
    Object.values(store.techSections).forEach((s) => { s.enabled = true; });
  } else {
    Object.values(store.funcSections).forEach((s) => { s.enabled = true; });
  }
}
</script>

<style scoped>
.sections-editor { display: flex; flex-direction: column; gap: 10px; }
.tabs-row { display: flex; gap: 4px; }
.sec-tab {
  padding: 4px 12px; border-radius: 4px; border: 1px solid #374151;
  background: transparent; color: #9ca3af; font-size: 11px; cursor: pointer;
  font-family: 'JetBrains Mono', monospace; transition: all 0.15s;
}
.sec-tab.active { border-color: #14b8a6; color: #14b8a6; background: rgba(20,184,166,0.08); }
.sec-table { display: flex; flex-direction: column; border: 1px solid #1f2937; border-radius: 6px; overflow: hidden; }
.sec-header {
  display: flex; align-items: center; gap: 8px; padding: 6px 10px;
  background: #0d1117; border-bottom: 1px solid #1f2937;
  font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em; color: #4b5563;
  font-family: 'JetBrains Mono', monospace;
}
.col-title { width: 160px; flex-shrink: 0; }
.col-desc { flex: 1; }
.sec-row {
  display: flex; align-items: center; gap: 8px; padding: 4px 10px;
  border-bottom: 1px solid #111827; transition: background 0.1s;
}
.sec-row:last-child { border-bottom: none; }
.sec-row:hover { background: #111827; }
.sec-row.disabled { opacity: 0.45; }
.sec-title-input { width: 160px; flex-shrink: 0; font-size: 12px !important; }
.sec-desc-input { flex: 1; font-size: 12px !important; color: #6b7280; }
.actions-row { display: flex; align-items: center; justify-content: space-between; }
.enabled-count { font-size: 11px; color: #6b7280; font-family: 'JetBrains Mono', monospace; }
</style>
