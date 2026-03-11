<template>
  <div class="graph-viewer">
    <div class="graph-toolbar">
      <span class="graph-title">
        <v-icon size="14" class="mr-1" color="teal">mdi-graph-outline</v-icon>
        Dependency Graph
        <span v-if="totalNodes > 0" class="node-count">{{ totalNodes }} nodes · {{ totalEdges }} edges</span>
      </span>
      <button class="tool-btn" title="Reload" @click="loadGraph">
        <v-icon size="16">mdi-refresh</v-icon>
      </button>
    </div>

    <div v-if="loading" class="graph-placeholder">
      <v-progress-circular indeterminate color="teal" size="28" />
    </div>
    <div v-else-if="!groups.length" class="graph-placeholder">
      <v-icon size="36" color="#374151">mdi-graph-outline</v-icon>
      <span class="ph-text">No graph available yet</span>
    </div>

    <div v-else class="groups-scroll">
      <!-- General: all nodes -->
      <div class="group-section">
        <div class="group-header" @click="toggleGroup('__all__')">
          <v-icon size="13" class="chevron" :class="{ rotated: !expanded['__all__'] }">mdi-chevron-down</v-icon>
          <span class="group-name">General</span>
          <span class="group-meta">{{ totalNodes }} nodes · {{ totalEdges }} edges</span>
        </div>
        <div v-show="expanded['__all__']"
             :ref="(el: Element | ComponentPublicInstance | null) => setGroupEl('__all__', el)"
             class="cy-group-container"
             :style="{ height: groupHeight(totalNodes) + 'px' }">
        </div>
      </div>

      <!-- Per-folder groups -->
      <div v-for="group in groups" :key="group.name" class="group-section">
        <div class="group-header" @click="toggleGroup(group.name)">
          <v-icon size="13" class="chevron" :class="{ rotated: !expanded[group.name] }">mdi-chevron-down</v-icon>
          <span class="group-name">> {{ group.name }}</span>
          <span class="group-meta">{{ group.nodes.length }} nodes · {{ group.edges.length }} edges</span>
        </div>
        <div v-show="expanded[group.name]"
             :ref="(el: Element | ComponentPublicInstance | null) => setGroupEl(group.name, el)"
             class="cy-group-container"
             :style="{ height: groupHeight(group.nodes.length) + 'px' }">
        </div>
      </div>
    </div>

    <div v-if="selectedNode" class="node-detail">
      <div class="nd-path">{{ selectedNode.path }}</div>
      <div class="nd-type">{{ selectedNode.tipo }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onBeforeUnmount, watch, nextTick } from 'vue';
import { useTheme } from 'vuetify';
// eslint-disable-next-line @typescript-eslint/no-explicit-any
type ComponentPublicInstance = any;
import { useAppStore } from '@/stores/store';
import { getGraph } from '@/services/backend';

const store = useAppStore();
const theme = useTheme();
const loading = ref(false);
const totalNodes = ref(0);
const totalEdges = ref(0);
const selectedNode = ref<Record<string, unknown> | null>(null);

interface GraphGroup {
  name: string;
  nodes: Record<string, unknown>[];
  edges: Record<string, unknown>[];
}

const groups = ref<GraphGroup[]>([]);
const expanded = reactive<Record<string, boolean>>({});
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const cyInstances = new Map<string, any>();
const groupEls = new Map<string, HTMLElement>();

// All nodes/edges stored for the General group
let allNodes: Record<string, unknown>[] = [];
let allEdges: Record<string, unknown>[] = [];

function groupHeight(nodeCount: number): number {
  if (nodeCount <= 8)  return 280;
  if (nodeCount <= 20) return 400;
  if (nodeCount <= 50) return 540;
  if (nodeCount <= 100) return 680;
  return 820;
}

function shortLabel(n: Record<string, unknown>): string {
  // Prefer explicit name field over full path
  const name = String(n.name ?? n.nome ?? '').trim();
  if (name && name !== String(n.path ?? '')) return name;
  // Fall back to last segment of path
  const path = String(n.path ?? n.label ?? n.id ?? '').replace(/\\/g, '/');
  const segments = path.split('/').filter(Boolean);
  return segments[segments.length - 1] || path;
}

function setGroupEl(key: string, el: Element | ComponentPublicInstance | null) {
  if (el instanceof HTMLElement) {
    groupEls.set(key, el);
  } else if (el === null) {
    groupEls.delete(key);
  }
}

