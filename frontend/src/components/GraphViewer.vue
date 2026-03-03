<template>
  <div class="graph-viewer">
    <div class="graph-toolbar">
      <span class="graph-title">
        <v-icon size="14" class="mr-1" color="teal">mdi-graph-outline</v-icon>
        Dependency Graph
        <span v-if="nodeCount > 0" class="node-count">{{ nodeCount }} nodes · {{ edgeCount }} edges</span>
      </span>
      <div class="graph-actions">
        <button class="tool-btn" title="Fit view" @click="fit">
          <v-icon size="16">mdi-fit-to-screen-outline</v-icon>
        </button>
        <button class="tool-btn" title="Zoom in" @click="zoom(1.2)">
          <v-icon size="16">mdi-magnify-plus-outline</v-icon>
        </button>
        <button class="tool-btn" title="Zoom out" @click="zoom(0.8)">
          <v-icon size="16">mdi-magnify-minus-outline</v-icon>
        </button>
        <button class="tool-btn" title="Reload" @click="loadGraph">
          <v-icon size="16">mdi-refresh</v-icon>
        </button>
      </div>
    </div>

    <div v-if="loading" class="graph-placeholder">
      <v-progress-circular indeterminate color="teal" size="28" />
    </div>
    <div v-else-if="!graphLoaded" class="graph-placeholder">
      <v-icon size="36" color="#374151">mdi-graph-outline</v-icon>
      <span class="ph-text">No graph available yet</span>
    </div>
    <div v-else ref="cyEl" class="cy-container"></div>

    <!-- Node detail tooltip -->
    <div v-if="selectedNode" class="node-detail">
      <div class="nd-path">{{ selectedNode.path }}</div>
      <div class="nd-type">{{ selectedNode.tipo }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import { useAppStore } from '@/stores/store';
import { getGraph } from '@/services/backend';

const store = useAppStore();
const cyEl = ref<HTMLElement | null>(null);
const loading = ref(false);
const graphLoaded = ref(false);
const nodeCount = ref(0);
const edgeCount = ref(0);
const selectedNode = ref<Record<string, unknown> | null>(null);

// eslint-disable-next-line @typescript-eslint/no-explicit-any
let cy: any = null;

async function loadGraph() {
  if (!store.repoState?.repo_name) return;
  loading.value = true;
  try {
    const data = await getGraph(store.repoState.repo_name, store.language);
    store.graphData = data;
    if (data) {
      graphLoaded.value = true;
      await renderGraph(data);
    }
  } catch { /* not critical */ }
  finally { loading.value = false; }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
async function renderGraph(data: any) {
  if (!cyEl.value) return;
  // Lazy-load cytoscape
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const cytoscape = ((await import('cytoscape')) as any).default ?? (await import('cytoscape'));

  // Build elements from data
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let elements: any[] = [];
  if (Array.isArray(data.elements)) {
    elements = data.elements;
  } else if (data.nodes || data.edges) {
    const nodes = (data.nodes ?? []).map((n: Record<string, unknown>) => ({
      group: 'nodes',
      data: { id: String(n.id ?? n.path ?? ''), label: String(n.nome ?? n.label ?? n.id ?? ''), ...n },
    }));
    const edges = (data.edges ?? []).map((e: Record<string, unknown>, i: number) => ({
      group: 'edges',
      data: { id: `e${i}`, source: String(e.source ?? e.from ?? ''), target: String(e.target ?? e.to ?? '') },
    }));
    elements = [...nodes, ...edges];
  }

  nodeCount.value = elements.filter((e) => e.group === 'nodes').length;
  edgeCount.value = elements.filter((e) => e.group === 'edges').length;

  if (cy) cy.destroy();

  cy = cytoscape({
    container: cyEl.value,
    elements,
    style: [
      {
        selector: 'node',
        style: {
          'background-color': '#1f2937',
          'border-color': '#374151',
          'border-width': 1,
          'label': 'data(label)',
          'color': '#9ca3af',
          'font-size': '9px',
          'font-family': 'JetBrains Mono, monospace',
          'text-valign': 'bottom',
          'text-margin-y': 4,
          'width': 24,
          'height': 24,
        },
      },
      {
        selector: 'node[tipo="module"]',
        style: { 'background-color': '#14b8a6', 'border-color': '#0d9488', 'width': 28, 'height': 28 },
      },
      {
        selector: 'node[tipo="class"]',
        style: { 'background-color': '#6366f1', 'border-color': '#4f46e5' },
      },
      {
        selector: 'node[tipo="function"]',
        style: { 'background-color': '#374151', 'border-color': '#4b5563' },
      },
      {
        selector: 'node:selected',
        style: { 'border-color': '#f59e0b', 'border-width': 2 },
      },
      {
        selector: 'edge',
        style: {
          'line-color': '#1f2937',
          'target-arrow-color': '#374151',
          'target-arrow-shape': 'triangle',
          'curve-style': 'bezier',
          'width': 1,
          'opacity': 0.6,
        },
      },
    ],
    layout: {
      name: 'cose',
      animate: false,
      nodeRepulsion: () => 8000,
      idealEdgeLength: () => 80,
      padding: 24,
    },
  });

  cy.on('tap', 'node', (evt: { target: { data: () => Record<string, unknown> } }) => {
    selectedNode.value = evt.target.data();
  });
  cy.on('tap', (evt: { target: { group?: () => string } }) => {
    if (evt.target === cy) selectedNode.value = null;
  });
}

function fit() { cy?.fit(undefined, 20); }
function zoom(factor: number) { cy?.zoom(cy.zoom() * factor); cy?.center(); }

watch(() => store.repoState?.docs_generated, (v) => { if (v) loadGraph(); });
watch(() => store.repoState?.repo_name, () => { graphLoaded.value = false; store.graphData = null; });

onMounted(() => { if (store.repoState?.docs_generated) loadGraph(); });
onBeforeUnmount(() => { cy?.destroy(); });
</script>

<style scoped>
.graph-viewer { display: flex; flex-direction: column; height: 100%; min-height: 400px; }
.graph-toolbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 12px; background: #0d1117; border-bottom: 1px solid #1f2937; flex-shrink: 0;
}
.graph-title { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #9ca3af; font-family: 'JetBrains Mono', monospace; }
.node-count { font-size: 10px; color: #4b5563; margin-left: 8px; }
.graph-actions { display: flex; gap: 4px; }
.tool-btn {
  width: 28px; height: 28px; border-radius: 4px; border: 1px solid #374151;
  background: transparent; color: #6b7280; cursor: pointer; display: flex; align-items: center; justify-content: center;
  transition: all 0.15s;
}
.tool-btn:hover { border-color: #6b7280; color: #d1d5db; }
.cy-container { flex: 1; background: #080c12; }
.graph-placeholder { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; background: #0d1117; }
.ph-text { font-size: 12px; color: #4b5563; font-family: 'JetBrains Mono', monospace; }
.node-detail {
  padding: 8px 12px; background: #111827; border-top: 1px solid #1f2937;
  font-family: 'JetBrains Mono', monospace; flex-shrink: 0;
}
.nd-path { font-size: 11px; color: #14b8a6; }
.nd-type { font-size: 10px; color: #6b7280; margin-top: 2px; }
</style>
