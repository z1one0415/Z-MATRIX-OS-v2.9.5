import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

const backendHost = process.env.ZMATRIX_BACKEND_HOST || process.env.Z_MATRIX_PRODUCT_HOST || "127.0.0.1";
const backendPort = process.env.ZMATRIX_BACKEND_PORT || process.env.Z_MATRIX_PRODUCT_PORT || "8765";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: `http://${backendHost}:${backendPort}`,
        changeOrigin: true
      }
    }
  },
  test: {
    environment: "jsdom",
    setupFiles: "./src/testSetup.ts",
    globals: true
  }
});
