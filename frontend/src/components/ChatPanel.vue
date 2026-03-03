<template>
  <div class="chat-panel">
    <div class="chat-header">
      <v-icon size="14" color="teal" class="mr-1">mdi-message-text-outline</v-icon>
      <span>Ask about the codebase</span>
      <button v-if="store.chatHistory.length > 0" class="clear-btn" @click="clear">
        <v-icon size="13">mdi-delete-outline</v-icon>
      </button>
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
</template>

<script setup lang="ts">
import { ref, computed, nextTick, watch } from 'vue';
import { useToast } from 'vue-toastification';
import { useAppStore } from '@/stores/store';
import { sendChatMessage, getChatHistory, clearChatHistory } from '@/services/backend';

const store = useAppStore();
const toast = useToast();
const question = ref('');
const messagesEl = ref<HTMLElement | null>(null);

const canChat = computed(() => !!store.repoState?.repo_name && store.llmSaved);

// Minimal markdown renderer (bold, code, newlines)
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

// Load history when repo changes
watch(() => store.repoState?.repo_name, async (name) => {
  if (!name) { store.chatHistory = []; return; }
  try {
    store.chatHistory = await getChatHistory(name);
  } catch { store.chatHistory = []; }
  scrollBottom();
});

async function send() {
  const q = question.value.trim();
  if (!q || !store.repoState?.repo_name) return;

  question.value = '';
  store.chatLoading = true;
  store.chatHistory.push({ role: 'user', content: q });
  scrollBottom();

  try {
    const res = await sendChatMessage(store.repoState.repo_name, q, store.language, store.llm);
    store.chatHistory = res.history;
  } catch (e: unknown) {
    toast.error('Chat failed: ' + String(e));
    store.chatHistory.push({ role: 'assistant', content: 'Error: ' + String(e) });
  } finally {
    store.chatLoading = false;
    scrollBottom();
  }
}

async function clear() {
  if (!store.repoState?.repo_name) return;
  try {
    await clearChatHistory(store.repoState.repo_name);
    store.chatHistory = [];
    toast.success('Chat cleared');
  } catch { toast.error('Failed to clear chat'); }
}
</script>

<style scoped>
.chat-panel { display: flex; flex-direction: column; height: 100%; gap: 0; }
.chat-header {
  display: flex; align-items: center; gap: 6px; padding: 8px 12px;
  background: #0d1117; border-bottom: 1px solid #1f2937; flex-shrink: 0;
  font-size: 12px; color: #9ca3af; font-family: 'JetBrains Mono', monospace;
}
.clear-btn {
  margin-left: auto; background: transparent; border: none; color: #4b5563;
  cursor: pointer; display: flex; align-items: center; transition: color 0.15s;
}
.clear-btn:hover { color: #f87171; }
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
