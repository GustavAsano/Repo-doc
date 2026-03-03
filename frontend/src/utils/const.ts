/// <reference types="vite/client" />

interface ImportMetaEnv {
  VITE_APP_BACKEND_HOST: string;
  VITE_APP_BACKEND_PORT: string;
  VITE_APP_API_KEY: string;
  VITE_APP_BACKEND_API_BASE: string;
}

export interface ImportMeta {
  readonly env: ImportMetaEnv;
}

const constants = {
  backendHost: import.meta.env.VITE_APP_BACKEND_HOST,
  backendPort: import.meta.env.VITE_APP_BACKEND_PORT,
  apiKey: import.meta.env.VITE_APP_API_KEY,
  backendBase: import.meta.env.VITE_APP_BACKEND_API_BASE,
};

export default constants;
