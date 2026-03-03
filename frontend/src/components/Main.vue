<template>
  <v-main class="app-main">
    <div class="layout">

      <!-- ── LEFT SIDEBAR ─────────────────────────────────────────────── -->
      <aside class="sidebar">
        <div class="sidebar-scroll">

          <!-- LLM Settings -->
          <div class="side-section">
            <div class="side-title" @click="togglePanel('llm')">
              <v-icon size="13" class="mr-2" color="teal">mdi-cpu-64-bit</v-icon>
              LLM Settings
              <v-icon size="14" class="ml-auto" :class="{ rotated: !panels.llm }">mdi-chevron-down</v-icon>
            </div>
            <transition name="collapse">
              <div v-show="panels.llm" class="panel-body">
                <LLMSettings />
              </div>
            </transition>
          </div>

          <!-- Repository -->
          <div class="side-section">
            <div class="side-title" @click="togglePanel('repo')">
              <v-icon size="13" class="mr-2" color="teal">mdi-source-repository</v-icon>
              Repository
              <v-icon size="14" class="ml-auto" :class="{ rotated: !panels.repo }">mdi-chevron-down</v-icon>
            </div>
            <transition name="collapse">
              <div v-show="panels.repo" class="panel-body">
                <RepoLoader @loaded="onRepoLoaded" />
              </div>
            </transition>
          </div>

          <!-- Generation -->
          <div class="side-section" v-if="store.repoState">
            <div class="side-title" @click="togglePanel('gen')">
              <v-icon size="13" class="mr-2" color="teal">mdi-file-document-edit-outline</v-icon>
              Generation
              <v-icon size="14" class="ml-auto" :class="{ rotated: !panels.gen }">mdi-chevron-down</v-icon>
            </div>
            <transition name="collapse">
              <div v-show="panels.gen" class="panel-body">
                <ProgressPanel />
              </div>
            </transition>
          </div>

          <!-- Sections -->
          <div class="side-section" v-if="store.repoState">
            <div class="side-title" @click="togglePanel('sec')">
              <v-icon size="13" class="mr-2" color="#6366f1">mdi-table-edit</v-icon>
              Sections
              <v-icon size="14" class="ml-auto" :class="{ rotated: !panels.sec }">mdi-chevron-down</v-icon>
            </div>
            <transition name="collapse">
              <div v-show="panels.sec" class="panel-body">
                <SectionsEditor :show-func-tab="showFuncSections" />
              </div>
            </transition>
          </div>

          <!-- Export -->
          <div class="side-section" v-if="store.hasActiveDocs">
            <div class="side-title" @click="togglePanel('export')">
              <v-icon size="13" class="mr-2" color="#f59e0b">mdi-download-outline</v-icon>
              Export
              <v-icon size="14" class="ml-auto" :class="{ rotated: !panels.export }">mdi-chevron-down</v-icon>
            </div>
            <transition name="collapse">
              <div v-show="panels.export" class="panel-body">
                <ExportButtons />
              </div>
            </transition>
          </div>

        </div>
      </aside>

      <!-- ── MAIN CONTENT ─────────────────────────────────────────────── -->
      <section class="content">

        <!-- Tabs -->
        <div class="content-tabs">
          <button
            v-for="tab in visibleTabs"
            :key="tab.id"
            class="c-tab"
            :class="{ active: activeTab === tab.id }"
            @click="activeTab = tab.id"
          >
            <v-icon size="13" class="mr-1">{{ tab.icon }}</v-icon>
            {{ tab.label }}
          </button>
        </div>

        <!-- Tab content -->
        <div class="tab-body">
          <!-- Welcome / setup -->
          <div v-if="activeTab === 'welcome'" class="welcome-view">
            <div class="welcome-inner">
              <div class="welcome-glyph">⊕</div>
              <h1 class="welcome-h1">Repository Documentation</h1>
              <p class="welcome-sub">Configure your LLM, load a repository, then generate technical and functional documentation.</p>
              <div class="welcome-steps">
                <div class="w-step" :class="{ done: store.llmSaved }">
                  <div class="step-num">1</div>
                  <div class="step-text">Configure LLM provider</div>
                  <v-icon v-if="store.llmSaved" size="14" color="teal">mdi-check</v-icon>
                </div>
                <div class="w-step" :class="{ done: !!store.repoState }">
                  <div class="step-num">2</div>
                  <div class="step-text">Load repository</div>
                  <v-icon v-if="store.repoState" size="14" color="teal">mdi-check</v-icon>
                </div>
                <div class="w-step" :class="{ done: store.hasActiveDocs }">
                  <div class="step-num">3</div>
                  <div class="step-text">Generate documentation</div>
                  <v-icon v-if="store.hasActiveDocs" size="14" color="teal">mdi-check</v-icon>
                </div>
              </div>
            </div>
          </div>

          <!-- Docs -->
          <DocsViewer v-if="activeTab === 'docs'" />

          <!-- Graph -->
          <GraphViewer v-if="activeTab === 'graph'" />

          <!-- Chat -->
          <ChatPanel v-if="activeTab === 'chat'" />
        </div>
      </section>
    </div>
  </v-main>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useAppStore } from '@/stores/store';
