/**
 * plugins/index.ts
 *
 * Automatically included in `./src/main.ts`
 */

// Plugins
import vuetify from '@/plugins/vuetify';
import pinia from '@/stores';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';

// Types
import type { App } from 'vue';

export function registerPlugins(app: App) {
  app.use(vuetify).use(pinia).use(Toast);
}
