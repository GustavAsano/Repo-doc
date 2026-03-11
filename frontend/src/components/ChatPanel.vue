<template>
  <div class="chat-panel">
    <!-- Session sidebar -->
    <div class="sessions-sidebar">
      <div class="sessions-header">
        <span class="sessions-title">Chats</span>
        <button class="icon-btn" title="New chat" @click="newSession">
          <v-icon size="14">mdi-plus</v-icon>
        </button>
      </div>
      <div class="sessions-list">
        <div
          v-for="s in store.chatSessions"
          :key="s.session_id"
          class="session-item"
          :class="{ active: s.session_id === store.activeChatSessionId }"
          @click="switchSession(s.session_id)"
        >
          <span class="session-title">{{ s.title }}</span>
          <button class="del-btn" title="Delete" @click.stop="deleteSession(s.session_id)">
            <v-icon size="11">mdi-close</v-icon>
          </button>
        </div>
        <div v-if="store.chatSessions.length === 0" class="sessions-empty">No chats yet</div>
      </div>
    </div>

    <!-- Chat area -->
    <div class="chat-area">
      <div class="chat-header">
        <v-icon size="14" color="teal" class="mr-1">mdi-message-text-outline</v-icon>
        <span>{{ activeSessionTitle }}</span>
      </div>

      <div class="messages" ref="messagesEl">
        <div v-if="store.chatHistory.length === 0" class="chat-empty">
          <v-icon size="28" color="#374151">mdi-robot-outline</v-icon>
          <span>Ask anything about {{ store.repoName || 'the repository' }}</span>
        </div>
        <template v-else>
          <div
            v-for="(msg, i) in store.chatHistory"
            :key="i"
            class="message"
            :class="msg.role"
          >
            <div class="msg-role">{{ msg.role === 'user' ? 'You' : 'AI' }}</div>
            <div class="msg-content" v-html="renderMd(msg.content)"></div>
          </div>
        </template>
        <div v-if="store.chatLoading" class="message assistant">
          <div class="msg-role">AI</div>
          <div class="typing-dots"><span></span><span></span><span></span></div>
        </div>
      </div>

      <div class="chat-input-row">
        <v-text-field
          v-model="question"
          placeholder="Ask about the code…"
          density="compact"
          variant="outlined"
          hide-details
          class="dark-input flex-1"
          :disabled="!canChat || store.chatLoading"
          @keydown.enter.exact.prevent="send"
        />
        <button
          class="send-btn"
          :disabled="!canChat || !question.trim() || store.chatLoading"
          @click="send"
        >
          <v-icon size="16">mdi-send</v-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, watch } from 'vue';
import { useToast } from 'vue-toastification';
import { useAppStore } from '@/stores/store';
import { sendChatMessage, getChatHistory, deleteChatSession, listChatSessions } from '@/services/backend';

const store = useAppStore();
const toast = useToast();
const question = ref('');
const messagesEl = ref<HTMLElement | null>(null);

const canChat = computed(() => !!store.repoState?.repo_name && store.llmSaved);

const activeSessionTitle = computed(() => {
  const s = store.chatSessions.find(s => s.session_id === store.activeChatSessionId);
  return s?.title ?? 'Ask about the codebase';
});

function renderMd(text: string): string {
  return text
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/```[\w]*\n?([\s\S]*?)```/g, '<pre class="code-block">$1</pre>')
    .replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>');
}

async function scrollBottom() {
  await nextTick();
  if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight;
}

watch(() => store.chatHistory.length, scrollBottom);

async function loadSessions(repoName: string) {
  try {
    store.chatSessions = await listChatSessions(repoName);
  } catch {
    store.chatSessions = [];
  }
}

async function loadHistory(sessionId: string) {
  const repo = store.repoState?.repo_name;
  if (!repo) return;
  try {
    store.chatHistory = await getChatHistory(repo, sessionId === '__default__' ? undefined : sessionId);
  } catch {
    store.chatHistory = [];
  }
  scrollBottom();
}

watch(() => store.repoState?.repo_name, async (name) => {
  store.chatHistory = [];
  store.chatSessions = [];
  store.activeChatSessionId = '';
  if (!name) return;
  await loadSessions(name);
  if (store.chatSessions.length > 0) {
    store.activeChatSessionId = store.chatSessions[0].session_id;
    await loadHistory(store.activeChatSessionId);
  }
});

