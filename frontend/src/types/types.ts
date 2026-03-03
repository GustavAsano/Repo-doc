// ─── LLM ───────────────────────────────────────────────────────────────────

export type LLMProvider = 'gemini' | 'openai' | 'bedrock';

export interface LLMSettings {
  provider: LLMProvider;
  model: string;
  useSystemKey: boolean;
  apiKey?: string;
  bedrockAccessKey?: string;
  bedrockSecretKey?: string;
}

export const PROVIDER_MODELS: Record<LLMProvider, string[]> = {
  gemini: ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-2.0-flash', 'gemini-2.0-pro'],
  openai: ['gpt-4o', 'gpt-4o-mini', 'gpt-5-mini', 'gpt-5-nano'],
  bedrock: [
    'anthropic.claude-3-5-sonnet-20241022-v2:0',
    'anthropic.claude-3-5-haiku-20241022-v1:0',
    'anthropic.claude-haiku-4-5-20251001-v1:0',
    'moonshot.kimi-k2-thinking',
  ],
};

// ─── Repository ────────────────────────────────────────────────────────────

export type SourceType = 'git_url' | 'zip' | 'local_folder';
export type GenerationMode = 'technical_only' | 'technical_and_functional' | 'functional_only';
export type Language = 'PT-BR' | 'EN-US' | 'ES-ES' | 'FR-FR' | 'DE-DE';

export const LANGUAGES: { value: Language; label: string }[] = [
  { value: 'PT-BR', label: 'Português (BR)' },
  { value: 'EN-US', label: 'English (US)' },
  { value: 'ES-ES', label: 'Español' },
  { value: 'FR-FR', label: 'Français' },
  { value: 'DE-DE', label: 'Deutsch' },
];

export interface SectionDefinition {
  title: string;
  description: string;
  enabled?: boolean;
}

export interface LibraryEntry {
  repo_name: string;
  language: Language;
  entry_key: string;
  updated_at?: string;
  docs_available: boolean;
  functional_docs_available: boolean;
  repo_url?: string;
  source_type?: string;
}

export interface RepoState {
  repo_name: string;
  repo_path?: string;
  owner?: string;
  language: Language;
  output_dir?: string;
  graph_path?: string;
  docs_generated: boolean;
  functional_docs_generated: boolean;
  docs_skipped: boolean;
  doc_variant: 'technical' | 'functional';
  generation_mode: GenerationMode;
  mkdocs_port?: number;
  library_entry_key?: string;
  result?: Record<string, unknown>;
}

// ─── Progress ──────────────────────────────────────────────────────────────

export type ProgressEventType = 'plan' | 'call_start' | 'call_end' | 'done' | 'error';

export interface ProgressEvent {
  event: ProgressEventType;
  phase?: string;
  current_call?: number;
  total_calls?: number;
  message?: string;
  is_multi_pass?: boolean;
  cost_available?: boolean;
  total_cost_usd?: number;
  call_cost_usd?: number;
  result?: RepoState;
}

// ─── Chat ──────────────────────────────────────────────────────────────────

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

// ─── Graph ─────────────────────────────────────────────────────────────────

export interface GraphNode {
  id: string;
  label?: string;
  tipo?: string;
  path?: string;
  [key: string]: unknown;
}

export interface GraphEdge {
  source: string;
  target: string;
  type?: string;
  [key: string]: unknown;
}

export interface GraphData {
  nodes?: GraphNode[];
  edges?: GraphEdge[];
  elements?: unknown;
  [key: string]: unknown;
}

// ─── App Steps ─────────────────────────────────────────────────────────────

export type AppStep = 'setup' | 'load' | 'generate' | 'view';
