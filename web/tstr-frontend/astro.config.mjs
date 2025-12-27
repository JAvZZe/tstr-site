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
  build: {
    defaultDocumentHead: {
      children: [
        {
          tag: 'link',
          attrs: { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
        },
        {
          tag: 'link',
          attrs: { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32x32.png' }
        },
        {
          tag: 'link',
          attrs: { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }
        }
      ]
    }
  },
  vite: {
    server: {
      allowedHosts: ['.netlify.app', '.pages.dev'],
    },
  },
});