function newSession() {
  const id = crypto.randomUUID();
  store.activeChatSessionId = id;
  store.chatHistory = [];
  // Don't persist empty session — it will be saved on first message
}

async function switchSession(sessionId: string) {
  if (sessionId === store.activeChatSessionId) return;
  store.activeChatSessionId = sessionId;
  await loadHistory(sessionId);
}

async function deleteSession(sessionId: string) {
  const repo = store.repoState?.repo_name;
  if (!repo) return;
  try {
    await deleteChatSession(repo, sessionId === '__default__' ? undefined : sessionId);
    store.chatSessions = store.chatSessions.filter(s => s.session_id !== sessionId);
    if (store.activeChatSessionId === sessionId) {
      if (store.chatSessions.length > 0) {
        store.activeChatSessionId = store.chatSessions[0].session_id;
        await loadHistory(store.activeChatSessionId);
      } else {
        store.activeChatSessionId = '';
        store.chatHistory = [];
      }
    }
  } catch {
    toast.error('Failed to delete chat');
  }
}

async function send() {
  const q = question.value.trim();
  if (!q || !store.repoState?.repo_name) return;

  // Create a new session ID if none active
  if (!store.activeChatSessionId) {
    store.activeChatSessionId = crypto.randomUUID();
  }

  question.value = '';
  store.chatLoading = true;
  store.chatHistory.push({ role: 'user', content: q });
  scrollBottom();

  const sessionId = store.activeChatSessionId;
  try {
    const res = await sendChatMessage(
      store.repoState.repo_name,
      q,
      store.language,
      store.llm,
      sessionId === '__default__' ? undefined : sessionId,
    );
    store.chatHistory = res.history;
    // Refresh session list to pick up new title / new session entry
    await loadSessions(store.repoState.repo_name);
    // If this was a brand new session not yet in the list, ensure it's selected
    if (!store.chatSessions.find(s => s.session_id === sessionId)) {
      await loadSessions(store.repoState.repo_name);
    }
  } catch (e: unknown) {
    toast.error('Chat failed: ' + String(e));
    store.chatHistory.push({ role: 'assistant', content: 'Error: ' + String(e) });
  } finally {
    store.chatLoading = false;
    scrollBottom();
  }
}
</script>

<style scoped>
.chat-panel { display: flex; height: 100%; overflow: hidden; }

