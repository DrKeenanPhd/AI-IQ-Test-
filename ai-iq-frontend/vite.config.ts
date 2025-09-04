import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: false,
    allowedHosts: [
      'ai-iq-test-app-tunnel-uhi1ata3.devinapps.com',
      'ai-iq-test-app-tunnel-x21qruff.devinapps.com', 
      'ai-iq-test-app-tunnel-s7hqw0gp.devinapps.com',
      '.devinapps.com'
    ],
    hmr: {
      clientPort: 443
    }
  },
})

