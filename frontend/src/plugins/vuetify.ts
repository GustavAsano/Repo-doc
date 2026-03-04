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
    },
  },
});
