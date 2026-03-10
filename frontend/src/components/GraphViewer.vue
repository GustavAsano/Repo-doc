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
import type { ComponentPublicInstance } from 'vue';
import { useAppStore } from '@/stores/store';
import { getGraph } from '@/services/backend';

const store = useAppStore();
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
  if (nodeCount <= 10) return 260;
  if (nodeCount <= 30) return 360;
  if (nodeCount <= 80) return 460;
  return 560;
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
      label: String(n.name ?? n.nome ?? n.label ?? n.path ?? n.id ?? ''),
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
  return [
    {
      selector: 'node',
      style: {
        'background-color': '#1e3a4a',
        'border-color': '#2d6a7a',
        'border-width': 1,
        'label': 'data(label)',
        'color': '#e2e8f0',
        'font-size': '10px',
        'font-family': 'JetBrains Mono, monospace',
        'text-valign': 'bottom',
        'text-margin-y': 5,
        'text-outline-color': '#080c12',
        'text-outline-width': 2,
        'width': 22,
        'height': 22,
      },
    },
    {
      selector: 'node[tipo="module"]',
      style: {
        'background-color': '#0d4f4a',
        'border-color': '#14b8a6',
        'border-width': 2,
        'width': 28,
        'height': 28,
        'color': '#5eead4',
      },
    },
    {
      selector: 'node[tipo="class"]',
      style: {
        'background-color': '#312e6e',
        'border-color': '#6366f1',
        'color': '#a5b4fc',
      },
    },
    {
      selector: 'node[tipo="function"]',
      style: {
        'background-color': '#1c2f20',
        'border-color': '#4ade80',
        'color': '#86efac',
      },
    },
    {
      selector: 'node:selected',
      style: { 'border-color': '#f59e0b', 'border-width': 2 },
    },
    {
      selector: 'edge',
      style: {
        'line-color': '#4b6480',
        'target-arrow-color': '#6b8da6',
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
      nodeRepulsion: () => 10000,
      idealEdgeLength: () => 90,
      padding: 28,
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
    groups.value.forEach((g: GraphGroup) => { expanded[g.name] = false; });

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
