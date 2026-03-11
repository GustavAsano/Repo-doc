import AutoImport from "unplugin-auto-import/vite";
import Components from "unplugin-vue-components/vite";
import Fonts from "unplugin-fonts/vite";
import Vue from "@vitejs/plugin-vue";
import Vuetify, { transformAssetUrls } from "vite-plugin-vuetify";
import { defineConfig } from "vite";
import { fileURLToPath, URL } from "node:url";

export default defineConfig({
  plugins: [
    AutoImport({
      imports: ["vue"],
      dts: "src/auto-imports.d.ts",
      eslintrc: { enabled: true },
      vueTemplate: true,
    }),
    Components({ dts: "src/components.d.ts" }),
    Vue({ template: { transformAssetUrls } }),
    Vuetify({
      autoImport: true,
      styles: { configFile: "src/styles/settings.scss" },
    }),
    Fonts({
      google: {
        families: [
          { name: "Syne", styles: "wght@700;800" },
          { name: "JetBrains+Mono", styles: "wght@400;500;600" },
        ],
      },
    }),
  ],
  define: { "process.env": {} },
  resolve: {
    alias: { "@": fileURLToPath(new URL("./src", import.meta.url)) },
    extensions: [".js", ".json", ".jsx", ".mjs", ".ts", ".tsx", ".vue"],
  },
  server: {
    port: 3000,
    proxy: {
      "/llm":    { target: "http://repo-doc-backend:8000", changeOrigin: true },
      "/repo":   { target: "http://repo-doc-backend:8000", changeOrigin: true },
      "/docs":   { target: "http://repo-doc-backend:8000", changeOrigin: true },
      "/export": { target: "http://repo-doc-backend:8000", changeOrigin: true },
      "/chat":   { target: "http://repo-doc-backend:8000", changeOrigin: true },
      "/graph":  { target: "http://repo-doc-backend:8000", changeOrigin: true },
      "/health": { target: "http://repo-doc-backend:8000", changeOrigin: true },
    },
  },
});
