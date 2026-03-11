<template>
  <v-app>
    <v-layout class="rounded rounded-md">
      <Header />
      <Main />
    </v-layout>
  </v-app>
</template>

<style>
body {
  font-family: 'Montserrat', sans-serif;
}
html {
  overflow-y: auto;
}

/* ── Light mode overrides ─────────────────────────────────────────── */
.v-theme--light .app-main             { background: #f1f5f9 !important; }
.v-theme--light .layout               { background: #f1f5f9; }
.v-theme--light .sidebar              { background: #ffffff; border-right-color: #e2e8f0; }
.v-theme--light .sidebar-scroll::-webkit-scrollbar-thumb { background: #cbd5e1; }
.v-theme--light .side-section         { border-bottom-color: #e2e8f0; }
.v-theme--light .side-title           { color: #334155; }
.v-theme--light .side-title:hover     { color: #0f172a; }
.v-theme--light .content              { background: #f1f5f9; }
.v-theme--light .content-tabs         { background: #ffffff; border-bottom-color: #e2e8f0; }
.v-theme--light .c-tab                { color: #64748b; }
.v-theme--light .c-tab:hover          { color: #1e293b; }
.v-theme--light .c-tab.active         { color: #0f766e; border-bottom-color: #0f766e; }
.v-theme--light .welcome-glyph        { color: #cbd5e1; }
.v-theme--light .welcome-h1           { color: #0f172a; }
.v-theme--light .welcome-sub          { color: #475569; }
.v-theme--light .w-step               { background: #ffffff; border-color: #e2e8f0; color: #475569; }
.v-theme--light .w-step.done          { border-color: rgba(15,118,110,0.3); color: #1e293b; }
.v-theme--light .step-num             { background: #e2e8f0; color: #64748b; }
.v-theme--light .w-step.done .step-num { background: rgba(15,118,110,0.1); color: #0f766e; }
.v-theme--light .generate-title       { color: #0f172a; }
.v-theme--light .generate-sub         { color: #475569; }
.v-theme--light .run-status-badge     { background: #ffffff; border-color: #e2e8f0; }
.v-theme--light .run-status-badge.status-running { border-color: rgba(15,118,110,0.4); background: rgba(15,118,110,0.06); }
.v-theme--light .run-status-badge.status-done    { border-color: rgba(16,185,129,0.4); background: rgba(16,185,129,0.06); }
.v-theme--light .run-status-dot       { background: #cbd5e1; }
.v-theme--light .run-status-label     { color: #475569; }
.v-theme--light .run-status-phase     { color: #64748b; }
.v-theme--light .run-status-calls     { color: #64748b; }
</style>
