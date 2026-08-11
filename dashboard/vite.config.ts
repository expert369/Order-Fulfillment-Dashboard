import path from 'path';
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import proxyOptions from './proxyOptions.ts';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 8080,
    host: '0.0.0.0',
    proxy: proxyOptions,
  },
  resolve: {
    alias: { '@': path.resolve(__dirname, 'src') },
  },
  build: {
    outDir: '../order_fulfillment_dashboard/public/order_fulfillment',
    emptyOutDir: true,
    target: 'es2015',
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
    css: false,
    include: ['src/**/*.{test,spec}.{ts,tsx}'],
  },
});