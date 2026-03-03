// services/backend.ts
import constants from '@/utils/const';
import axios from 'axios';
import type { LLMSettings, SectionDefinition, Language, GenerationMode, LibraryEntry, RepoState, ChatMessage } from '@/types/types';

// ─── URL builder ───────────────────────────────────────────────────────────

const getEndpoint = (path: string): string => {
  let base = constants.backendHost ?? '';
  if (!base) base = window.location.protocol + '//' + window.location.hostname;
  if (constants.backendPort) base += ':' + constants.backendPort;
  else base += ':' + window.location.port;
  base += constants.backendBase ?? '';
  return base + path;
};

const headers = () => ({
  Authorization: 'Bearer ' + (constants.apiKey ?? ''),
});

// ─── LLM ───────────────────────────────────────────────────────────────────

export const saveLLMSettings = async (settings: LLMSettings) => {
  const { data } = await axios.post(getEndpoint('/llm/settings'), {
    provider: settings.provider,
    model: settings.model,
    use_system_key: settings.useSystemKey,
    api_key: settings.apiKey ?? null,
    bedrock_access_key: settings.bedrockAccessKey ?? null,
    bedrock_secret_key: settings.bedrockSecretKey ?? null,
  }, { headers: headers() });
  return data;
};

export const getLLMSettings = async () => {
  const { data } = await axios.get(getEndpoint('/llm/settings'), { headers: headers() });
  return data;
};

// ─── Repo loading ──────────────────────────────────────────────────────────

export const loadRepoFromUrl = async (source: string, language: Language): Promise<RepoState> => {
  const fd = new FormData();
  fd.append('source', source);
  fd.append('source_type', 'git_url');
  fd.append('language', language);
  const { data } = await axios.post(getEndpoint('/repo/load'), fd, { headers: headers() });
  return data;
};

export const uploadZip = async (file: File): Promise<{ filename: string; path: string }> => {
  const fd = new FormData();
  fd.append('file', file);
  const { data } = await axios.post(getEndpoint('/repo/upload'), fd, { headers: headers() });
  return data;
};

export const loadRepoFromZip = async (path: string, language: Language): Promise<RepoState> => {
  const fd = new FormData();
  fd.append('source', path);
  fd.append('source_type', 'zip');
  fd.append('language', language);
  const { data } = await axios.post(getEndpoint('/repo/load'), fd, { headers: headers() });
  return data;
};

export const loadRepoFromFolder = async (path: string, language: Language): Promise<RepoState> => {
  const fd = new FormData();
  fd.append('source', path);
  fd.append('source_type', 'local_folder');
  fd.append('language', language);
  const { data } = await axios.post(getEndpoint('/repo/load'), fd, { headers: headers() });
  return data;
};

// ─── Library ───────────────────────────────────────────────────────────────

export const getLibrary = async (kind: 'technical' | 'functional' = 'technical'): Promise<LibraryEntry[]> => {
  const { data } = await axios.get(getEndpoint('/repo/library'), { params: { kind }, headers: headers() });
  return data.entries ?? [];
};

export const deleteLibraryEntry = async (entryKey: string, kind: 'technical' | 'functional' = 'technical') => {
  const { data } = await axios.delete(getEndpoint(`/repo/library/${encodeURIComponent(entryKey)}`), {
    params: { kind },
    headers: headers(),
  });
  return data;
};

export const activateLibraryEntry = async (
  entryKey: string,
  docVariant: 'technical' | 'functional' = 'technical',
  startMkdocs: boolean = true,
): Promise<RepoState> => {
  const fd = new FormData();
  fd.append('entry_key', entryKey);
  fd.append('doc_variant', docVariant);
  fd.append('start_mkdocs', startMkdocs ? 'true' : 'false');
  const { data } = await axios.post(getEndpoint('/repo/activate'), fd, { headers: headers() });
  return data;
};

// ─── Documentation generation (SSE) ───────────────────────────────────────

export const generateDocs = (
  payload: {
    repo_name: string;
    language: Language;
    generation_mode: GenerationMode;
    provider: string;
    model: string;
    use_system_key: boolean;
    api_key?: string;
    documentation_sections?: Record<string, SectionDefinition>;
    functional_sections?: Record<string, SectionDefinition>;
  },
  onEvent: (ev: Record<string, unknown>) => void,
  onDone: () => void,
  onError: (msg: string) => void,
): AbortController => {
  const ctrl = new AbortController();

  const doFetch = async () => {
    let response: Response;
    try {
      response = await fetch(getEndpoint('/docs/generate'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + (constants.apiKey ?? ''),
        },
        body: JSON.stringify(payload),
        signal: ctrl.signal,
      });
    } catch (e: unknown) {
      if ((e as Error).name !== 'AbortError') onError(String(e));
      return;
    }

    if (!response.ok) {
      onError(`HTTP ${response.status}`);
      return;
    }

    const reader = response.body!.getReader();
    const decoder = new TextDecoder();
    let buf = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      const lines = buf.split('\n');
      buf = lines.pop() ?? '';
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const ev = JSON.parse(line.slice(6));
            onEvent(ev);
            if (ev.event === 'done') { onDone(); return; }
            if (ev.event === 'error') { onError(ev.message ?? 'Generation error'); return; }
          } catch { /* ignore malformed */ }
        }
      }
    }
    onDone();
  };

  doFetch();
  return ctrl;
};

// ─── Docs server ───────────────────────────────────────────────────────────

export const getDocsServer = async (): Promise<{ port: number; docs_url: string; entry_html: string }> => {
  const { data } = await axios.get(getEndpoint('/docs/server'), { headers: headers() });
  return data;
};

// ─── Export ────────────────────────────────────────────────────────────────

export const exportDoc = async (
  repoName: string,
  format: 'pdf' | 'docx',
  language: Language,
  docVariant: 'technical' | 'functional' = 'technical',
): Promise<{ filename: string; data: string }> => {
  const { data } = await axios.get(getEndpoint(`/export/${format}/${encodeURIComponent(repoName)}`), {
    params: { language, doc_variant: docVariant },
    headers: headers(),
  });
  return data;
};

// ─── Chat ──────────────────────────────────────────────────────────────────

export const sendChatMessage = async (
  repoName: string,
  question: string,
  language: Language,
  settings: LLMSettings,
): Promise<{ answer: string; history: ChatMessage[] }> => {
  const { data } = await axios.post(
    getEndpoint('/chat/message'),
    {
      repo_name: repoName,
      question,
      language,
      provider: settings.provider,
      model: settings.model,
      use_system_key: settings.useSystemKey,
      api_key: settings.apiKey ?? null,
    },
    { headers: headers() },
  );
  return data;
};

export const getChatHistory = async (repoName: string): Promise<ChatMessage[]> => {
  const { data } = await axios.get(getEndpoint(`/chat/history/${encodeURIComponent(repoName)}`), {
    headers: headers(),
  });
  return data.history ?? [];
};

export const clearChatHistory = async (repoName: string) => {
  const { data } = await axios.delete(getEndpoint(`/chat/history/${encodeURIComponent(repoName)}`), {
    headers: headers(),
  });
  return data;
};

// ─── Graph ─────────────────────────────────────────────────────────────────

export const getGraph = async (repoName: string, language: Language) => {
  const { data } = await axios.get(getEndpoint(`/graph/${encodeURIComponent(repoName)}`), {
    params: { language },
    headers: headers(),
  });
  return data.graph ?? null;
};
