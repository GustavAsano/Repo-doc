import { defineStore } from 'pinia';
import type { LLMSettings, RepoState, ChatMessage, Language, GenerationMode, SectionDefinition, LibraryEntry } from '@/types/types';
import { PROVIDER_MODELS } from '@/types/types';

// ─── Default sections (mirrors doc_gen.py) ─────────────────────────────────

const DEFAULT_TECH_SECTIONS: Record<string, SectionDefinition & { enabled: boolean }> = {
  INDEX:          { title: 'Overview',           description: 'Describe repository purpose, target audience, and key capabilities.', enabled: true },
  GETTING_STARTED:{ title: 'Getting Started',    description: 'Quick steps to run the project for the first time.', enabled: true },
  INSTALLATION:   { title: 'Installation',       description: 'System requirements, dependencies, and detailed setup steps.', enabled: true },
  USAGE:          { title: 'Usage',              description: 'Practical usage flows, examples, and common scenarios.', enabled: true },
  ARCHITECTURE:   { title: 'Architecture',       description: 'Architecture overview, folder structure, main modules, and responsibilities.', enabled: true },
  TECHNOLOGIES:   { title: 'Technologies',       description: 'Main technologies, frameworks, libraries, and tools.', enabled: true },
  API_REFERENCE:  { title: 'API Reference',      description: 'Functions, classes, methods, and public interfaces.', enabled: true },
  CONFIGURATION:  { title: 'Configuration',      description: 'Configuration files, environment variables, and adjustable parameters.', enabled: true },
  TESTING:        { title: 'Testing',            description: 'How to run tests, available test types, and best practices.', enabled: true },
  FILE_ANALYSIS:  { title: 'File-by-File Analysis', description: 'Detailed analysis of each file with responsibilities, dependencies, and behavior.', enabled: true },
};

const DEFAULT_FUNC_SECTIONS: Record<string, SectionDefinition & { enabled: boolean }> = {
  OVERVIEW:                { title: 'Overview',                   description: 'Summarize business context, objective, and expected outcomes.', enabled: true },
  BUSINESS_SCOPE:          { title: 'Business Scope',             description: 'Define business boundaries, stakeholders, and covered domains.', enabled: true },
  FUNCTIONAL_FLOWS:        { title: 'Functional Flows',           description: 'Describe end-to-end functional flows, inputs, outputs, and decision points.', enabled: true },
  BUSINESS_RULES_EXCEPTIONS:{ title: 'Business Rules & Exceptions', description: 'List applicable business rules, validations, constraints, and exceptions.', enabled: true },
  OPERATIONAL_PROCEDURES:  { title: 'Operational Procedures',     description: 'Describe operational routines, monitoring, and support actions.', enabled: true },
};

export interface AppStore {
  // LLM config
  llm: LLMSettings;
  llmSaved: boolean;
  // Repo loading
  sourceType: 'git_url' | 'zip' | 'local_folder' | 'library';
  gitUrl: string;
  localPath: string;
  zipFile: File | null;
  zipUploadedPath: string;
  language: Language;
  generationMode: GenerationMode;
  // Library
  library: LibraryEntry[];
  functionalLibrary: LibraryEntry[];
  selectedLibraryKey: string;
  // Sections
  techSections: Record<string, SectionDefinition & { enabled: boolean }>;
  funcSections: Record<string, SectionDefinition & { enabled: boolean }>;
  // Active repo state
  repoState: RepoState | null;
  loading: boolean;
  loadingMessage: string;
  // Generation progress
  generating: boolean;
  progressEvents: Array<Record<string, unknown>>;
  progressCurrent: number;
  progressTotal: number;
  progressPhase: string;
  progressCost: number | null;
  // Docs server
  docsUrl: string;
  mkdocsPort: number | null;
  // Chat
  chatHistory: ChatMessage[];
  chatLoading: boolean;
  chatSessions: { session_id: string; title: string; updated_at: number }[];
  activeChatSessionId: string;
  // Graph
  graphData: unknown;
  // UI step
  activeTab: number;
}

export const useAppStore = defineStore('app', {
  state: (): AppStore => ({
    llm: {
      provider: 'gemini',
      model: PROVIDER_MODELS.gemini[0],
      useSystemKey: true,
      apiKey: '',
      bedrockAccessKey: '',
      bedrockSecretKey: '',
    },
    llmSaved: false,
    sourceType: 'git_url',
    gitUrl: '',
    localPath: '',
    zipFile: null,
    zipUploadedPath: '',
    language: 'EN-US',
    generationMode: 'technical_only',
    library: [],
    functionalLibrary: [],
    selectedLibraryKey: '',
    techSections: { ...DEFAULT_TECH_SECTIONS },
    funcSections: { ...DEFAULT_FUNC_SECTIONS },
    repoState: null,
    loading: false,
    loadingMessage: '',
    generating: false,
    progressEvents: [],
    progressCurrent: 0,
    progressTotal: 0,
    progressPhase: '',
    progressCost: null,
    docsUrl: '',
    mkdocsPort: null,
    chatHistory: [],
    chatLoading: false,
    chatSessions: [],
    activeChatSessionId: '',
    graphData: null,
    activeTab: 0,
  }),

  getters: {
    activeModels: (state): string[] => PROVIDER_MODELS[state.llm.provider] ?? [],
    enabledTechSections: (state) =>
      Object.fromEntries(
        Object.entries(state.techSections)
          .filter(([, v]) => v.enabled)
          .map(([k, v]) => [k, { title: v.title, description: v.description }]),
      ),
    enabledFuncSections: (state) =>
      Object.fromEntries(
        Object.entries(state.funcSections)
          .filter(([, v]) => v.enabled)
          .map(([k, v]) => [k, { title: v.title, description: v.description }]),
      ),
    hasActiveDocs: (state) => !!state.repoState?.docs_generated || !!state.repoState?.functional_docs_generated,
    repoName: (state) => state.repoState?.repo_name ?? '',
  },

  actions: {
    resetProgress() {
      this.progressEvents = [];
      this.progressCurrent = 0;
      this.progressTotal = 0;
      this.progressPhase = '';
      this.progressCost = null;
    },
    pushProgressEvent(ev: Record<string, unknown>) {
      this.progressEvents.push(ev);
      if (typeof ev.current_call === 'number') this.progressCurrent = ev.current_call;
      if (typeof ev.total_calls === 'number') this.progressTotal = ev.total_calls;
      if (typeof ev.phase === 'string') this.progressPhase = ev.phase;
      if (typeof ev.total_cost_usd === 'number') this.progressCost = ev.total_cost_usd;
    },
    resetSections() {
      this.techSections = { ...DEFAULT_TECH_SECTIONS };
      this.funcSections = { ...DEFAULT_FUNC_SECTIONS };
    },
    addSection(tab: 'tech' | 'func', key: string, title: string, description: string) {
      const target = tab === 'tech' ? this.techSections : this.funcSections;
      target[key] = { title, description, enabled: true };
    },
    removeSection(tab: 'tech' | 'func', key: string) {
      const target = tab === 'tech' ? this.techSections : this.funcSections;
      delete target[key];
    },
  },
});
