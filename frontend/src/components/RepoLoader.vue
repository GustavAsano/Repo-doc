<template>
  <div class="repo-loader">
    <!-- Source type selector -->
    <div class="source-tabs">
      <button
        v-for="s in sourceOptions"
        :key="s.value"
        class="tab-btn"
        :class="{ active: store.sourceType === s.value }"
        @click="store.sourceType = s.value"
      >
        <v-icon size="14" class="mr-1">{{ s.icon }}</v-icon>
        {{ s.label }}
      </button>
    </div>

    <!-- Git URL -->
    <div v-if="store.sourceType === 'git_url'" class="input-block">
      <v-text-field
        v-model="store.gitUrl"
        placeholder="https://github.com/org/repo.git"
        density="compact"
        variant="outlined"
        hide-details
        class="dark-input"
        prepend-inner-icon="mdi-github"
      />
    </div>

    <!-- Local folder -->
    <div v-if="store.sourceType === 'local_folder'" class="input-block">
      <v-text-field
        v-model="store.localPath"
        placeholder="/path/to/repository"
        density="compact"
        variant="outlined"
        hide-details
        class="dark-input"
        prepend-inner-icon="mdi-folder-outline"
      />
    </div>

    <!-- ZIP upload -->
    <div v-if="store.sourceType === 'zip'" class="input-block">
      <div
        class="drop-zone"
        :class="{ 'drag-over': dragging }"
        @dragover.prevent="dragging = true"
        @dragleave="dragging = false"
        @drop.prevent="onDrop"
        @click="fileInput?.click()"
      >
        <input ref="fileInput" type="file" accept=".zip" style="display:none" @change="onFileChange" />
        <v-icon size="28" color="teal" class="mb-2">mdi-archive-arrow-up-outline</v-icon>
        <div v-if="store.zipFile" class="zip-name">{{ store.zipFile.name }}</div>
        <div v-else class="drop-hint">Drop .zip here or click to browse</div>
      </div>
    </div>

    <!-- Library picker -->
    <div v-if="store.sourceType === 'library'" class="input-block">
      <div v-if="store.library.length === 0" class="empty-library">
        <v-icon color="#4b5563">mdi-archive-off-outline</v-icon>
        <span>No saved repositories yet</span>
      </div>
      <div v-else class="library-list">
        <div
          v-for="entry in store.library"
          :key="entry.entry_key"
          class="lib-entry"
          :class="{ selected: store.selectedLibraryKey === entry.entry_key }"
          @click="store.selectedLibraryKey = entry.entry_key"
        >
          <div class="lib-name">{{ entry.repo_name }}</div>
          <div class="lib-meta">
            <span class="badge lang">{{ entry.language }}</span>
            <span v-if="entry.docs_available" class="badge tech">tech</span>
            <span v-if="entry.functional_docs_available" class="badge func">func</span>
            <span class="lib-date">{{ formatDate(entry.updated_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Language + mode row -->
    <div class="options-row">
      <div class="opt-group">
        <div class="opt-label">Language</div>
        <v-select
          v-model="store.language"
          :items="LANGUAGES"
          item-title="label"
          item-value="value"
          density="compact"
          variant="outlined"
          hide-details
          class="dark-select"
          style="min-width:140px"
        />
      </div>
      <div v-if="store.sourceType !== 'library'" class="opt-group">
        <div class="opt-label">Generate</div>
        <v-select
          v-model="store.generationMode"
          :items="modes"
          item-title="label"
          item-value="value"
          density="compact"
          variant="outlined"
          hide-details
          class="dark-select"
          style="min-width:220px"
        />
      </div>
    </div>

    <!-- Action button -->
    <v-btn
      block
      color="teal"
      :loading="store.loading"
      :disabled="!canLoad"
      class="load-btn"
      @click="load"
    >
      <v-icon start>{{ store.sourceType === 'library' ? 'mdi-book-open-variant' : 'mdi-database-import-outline' }}</v-icon>
      {{ store.sourceType === 'library' ? 'Load from library' : 'Load repository' }}
    </v-btn>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useToast } from 'vue-toastification';
import { useAppStore } from '@/stores/store';
import { LANGUAGES } from '@/types/types';
import axios from 'axios';
import {
  loadRepoFromUrl,
  loadRepoFromFolder,
  uploadZip,
  loadRepoFromZip,
  activateLibraryEntry,
} from '@/services/backend';

const emit = defineEmits<{ loaded: [] }>();
const store = useAppStore();
const toast = useToast();
const dragging = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);

const sourceOptions = [
  { value: 'git_url' as const,      label: 'Git URL',    icon: 'mdi-git' },
  { value: 'local_folder' as const, label: 'Local',      icon: 'mdi-folder-outline' },
  { value: 'zip' as const,          label: 'ZIP',        icon: 'mdi-archive-outline' },
  { value: 'library' as const,      label: 'Library',    icon: 'mdi-bookshelf' },
];

const modes = [
  { value: 'technical_only',           label: 'Technical docs' },
  { value: 'technical_and_functional', label: 'Technical + Functional' },
  { value: 'functional_only',          label: 'Functional docs only' },
];

const canLoad = computed(() => {
  if (store.loading) return false;
  if (store.sourceType === 'git_url') return !!store.gitUrl.trim();
  if (store.sourceType === 'local_folder') return !!store.localPath.trim();
  if (store.sourceType === 'zip') return !!store.zipFile;
  if (store.sourceType === 'library') return !!store.selectedLibraryKey;
  return false;
});

function onFileChange(e: Event) {
  const f = (e.target as HTMLInputElement).files?.[0];
  if (f) store.zipFile = f;
}
function onDrop(e: DragEvent) {
  dragging.value = false;
  const f = e.dataTransfer?.files?.[0];
  if (f?.name.endsWith('.zip')) store.zipFile = f;
}
function formatDate(d?: string) {
  if (!d) return '';
  try { return new Date(d).toLocaleDateString(); } catch { return ''; }
}

async function load() {
  store.loading = true;
  store.loadingMessage = 'Loading repository…';
  try {
    let state;
    if (store.sourceType === 'git_url') {
      state = await loadRepoFromUrl(store.gitUrl.trim(), store.language);
    } else if (store.sourceType === 'local_folder') {
      state = await loadRepoFromFolder(store.localPath.trim(), store.language);
    } else if (store.sourceType === 'zip' && store.zipFile) {
      const upload = await uploadZip(store.zipFile);
      store.zipUploadedPath = upload.path;
      state = await loadRepoFromZip(upload.path, store.language);
    } else if (store.sourceType === 'library') {
      state = await activateLibraryEntry(store.selectedLibraryKey, 'technical', true);
      if (state.mkdocs_port) {
        store.mkdocsPort = state.mkdocs_port;
        store.docsUrl = `http://127.0.0.1:${state.mkdocs_port}/`;
      }
    }
    store.repoState = state!;
    toast.success(`Repository "${state!.repo_name}" loaded`);
    emit('loaded');
  } catch (e: unknown) {
  if (axios.isAxiosError(e)) {
      const detail = e.response?.data?.detail ?? e.response?.data ?? e.message;
      toast.error('Load failed: ' + JSON.stringify(detail));
  } else {
    toast.error('Load failed: ' + String(e));
  }
  } finally {
    store.loading = false;
    store.loadingMessage = '';
  }
}
</script>

<style scoped>
.repo-loader { display: flex; flex-direction: column; gap: 14px; }
.source-tabs { display: flex; gap: 4px; flex-wrap: wrap; }
.tab-btn {
  padding: 5px 13px; border-radius: 4px; border: 1px solid #374151;
  background: transparent; color: #9ca3af; font-size: 12px; cursor: pointer;
  font-family: 'JetBrains Mono', monospace; transition: all 0.15s;
  display: flex; align-items: center;
}
.tab-btn:hover { border-color: #6b7280; color: #d1d5db; }
.tab-btn.active { border-color: #14b8a6; color: #14b8a6; background: rgba(20,184,166,0.08); }
.input-block { display: flex; flex-direction: column; gap: 8px; }
.drop-zone {
  border: 1.5px dashed #374151; border-radius: 8px; padding: 28px 16px;
  text-align: center; cursor: pointer; transition: all 0.2s;
  display: flex; flex-direction: column; align-items: center;
}
.drop-zone:hover, .drop-zone.drag-over { border-color: #14b8a6; background: rgba(20,184,166,0.05); }
.zip-name { color: #14b8a6; font-family: 'JetBrains Mono', monospace; font-size: 12px; }
.drop-hint { color: #6b7280; font-size: 12px; }
.library-list { display: flex; flex-direction: column; gap: 4px; max-height: 220px; overflow-y: auto; }
.lib-entry {
  padding: 10px 12px; border-radius: 6px; border: 1px solid #374151;
  cursor: pointer; transition: all 0.15s;
}
.lib-entry:hover { border-color: #4b5563; background: #1f2937; }
.lib-entry.selected { border-color: #14b8a6; background: rgba(20,184,166,0.08); }
.lib-name { font-size: 13px; color: #e5e7eb; font-weight: 500; margin-bottom: 4px; }
.lib-meta { display: flex; align-items: center; gap: 6px; }
.badge { padding: 1px 7px; border-radius: 10px; font-size: 10px; font-family: 'JetBrains Mono', monospace; }
.badge.lang { background: #1f2937; color: #9ca3af; border: 1px solid #374151; }
.badge.tech { background: rgba(20,184,166,0.15); color: #14b8a6; }
.badge.func { background: rgba(99,102,241,0.15); color: #818cf8; }
.lib-date { font-size: 10px; color: #6b7280; margin-left: auto; }
.empty-library { display: flex; align-items: center; gap: 8px; color: #6b7280; font-size: 13px; padding: 16px; }
.options-row { display: flex; gap: 12px; flex-wrap: wrap; align-items: flex-end; }
.opt-group { display: flex; flex-direction: column; gap: 5px; }
.opt-label { font-size: 11px; color: #6b7280; font-family: 'JetBrains Mono', monospace; }
.load-btn { font-family: 'JetBrains Mono', monospace !important; font-size: 12px !important; letter-spacing: 0.04em !important; }
</style>
