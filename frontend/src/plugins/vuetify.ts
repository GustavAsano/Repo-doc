import '@mdi/font/css/materialdesignicons.css';
import 'vuetify/styles';
import { createVuetify } from 'vuetify';

export default createVuetify({
  theme: {
    defaultTheme: 'dark',
    themes: {
      dark: {
        dark: true,
        colors: {
          primary: '#14b8a6',
          secondary: '#1E1E1E',
          surface: '#0d1117',
          background: '#080c12',
          'on-surface': '#e5e7eb',
          'on-background': '#e5e7eb',
        },
      },
      light: {
        dark: false,
        colors: {
          primary: '#0f766e',
          secondary: '#e2e8f0',
          surface: '#ffffff',
          background: '#f1f5f9',
          'on-surface': '#0f172a',
          'on-background': '#0f172a',
        },
      },
    },
  },
});
