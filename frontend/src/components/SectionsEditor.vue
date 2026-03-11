<template>
  <div class="sections-editor">
    <div class="tabs-row" v-if="showFuncTab">
      <button class="sec-tab" :class="{ active: activeTab === 'tech' }" @click="activeTab = 'tech'">Technical</button>
      <button class="sec-tab" :class="{ active: activeTab === 'func' }" @click="activeTab = 'func'">Functional</button>
    </div>

    <div class="sec-table">
      <div class="sec-header">
        <span class="col-check"></span>
        <span class="col-title">Section</span>
        <span class="col-desc">Description</span>
        <span class="col-del"></span>
      </div>

      <div
        v-for="(sec, key) in activeSections"
        :key="key"
        class="sec-row"
        :class="{ disabled: !sec.enabled }"
      >
        <span class="col-check">
          <input type="checkbox" v-model="sec.enabled" class="sec-checkbox" />
        </span>
        <span class="col-title">
          <input
            v-model="sec.title"
            class="sec-input"
            :disabled="!sec.enabled"
            placeholder="Section title"
          />
        </span>
        <span class="col-desc">
          <input
            v-model="sec.description"
            class="sec-input desc-input"
            :disabled="!sec.enabled"
            placeholder="Description"
          />
        </span>
        <span class="col-del">
          <button class="del-btn" @click="removeSection(String(key))" title="Remove section">×</button>
        </span>
      </div>

      <!-- Add new section row -->
      <div v-if="adding" class="sec-row add-row">
        <span class="col-check"></span>
        <span class="col-title">
          <input
            v-model="newTitle"
            class="sec-input"
            placeholder="Title"
            ref="newTitleInput"
            @keydown.enter="confirmAdd"
            @keydown.esc="cancelAdd"
          />
        </span>
        <span class="col-desc">
          <input
            v-model="newDesc"
            class="sec-input desc-input"
            placeholder="Description"
            @keydown.enter="confirmAdd"
            @keydown.esc="cancelAdd"
          />
        </span>
        <span class="col-del">
          <button class="confirm-btn" @click="confirmAdd" title="Add">✓</button>
        </span>
      </div>
    </div>

    <div class="actions-row">
      <div class="actions-left">
        <button class="action-btn" @click="startAdd">+ Add section</button>
        <button class="action-btn muted" @click="reset">↺ Reset</button>
      </div>
      <span class="enabled-count">{{ enabledCount }} / {{ totalCount }} enabled</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue';
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

// Add section
const adding = ref(false);
const newTitle = ref('');
const newDesc = ref('');
const newTitleInput = ref<HTMLInputElement | null>(null);

function startAdd() {
  adding.value = true;
  newTitle.value = '';
  newDesc.value = '';
  nextTick(() => newTitleInput.value?.focus());
}

function confirmAdd() {
  const title = newTitle.value.trim();
  if (!title) return;
  const key = title.toUpperCase().replace(/[^A-Z0-9]+/g, '_').replace(/^_|_$/g, '') + '_' + Date.now().toString(36).slice(-4);
  store.addSection(activeTab.value, key, title, newDesc.value.trim());
  adding.value = false;
}

function cancelAdd() {
  adding.value = false;
}

function removeSection(key: string) {
  store.removeSection(activeTab.value, key);
}

function reset() {
  store.resetSections();
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

.sec-table {
  display: flex; flex-direction: column;
  border: 1px solid #1f2937; border-radius: 6px; overflow: hidden;
}

.sec-header, .sec-row {
  display: grid;
  grid-template-columns: 28px 160px 1fr 28px;
  align-items: center;
  gap: 0;
}

.sec-header {
  padding: 5px 8px; background: #0d1117;
  border-bottom: 1px solid #1f2937;
  font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em;
  color: #4b5563; font-family: 'JetBrains Mono', monospace;
}

.sec-row {
  padding: 3px 8px;
  border-bottom: 1px solid #111827; transition: background 0.1s;
  min-height: 32px;
}
.sec-row:last-child { border-bottom: none; }
.sec-row:hover { background: #111827; }
.sec-row.disabled { opacity: 0.45; }
.sec-row.add-row { background: rgba(20,184,166,0.04); }

.col-check { display: flex; align-items: center; justify-content: center; }
.col-title { padding-right: 8px; }
.col-desc { padding-right: 4px; }
.col-del { display: flex; align-items: center; justify-content: center; }

.sec-checkbox {
  width: 14px; height: 14px; accent-color: #14b8a6; cursor: pointer; margin: 0;
}

.sec-input {
  width: 100%;
  background: transparent;
  border: none;
  outline: none;
  color: #e5e7eb;
  font-size: 12px;
  font-family: inherit;
  padding: 3px 0;
  line-height: 1.4;
}
.sec-input::placeholder { color: #4b5563; }
.sec-input:disabled { color: #4b5563; cursor: default; }
.sec-input.desc-input { color: #9ca3af; font-size: 11px; }

.del-btn {
  background: none; border: none; color: #4b5563; font-size: 16px;
  cursor: pointer; line-height: 1; padding: 2px 4px; border-radius: 3px;
  transition: color 0.15s;
}
.del-btn:hover { color: #ef4444; }

.confirm-btn {
  background: none; border: none; color: #14b8a6; font-size: 14px;
  cursor: pointer; line-height: 1; padding: 2px 4px; border-radius: 3px;
  transition: color 0.15s;
}
.confirm-btn:hover { color: #5eead4; }

.actions-row {
  display: flex; align-items: center; justify-content: space-between;
}
.actions-left { display: flex; gap: 8px; }

.action-btn {
  background: none; border: 1px solid #374151; color: #9ca3af;
  font-size: 11px; padding: 3px 10px; border-radius: 4px; cursor: pointer;
  font-family: 'JetBrains Mono', monospace; transition: all 0.15s;
}
.action-btn:hover { border-color: #14b8a6; color: #14b8a6; }
.action-btn.muted:hover { border-color: #6b7280; color: #d1d5db; }

.enabled-count { font-size: 11px; color: #6b7280; font-family: 'JetBrains Mono', monospace; }
</style>