function buildElements(nodes: Record<string, unknown>[], edges: Record<string, unknown>[]) {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const nodeEls: any[] = nodes.map((n) => ({
    group: 'nodes',
    data: {
      id: String(n.id ?? n.path ?? ''),
      label: shortLabel(n),
      path: String(n.path ?? ''),
      tipo: String(n.tipo ?? n.kind ?? ''),
    },
  }));
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const edgeEls: any[] = edges.map((e, i) => ({
    group: 'edges',
    data: {
      id: `e${i}`,
      source: String(e.source ?? e.from ?? ''),
      target: String(e.target ?? e.to ?? ''),
    },
  }));
  return [...nodeEls, ...edgeEls];
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function cyStyle() {
  const isLight = theme.global.name.value === 'light';
  return [
    {
      selector: 'node',
      style: {
        'background-color': isLight ? '#cbd5e1' : '#1e3a4a',
        'border-color': isLight ? '#94a3b8' : '#2d6a7a',
        'border-width': 1,
        'label': 'data(label)',
        'color': isLight ? '#0f172a' : '#e2e8f0',
        'font-size': '9px',
        'font-family': 'JetBrains Mono, monospace',
        'text-valign': 'bottom',
        'text-halign': 'center',
        'text-margin-y': 4,
        'text-outline-color': isLight ? '#f1f5f9' : '#080c12',
        'text-outline-width': 2,
        'text-wrap': 'ellipsis',
        'text-max-width': '90px',
        'width': 26,
        'height': 26,
      },
    },
    {
      selector: 'node[tipo="module"]',
      style: {
        'background-color': isLight ? '#99f6e4' : '#0d4f4a',
        'border-color': isLight ? '#0d9488' : '#14b8a6',
        'border-width': 2,
        'width': 28,
        'height': 28,
        'color': isLight ? '#0f172a' : '#5eead4',
      },
    },
    {
      selector: 'node[tipo="class"]',
      style: {
        'background-color': isLight ? '#c7d2fe' : '#312e6e',
        'border-color': isLight ? '#6366f1' : '#6366f1',
        'color': isLight ? '#0f172a' : '#a5b4fc',
      },
    },
    {
      selector: 'node[tipo="function"]',
      style: {
        'background-color': isLight ? '#bbf7d0' : '#1c2f20',
        'border-color': isLight ? '#16a34a' : '#4ade80',
        'color': isLight ? '#0f172a' : '#86efac',
      },
    },
    {
      selector: 'node:selected',
      style: { 'border-color': '#f59e0b', 'border-width': 2 },
    },
    {
      selector: 'edge',
      style: {
        'line-color': isLight ? '#94a3b8' : '#4b6480',
        'target-arrow-color': isLight ? '#64748b' : '#6b8da6',
        'target-arrow-shape': 'triangle',
        'curve-style': 'bezier',
        'width': 1.5,
        'opacity': 0.75,
      },
    },
  ];
}

async function renderGroup(key: string, nodes: Record<string, unknown>[], edges: Record<string, unknown>[]) {
  const container = groupEls.get(key);
  if (!container) return;

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const cytoscape = ((await import('cytoscape')) as any).default ?? (await import('cytoscape'));

  const existing = cyInstances.get(key);
  if (existing) existing.destroy();

  const cy = cytoscape({
    container,
    elements: buildElements(nodes, edges),
    style: cyStyle(),
    layout: {
      name: 'cose',
      animate: false,
      nodeRepulsion: () => 80000,
      idealEdgeLength: () => 140,
      nodeOverlap: 24,
      gravity: 0.15,
      numIter: 1000,
      padding: 40,
      randomize: true,
      componentSpacing: 80,
    },
    wheelSensitivity: 0.2,
  });

  cy.on('tap', 'node', (evt: { target: { data: () => Record<string, unknown> } }) => {
    selectedNode.value = evt.target.data();
  });
  cy.on('tap', (evt: { target: unknown }) => {
    if (evt.target === cy) selectedNode.value = null;
  });

  cyInstances.set(key, cy);
}

async function toggleGroup(key: string) {
  expanded[key] = !expanded[key];
  if (!expanded[key]) return;
  await nextTick();
  if (cyInstances.has(key)) {
    cyInstances.get(key)?.resize();
    cyInstances.get(key)?.fit(undefined, 24);
    return;
  }
  if (key === '__all__') {
    await renderGroup('__all__', allNodes, allEdges);
  } else {
    const group = groups.value.find((g) => g.name === key);
    if (group) await renderGroup(key, group.nodes, group.edges);
  }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function buildGroups(data: any): GraphGroup[] {
  const nodes: Record<string, unknown>[] = data.nodes ?? [];
  const edges: Record<string, unknown>[] = data.edges ?? [];

  const groupMap: Record<string, Record<string, unknown>[]> = {};
  for (const n of nodes) {
    const path = String(n.path ?? '').replace(/\\/g, '/');
    const topDir = path.includes('/') ? path.split('/')[0] : 'root';
    if (!groupMap[topDir]) groupMap[topDir] = [];
    groupMap[topDir].push(n);
  }

  return Object.entries(groupMap)
    .map(([name, gnodes]) => {
      const idSet = new Set(gnodes.map((n) => n.id));
      const gedges = edges.filter((e) => idSet.has(e.from ?? e.source) && idSet.has(e.to ?? e.target));
      return { name, nodes: gnodes, edges: gedges };
    })
    .sort((a: GraphGroup, b: GraphGroup) => a.name.localeCompare(b.name));
}

async function loadGraph() {
  if (!store.repoState?.repo_name) return;
  loading.value = true;
  // destroy old instances
  cyInstances.forEach((c) => c.destroy());
  cyInstances.clear();
  groups.value = [];
  Object.keys(expanded).forEach((k) => delete expanded[k]);

  try {
    const data = await getGraph(store.repoState.repo_name, store.language);
    store.graphData = data;
    if (!data) return;

    allNodes = data.nodes ?? [];
    allEdges = data.edges ?? [];
    totalNodes.value = allNodes.length;
    totalEdges.value = allEdges.length;

    groups.value = buildGroups(data);

    // Start with General expanded, all folders collapsed
    expanded['__all__'] = true;
    groups.value.forEach((g) => { expanded[(g as GraphGroup).name] = false; });

    loading.value = false;
    await nextTick();
    await renderGroup('__all__', allNodes, allEdges);
  } catch (err) {
    console.warn('[GraphViewer] loadGraph failed:', err);
  } finally {
    loading.value = false;
  }
}

watch(() => store.repoState?.repo_name, (name: string | undefined, prev: string | undefined) => {
  if (!name) { groups.value = []; store.graphData = null; return; }
  if (name !== prev) { groups.value = []; store.graphData = null; }
  loadGraph();
});

onMounted(() => { if (store.repoState?.repo_name) loadGraph(); });
onBeforeUnmount(() => { cyInstances.forEach((c) => c.destroy()); cyInstances.clear(); });
</script>

<style scoped>
.graph-viewer { display: flex; flex-direction: column; height: 100%; overflow: hidden; }

.graph-toolbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 12px; background: #0d1117; border-bottom: 1px solid #1f2937; flex-shrink: 0;
}
.graph-title { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #9ca3af; font-family: 'JetBrains Mono', monospace; }
.node-count { font-size: 10px; color: #4b5563; margin-left: 8px; }
.tool-btn {
  width: 28px; height: 28px; border-radius: 4px; border: 1px solid #374151;
  background: transparent; color: #6b7280; cursor: pointer; display: flex; align-items: center; justify-content: center;
  transition: all 0.15s;
}
.tool-btn:hover { border-color: #6b7280; color: #d1d5db; }

.graph-placeholder { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; background: #0d1117; }
.ph-text { font-size: 12px; color: #4b5563; font-family: 'JetBrains Mono', monospace; }

.groups-scroll { flex: 1; overflow-y: auto; background: #080c12; }
.groups-scroll::-webkit-scrollbar { width: 4px; }
.groups-scroll::-webkit-scrollbar-thumb { background: #1f2937; border-radius: 2px; }

.group-section { border-bottom: 1px solid #111827; }
.group-header {
  display: flex; align-items: center; gap: 8px;
  padding: 8px 14px; cursor: pointer; user-select: none;
  background: #0a0e17;
  font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #9ca3af;
  transition: background 0.12s, color 0.12s;
}
.group-header:hover { background: #0f1623; color: #e5e7eb; }
.chevron { transition: transform 0.18s; color: #4b5563; }
.chevron.rotated { transform: rotate(-90deg); }
.group-name { flex: 1; color: #cbd5e1; }
.group-meta { font-size: 10px; color: #4b5563; }

.cy-group-container { width: 100%; background: #080c12; }

.node-detail {
  padding: 8px 12px; background: #111827; border-top: 1px solid #1f2937;
  font-family: 'JetBrains Mono', monospace; flex-shrink: 0;
}
.nd-path { font-size: 11px; color: #14b8a6; }
.nd-type { font-size: 10px; color: #6b7280; margin-top: 2px; }
</style>

<style>
.v-theme--light .graph-toolbar { background: #ffffff; border-bottom-color: #e2e8f0; }
.v-theme--light .graph-title { color: #475569; }
.v-theme--light .node-count { color: #94a3b8; }
.v-theme--light .tool-btn { border-color: #e2e8f0; color: #94a3b8; }
.v-theme--light .tool-btn:hover { border-color: #94a3b8; color: #0f172a; }
.v-theme--light .graph-placeholder { background: #f8fafc; }
.v-theme--light .ph-text { color: #94a3b8; }
.v-theme--light .groups-scroll { background: #f1f5f9; }
.v-theme--light .groups-scroll::-webkit-scrollbar-thumb { background: #cbd5e1; }
.v-theme--light .group-section { border-bottom-color: #e2e8f0; }
.v-theme--light .group-header { background: #ffffff; color: #475569; }
.v-theme--light .group-header:hover { background: #f8fafc; color: #0f172a; }
.v-theme--light .chevron { color: #94a3b8; }
.v-theme--light .group-name { color: #0f172a; }
.v-theme--light .group-meta { color: #94a3b8; }
.v-theme--light .cy-group-container { background: #f8fafc; }
.v-theme--light .node-detail { background: #f1f5f9; border-top-color: #e2e8f0; }
.v-theme--light .nd-path { color: #0f766e; }
.v-theme--light .nd-type { color: #64748b; }
</style>