/* Session sidebar */
.sessions-sidebar {
  width: 180px; flex-shrink: 0;
  background: #0d1117; border-right: 1px solid #1f2937;
  display: flex; flex-direction: column; overflow: hidden;
}
.sessions-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 10px; border-bottom: 1px solid #1f2937; flex-shrink: 0;
}
.sessions-title { font-size: 10px; color: #4b5563; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; letter-spacing: 0.08em; }
.icon-btn {
  background: transparent; border: 1px solid #374151; color: #6b7280;
  border-radius: 4px; width: 20px; height: 20px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: all 0.15s;
}
.icon-btn:hover { border-color: #14b8a6; color: #14b8a6; }
.sessions-list { flex: 1; overflow-y: auto; padding: 6px; display: flex; flex-direction: column; gap: 2px; }
.session-item {
  display: flex; align-items: center; gap: 4px;
  padding: 6px 8px; border-radius: 5px; cursor: pointer;
  border: 1px solid transparent; transition: all 0.15s;
}
.session-item:hover { background: #1f2937; border-color: #374151; }
.session-item.active { background: rgba(20,184,166,0.08); border-color: rgba(20,184,166,0.3); }
.session-title {
  flex: 1; font-size: 11px; color: #9ca3af; font-family: 'JetBrains Mono', monospace;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.session-item.active .session-title { color: #14b8a6; }
.del-btn {
  flex-shrink: 0; background: transparent; border: none; color: #374151;
  cursor: pointer; display: flex; align-items: center; padding: 1px;
  border-radius: 3px; transition: color 0.15s; opacity: 0;
}
.session-item:hover .del-btn { opacity: 1; }
.del-btn:hover { color: #f87171; }
.sessions-empty { font-size: 10px; color: #374151; font-family: 'JetBrains Mono', monospace; padding: 10px 8px; }

/* Chat area */
.chat-area { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
.chat-header {
  display: flex; align-items: center; gap: 6px; padding: 8px 12px;
  background: #0d1117; border-bottom: 1px solid #1f2937; flex-shrink: 0;
  font-size: 12px; color: #9ca3af; font-family: 'JetBrains Mono', monospace;
}
.messages { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 14px; background: #080c12; }
.chat-empty { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; color: #4b5563; font-size: 12px; font-family: 'JetBrains Mono', monospace; }
.message { display: flex; flex-direction: column; gap: 4px; max-width: 85%; }
.message.user { align-self: flex-end; }
.message.assistant { align-self: flex-start; }
.msg-role { font-size: 10px; font-family: 'JetBrains Mono', monospace; color: #4b5563; }
.message.user .msg-role { text-align: right; color: #14b8a6; }
.msg-content {
  font-size: 13px; color: #d1d5db; line-height: 1.6;
  background: #111827; border-radius: 8px; padding: 10px 14px;
  border: 1px solid #1f2937;
}
.message.user .msg-content { background: rgba(20,184,166,0.1); border-color: rgba(20,184,166,0.2); color: #e5e7eb; }
:deep(.code-block) { background: #0d1117; border: 1px solid #374151; border-radius: 4px; padding: 10px; font-family: 'JetBrains Mono', monospace; font-size: 11px; overflow-x: auto; color: #9ca3af; white-space: pre; }
:deep(.inline-code) { background: #1f2937; border-radius: 3px; padding: 1px 5px; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #14b8a6; }
.typing-dots { display: flex; gap: 4px; padding: 8px 12px; background: #111827; border-radius: 8px; border: 1px solid #1f2937; }
.typing-dots span { width: 6px; height: 6px; border-radius: 50%; background: #4b5563; animation: bounce 1.2s infinite; }
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-4px); } }
.chat-input-row { display: flex; gap: 8px; padding: 10px 12px; background: #0d1117; border-top: 1px solid #1f2937; flex-shrink: 0; }
.send-btn {
  width: 36px; height: 36px; border-radius: 6px; border: 1px solid #374151;
  background: transparent; color: #6b7280; cursor: pointer;
  display: flex; align-items: center; justify-content: center; transition: all 0.15s; flex-shrink: 0;
}
.send-btn:hover:not(:disabled) { border-color: #14b8a6; color: #14b8a6; }
.send-btn:disabled { opacity: 0.4; cursor: not-allowed; }
</style>

<style>
.v-theme--light .sessions-sidebar { background: #ffffff; border-right-color: #e2e8f0; }
.v-theme--light .sessions-header { border-bottom-color: #e2e8f0; }
.v-theme--light .sessions-title { color: #94a3b8; }
.v-theme--light .icon-btn { border-color: #e2e8f0; color: #94a3b8; }
.v-theme--light .icon-btn:hover { border-color: #0f766e; color: #0f766e; }
.v-theme--light .session-item:hover { background: #f1f5f9; border-color: #e2e8f0; }
.v-theme--light .session-item.active { background: rgba(15,118,110,0.06); border-color: rgba(15,118,110,0.3); }
.v-theme--light .session-title { color: #475569; }
.v-theme--light .session-item.active .session-title { color: #0f766e; }
.v-theme--light .del-btn { color: #cbd5e1; }
.v-theme--light .sessions-empty { color: #cbd5e1; }
.v-theme--light .chat-header { background: #ffffff; border-bottom-color: #e2e8f0; color: #475569; }
.v-theme--light .messages { background: #f1f5f9; }
.v-theme--light .chat-empty { color: #94a3b8; }
.v-theme--light .msg-role { color: #94a3b8; }
.v-theme--light .message.user .msg-role { color: #0f766e; }
.v-theme--light .msg-content { background: #ffffff; border-color: #e2e8f0; color: #0f172a; }
.v-theme--light .message.user .msg-content { background: rgba(15,118,110,0.07); border-color: rgba(15,118,110,0.2); color: #0f172a; }
.v-theme--light :deep(.code-block) { background: #f1f5f9; border-color: #e2e8f0; color: #475569; }
.v-theme--light :deep(.inline-code) { background: #e2e8f0; color: #0f766e; }
.v-theme--light .typing-dots { background: #ffffff; border-color: #e2e8f0; }
.v-theme--light .typing-dots span { background: #cbd5e1; }
.v-theme--light .chat-input-row { background: #ffffff; border-top-color: #e2e8f0; }
.v-theme--light .send-btn { border-color: #e2e8f0; color: #94a3b8; }
.v-theme--light .send-btn:hover:not(:disabled) { border-color: #0f766e; color: #0f766e; }
</style>
