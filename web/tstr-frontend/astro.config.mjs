// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import cloudflare from '@astrojs/cloudflare';

// https://astro.build/config
export default defineConfig({
  output: 'server', // Enable SSR (all pages server-rendered)
  adapter: cloudflare(), // Cloudflare Pages adapter for SSR
  integrations: [react(), tailwind()],
  vite: {
    server: {
      allowedHosts: ['.netlify.app', '.pages.dev'],
    },
  },
});
