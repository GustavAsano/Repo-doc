import '@mdi/font/css/materialdesignicons.css';
import 'vuetify/styles';
import { createVuetify } from 'vuetify';

export default createVuetify({
  theme: {
    defaultTheme: 'dark',
    themes: {
      dark: {
        dark: true,  // ← critical: tells Vuetify this is actually a dark theme
        colors: {
          primary: '#14b8a6',
          surface: '#0d1117',      // ← fixes dropdown/menu background
          background: '#080c12',
          'on-surface': '#e5e7eb', // ← fixes text on dropdowns
          'on-background': '#e5e7eb',
        },
      },
    },
  },
});