import { getLibrary } from '@/services/backend';
import LLMSettings from '@/components/LLMSettings.vue';
import RepoLoader from '@/components/RepoLoader.vue';
import ProgressPanel from '@/components/ProgressPanel.vue';
import SectionsEditor from '@/components/SectionsEditor.vue';
import ExportButtons from '@/components/ExportButtons.vue';
import DocsViewer from '@/components/DocsViewer.vue';
import GraphViewer from '@/components/GraphViewer.vue';
import ChatPanel from '@/components/ChatPanel.vue';

const store = useAppStore();
const activeTab = ref('welcome');

const panels = ref({ llm: true, repo: true, gen: true, sec: false, export: true });
function togglePanel(key: keyof typeof panels.value) {
  panels.value[key] = !panels.value[key];
}

const showFuncSections = computed(() =>
  ['technical_and_functional', 'functional_only'].includes(store.generationMode),
);

const allTabs = [
  { id: 'welcome', label: 'Home',       icon: 'mdi-home-outline',                  always: true },
  { id: 'docs',    label: 'Docs',       icon: 'mdi-book-open-page-variant-outline', always: false },
  { id: 'graph',   label: 'Graph',      icon: 'mdi-graph-outline',                  always: false },
  { id: 'chat',    label: 'Chat',       icon: 'mdi-message-text-outline',           always: false },
];

const visibleTabs = computed(() =>
  allTabs.filter((t) => t.always || !!store.repoState),
);

function onRepoLoaded() {
  panels.value.gen = true;
  panels.value.sec = true;
  if (store.hasActiveDocs) {
    activeTab.value = 'docs';
  }
}

watch(() => store.hasActiveDocs, (v) => {
  if (v && activeTab.value === 'welcome') activeTab.value = 'docs';
});

// Load library on mount
getLibrary('technical').then((entries) => { store.library = entries; }).catch(() => {});
getLibrary('functional').then((entries) => { store.functionalLibrary = entries; }).catch(() => {});
</script>

<style scoped>
.app-main { background: #080c12 !important; }
.layout { display: flex; height: calc(100vh - 64px); overflow: hidden; }

/* Sidebar */
.sidebar { width: 320px; min-width: 280px; flex-shrink: 0; background: #0a0e17; border-right: 1px solid #1f2937; display: flex; flex-direction: column; overflow: hidden; }
.sidebar-scroll { flex: 1; overflow-y: auto; padding: 8px 0; }
.sidebar-scroll::-webkit-scrollbar { width: 4px; }
.sidebar-scroll::-webkit-scrollbar-track { background: transparent; }
.sidebar-scroll::-webkit-scrollbar-thumb { background: #1f2937; border-radius: 2px; }

/* Side sections */
.side-section { border-bottom: 1px solid #111827; }
.side-title {
  display: flex; align-items: center; padding: 10px 16px; cursor: pointer;
  font-family: 'JetBrains Mono', monospace; font-size: 11px; text-transform: uppercase;
  letter-spacing: 0.08em; color: #6b7280; transition: color 0.15s; user-select: none;
}
.side-title:hover { color: #9ca3af; }
.side-title .rotated { transform: rotate(-90deg); }
.panel-body { padding: 0 16px 14px; }

/* Collapse animation */
.collapse-enter-active, .collapse-leave-active { transition: max-height 0.22s ease, opacity 0.18s; overflow: hidden; }
.collapse-enter-from, .collapse-leave-to { max-height: 0; opacity: 0; }
.collapse-enter-to, .collapse-leave-from { max-height: 600px; opacity: 1; }

/* Content area */
.content { flex: 1; display: flex; flex-direction: column; overflow: hidden; background: #080c12; }

/* Tabs */
.content-tabs { display: flex; gap: 0; padding: 0 16px; background: #0a0e17; border-bottom: 1px solid #1f2937; flex-shrink: 0; }
.c-tab {
  padding: 10px 16px; background: transparent; border: none; border-bottom: 2px solid transparent;
  color: #6b7280; font-size: 12px; font-family: 'JetBrains Mono', monospace; cursor: pointer;
  display: flex; align-items: center; transition: all 0.15s; margin-bottom: -1px;
}
.c-tab:hover { color: #9ca3af; }
.c-tab.active { color: #14b8a6; border-bottom-color: #14b8a6; }

.tab-body { flex: 1; overflow: hidden; display: flex; flex-direction: column; }

/* Welcome view */
.welcome-view { flex: 1; display: flex; align-items: center; justify-content: center; padding: 40px; }
.welcome-inner { max-width: 440px; display: flex; flex-direction: column; align-items: center; gap: 16px; text-align: center; }
.welcome-glyph { font-size: 48px; color: #1f2937; line-height: 1; }
.welcome-h1 { font-family: 'Syne', sans-serif; font-size: 26px; font-weight: 800; color: #e5e7eb; letter-spacing: -0.02em; margin: 0; }
.welcome-sub { font-size: 13px; color: #6b7280; line-height: 1.6; margin: 0; }
.welcome-steps { display: flex; flex-direction: column; gap: 8px; width: 100%; margin-top: 8px; }
.w-step {
  display: flex; align-items: center; gap: 12px; padding: 10px 14px;
  background: #0d1117; border: 1px solid #1f2937; border-radius: 6px;
  font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #6b7280;
  transition: border-color 0.2s;
}
.w-step.done { border-color: rgba(20,184,166,0.3); color: #9ca3af; }
.step-num { width: 20px; height: 20px; border-radius: 50%; background: #1f2937; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #4b5563; flex-shrink: 0; }
.w-step.done .step-num { background: rgba(20,184,166,0.15); color: #14b8a6; }
.step-text { flex: 1; }
</style>
