// src/lib/markdown-for-agents.ts
// Self-hosted "Markdown for Agents" — mirrors Cloudflare's paid edge feature at $0
// on our free Cloudflare Pages plan (SSR => single Pages Worker; this runs inside it).
//
// Behavior mirrors developers.cloudflare.com/fundamentals/reference/markdown-for-agents/:
//  - Triggered by `Accept: text/markdown` (content negotiation).
//  - Strips nav/footer/scripts/styles, keeps the <main> body.
//  - Prepends YAML frontmatter from <meta> tags (title > og:title, description >
//    og:description, og:image). Only emitted when at least one is present.
//  - Appends JSON-LD <script type="application/ld+json"> blocks as a fenced ```json block.
//  - Emits content-type: text/markdown, vary: accept, and token-count headers.
//  - Sets an explicit content-signal policy (authoritative over Cloudflare's default).
//
// Implementation notes:
//  - Uses `node-html-markdown` (self-contained HTML parser, no DOM globals) so it is
//    Cloudflare-Worker-safe and does not pull in @types pollution that breaks the project.
//  - <main> extraction + JSON-LD collection use dependency-free regex/string scanning,
//    which is sufficient and avoids a full DOM library in the SSR worker.

import { NodeHtmlMarkdown } from 'node-html-markdown';

/** Rough token estimate (≈4 chars/token, matching Cloudflare's x-*-tokens granularity). */
export function estimateTokens(text: string): number {
  return Math.max(0, Math.round(text.length / 4));
}

export interface ConvertOptions {
  /** Raw HTML of the rendered page. */
  html: string;
  /** Optional URL, used to resolve relative asset paths if needed. */
  url?: string;
}

export interface ConvertResult {
  markdown: string;
  frontmatter: { title?: string; description?: string; image?: string };
  jsonLdCount: number;
  originalTokens: number;
}

/** Decode the handful of HTML entities we care about in attributes/text. */
function decodeAttr(s: string): string {
  return s
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&nbsp;/g, ' ');
}

/** Return the inner HTML of the first matching tag, case-insensitively. */
function extractTagInner(html: string, tag: string): string | null {
  const open = new RegExp(`<${tag}[\\s>]`, 'i');
  const start = html.search(open);
  if (start === -1) return null;
  // find the '>' that closes the opening tag
  const openEnd = html.indexOf('>', start);
  if (openEnd === -1) return null;
  const closeRe = new RegExp(`</${tag}>`, 'i');
  const close = html.search(closeRe);
  if (close === -1 || close < openEnd) return null;
  return html.slice(openEnd + 1, close);
}

/** Extract meta content attribute by name= or property=. Returns undefined if absent. */
function metaContent(html: string, key: string): string | undefined {
  // match <meta ... name="key" ... content="value"> or property="key"
  const re = new RegExp(
    `<meta[^>]+(?:name|property)=["']${key}["'][^>]*content=["']([^"']*)["']`,
    'i'
  );
  const m = html.match(re);
  if (m) return decodeAttr(m[1]);
  // also match reversed attribute order (content before name/property)
  const re2 = new RegExp(
    `<meta[^>]+content=["']([^"']*)["'][^>]*(?:name|property)=["']${key}["']`,
    'i'
  );
  const m2 = html.match(re2);
  if (m2) return decodeAttr(m2[1]);
  return undefined;
}

/**
 * Extract a single <meta> value, preferring the standard name over the og: fallback.
 * Cloudflare precedence: <meta name> wins over <meta property="og:...">.
 */
function metaWithFallback(html: string, std: string, og: string): string | undefined {
  return metaContent(html, std) ?? metaContent(html, og);
}

/** Collect all JSON-LD script contents in source order. */
function extractJsonLd(html: string): string[] {
  const blocks: string[] = [];
  const re = /<script[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi;
  for (const m of Array.from(html.matchAll(re))) {
    const raw = m[1].trim();
    if (raw) blocks.push(raw);
  }
  return blocks;
}

/** Build the YAML frontmatter block (Cloudflare: only fields with a value are emitted). */
function buildFrontmatter(meta: { title?: string; description?: string; image?: string }): string {
  const lines: string[] = ['---'];
  if (meta.title) lines.push(`title: ${meta.title}`);
  if (meta.description) lines.push(`description: ${meta.description}`);
  if (meta.image) lines.push(`image: ${meta.image}`);
  lines.push('---');
  return lines.join('\n');
}

const NHM = new NodeHtmlMarkdown({
  keepDataImages: false,
  codeBlockStyle: 'fenced',
  bulletMarker: '-',
  strongDelimiter: '**',
  emDelimiter: '_',
  ignore: ['script', 'style', 'noscript', 'svg', 'form', 'button', 'nav', 'aside'],
});

/**
 * Convert a full HTML page to Markdown-for-Agents format.
 * Throws only on catastrophic parse failure; callers should catch and fall back to HTML.
 */
export function htmlToMarkdownForAgents({ html, url }: ConvertOptions): ConvertResult {
  const originalTokens = estimateTokens(html);

  const title = metaWithFallback(html, 'title', 'og:title');
  const description = metaWithFallback(html, 'description', 'og:description');
  const image = metaContent(html, 'og:image');

  // Prefer the semantic <main> region (BaseLayout wraps page content in <main>).
  const mainHtml = extractTagInner(html, 'main') ?? extractTagInner(html, 'body') ?? html;

  const bodyMarkdown = NHM.translate(mainHtml).trim();

  const jsonLdBlocks = extractJsonLd(html);
  const jsonLdCount = jsonLdBlocks.length;

  // Assemble: frontmatter (if any) + body + JSON-LD fenced block (if any).
  const parts: string[] = [];
  if (title || description || image) {
    parts.push(buildFrontmatter({ title, description, image }));
  }
  parts.push(bodyMarkdown);
  if (jsonLdCount > 0) {
    parts.push('');
    parts.push('```json');
    parts.push(jsonLdBlocks.join('\n'));
    parts.push('```');
  }

  const markdown =
    parts
      .join('\n')
      .replace(/\n{3,}/g, '\n\n')
      .trim() + '\n';

  return {
    markdown,
    frontmatter: { title, description, image },
    jsonLdCount,
    originalTokens,
  };
}

/** Default content-signal policy. Authoritative over Cloudflare's default once set at origin. */
export const CONTENT_SIGNAL = 'ai-train=yes, search=yes, ai-input=yes';
