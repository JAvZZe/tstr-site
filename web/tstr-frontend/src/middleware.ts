// src/middleware.ts
// Self-hosted "Markdown for Agents" (mirrors Cloudflare's paid edge feature, $0 on our
// free Cloudflare Pages plan). Runs inside the SSR Worker. For AI agents that request
// `Accept: text/markdown`, the HTML response is converted to Markdown (frontmatter from
// <meta> + appended JSON-LD) and returned with content-type: text/markdown.
//
// See https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/
import { defineMiddleware } from 'astro:middleware';
import { htmlToMarkdownForAgents, CONTENT_SIGNAL } from './lib/markdown-for-agents';

// Paths that are not public content (auth, dashboards, API, checkout, health) or that
// serve non-HTML (assets, sitemaps, llms.txt, robots). Agents hitting these get raw HTML.
const EXCLUDED_PREFIXES = [
  '/account',
  '/admin',
  '/api',
  '/checkout',
  '/login',
  '/signup',
  '/_',
  '/favicon',
  '/robots',
];

function isExcluded(pathname: string): boolean {
  const p = pathname.toLowerCase();
  if (p === '/llms.txt' || p === '/sitemap.xml' || p === '/sitemap-index.xml') return true;
  return EXCLUDED_PREFIXES.some((prefix) => p.startsWith(prefix));
}

function wantsMarkdown(accept: string | null): boolean {
  if (!accept) return false;
  // Cloudflare honors `text/markdown` appearing anywhere in the Accept list.
  return accept.toLowerCase().includes('text/markdown');
}

export const onRequest = defineMiddleware(async (context, next) => {
  const { request, url } = context;

  // Only intercept GET HTML page requests that explicitly ask for markdown.
  const isGet = request.method === 'GET';
  if (!isGet || isExcluded(url.pathname) || !wantsMarkdown(request.headers.get('accept'))) {
    return next();
  }

  const response = await next();

  // Only transform successful HTML responses.
  const contentType = response.headers.get('content-type') ?? '';
  if (!response.ok || !contentType.includes('text/html')) {
    return response;
  }

  try {
    const html = await response.text();
    const { markdown, originalTokens } = htmlToMarkdownForAgents({ html, url: url.toString() });
    const markdownTokens = Math.max(1, Math.round(markdown.length / 4));

    const headers = new Headers(response.headers);
    headers.set('content-type', 'text/markdown; charset=utf-8');
    headers.set('vary', 'accept');
    headers.set('x-markdown-tokens', String(markdownTokens));
    headers.set('x-original-tokens', String(originalTokens));
    // Authoritative content-signal policy (overrides Cloudflare's default once set at origin).
    headers.set('content-signal', CONTENT_SIGNAL);
    // Body is replaced; drop body-specific headers that no longer match.
    headers.delete('content-encoding');
    headers.delete('content-length');
    headers.delete('etag');
    headers.delete('last-modified');

    return new Response(markdown, {
      status: response.status,
      statusText: response.statusText,
      headers,
    });
  } catch (err) {
    // Conversion failed: fall back to the original HTML response.
    console.error('[markdown-for-agents] conversion failed, serving HTML:', err);
    return response;
  }
});
