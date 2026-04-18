import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';

export const prerender = false;

const GEMINI_API_KEY = import.meta.env.GEMINI_API_KEY;
const SUPABASE_URL = (import.meta.env.SUPABASE_URL || import.meta.env.PUBLIC_SUPABASE_URL || 'https://haimjeaetrsaauitrhfy.supabase.co') as string;
const SUPABASE_SERVICE_ROLE_KEY = import.meta.env.SUPABASE_SERVICE_ROLE_KEY as string;

// Real category slugs from the DB — keep in sync with categories table
const CATEGORY_CONTEXT = [
  { slug: 'hydrogen-infrastructure-testing', name: 'Hydrogen Infrastructure Testers', keywords: ['hydrogen', 'h2', 'valve', 'pressure', 'fuel cell', 'electrolyser', 'iso 19880', 'sae j2601', 'iso 11114'] },
  { slug: 'materials-testing', name: 'Materials Testers', keywords: ['materials', 'fatigue', 'tensile', 'composites', 'metals', 'corrosion', 'hardness', 'ndt', 'mechanical'] },
  { slug: 'environmental-testing', name: 'Environmental Testers', keywords: ['environmental', 'air quality', 'water quality', 'soil', 'noise', 'esg', 'emissions', 'pollution', 'vibration'] },
  { slug: 'pharmaceutical-testing', name: 'Biopharma & Life Sciences Testers', keywords: ['pharma', 'biopharma', 'life sciences', 'biotech', 'drug', 'medical', 'clinical', 'gmp', 'fda'] },
  { slug: 'oil-gas-testing', name: 'Oil & Gas Testers', keywords: ['oil', 'gas', 'petroleum', 'pipeline', 'refinery', 'upstream', 'downstream'] },
  { slug: 'biotech-testing', name: 'Biotech Testers', keywords: ['biotech', 'biotechnology', 'biological', 'genomics', 'microbiology'] },
  { slug: 'engineering-services', name: 'Engineering Services', keywords: ['engineering', 'inspection', 'calibration', 'ndt', 'structural'] },
];

const GEMINI_PROMPT = (query: string) => `You are a search intent parser for TSTR.directory, a global directory for specialist testing laboratories.

Available category slugs:
${CATEGORY_CONTEXT.map(c => `- ${c.slug}: "${c.name}" (keywords: ${c.keywords.join(', ')})`).join('\n')}

User query: "${query}"

Return ONLY valid JSON (no markdown fences, no explanation):
{
  "category_slug": "<slug from list above, or null if unclear>",
  "region": "<country name e.g. 'United Kingdom', 'Germany', 'United States', or null>",
  "standard_code": "<ISO/IEC/SAE/UN ECE standard code if mentioned e.g. 'ISO 19880-3', or null>",
  "keywords": ["<most important search keyword>", "<second keyword>"],
  "confidence": <number 0.0-1.0>
}`;

export const POST: APIRoute = async ({ request }) => {
  const headers = { 'Content-Type': 'application/json' };

  let query: string;
  try {
    const body = await request.json();
    query = String(body.query || '').trim();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON body' }), { status: 400, headers });
  }

  if (!query || query.length < 2) {
    return new Response(
      JSON.stringify({ results: [], intent: {}, total: 0, search_mode: 'empty' }),
      { headers }
    );
  }

  const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY);

  // --- AI Intent Extraction (Gemini Flash) ---
  let intent: {
    category_slug?: string | null;
    region?: string | null;
    standard_code?: string | null;
    keywords?: string[];
    confidence?: number;
  } = {};
  let searchMode = 'fulltext';

  const OPENROUTER_API_KEY = import.meta.env.OPENROUTER_API_KEY;
  const GEMINI_API_KEY_ALT = import.meta.env.GEMINI_API_KEY_ALT;

  if (GEMINI_API_KEY || GEMINI_API_KEY_ALT || OPENROUTER_API_KEY) {
    try {
      let rawText = '';
      
      // 1. Try Primary Gemini
      if (GEMINI_API_KEY) {
        const geminiRes = await fetch(
          `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_API_KEY}`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              contents: [{ parts: [{ text: GEMINI_PROMPT(query) }] }],
              generationConfig: { temperature: 0.1, maxOutputTokens: 300, responseMimeType: 'application/json' },
            }),
          }
        );

        if (geminiRes.ok) {
          const geminiData = await geminiRes.json();
          rawText = geminiData.candidates?.[0]?.content?.parts?.[0]?.text || '';
          if (rawText) searchMode = 'ai';
        } else {
          const errText = await geminiRes.text();
          console.warn('Gemini 1 HTTP Error:', geminiRes.status, errText);
        }
      }

      // 2. Try Alternate Gemini if Primary failed
      if (!rawText && GEMINI_API_KEY_ALT) {
        const geminiAltRes = await fetch(
          `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_API_KEY_ALT}`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              contents: [{ parts: [{ text: GEMINI_PROMPT(query) }] }],
              generationConfig: { temperature: 0.1, maxOutputTokens: 300, responseMimeType: 'application/json' },
            }),
          }
        );

        if (geminiAltRes.ok) {
          const geminiData = await geminiAltRes.json();
          rawText = geminiData.candidates?.[0]?.content?.parts?.[0]?.text || '';
          if (rawText) searchMode = 'ai_alt';
        } else {
          const errText = await geminiAltRes.text();
          console.warn('Gemini 2 HTTP Error:', geminiAltRes.status, errText);
        }
      }

      // 3. Fallback to OpenRouter
      if (!rawText && OPENROUTER_API_KEY) {
        const orRes = await fetch('https://openrouter.ai/api/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${OPENROUTER_API_KEY}`,
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://tstr.directory',
            'X-Title': 'TSTR Hub'
          },
          body: JSON.stringify({
            model: 'google/gemini-flash-1.5-8b:free',
            messages: [{ role: 'user', content: GEMINI_PROMPT(query) }],
            response_format: { type: 'json_object' }
          }),
        });

        if (orRes.ok) {
          const orData = await orRes.json();
          rawText = orData.choices?.[0]?.message?.content || '';
          if (rawText) searchMode = 'ai_fallback';
        } else {
          const errText = await orRes.text();
          console.warn('OpenRouter HTTP Error:', orRes.status, errText);
        }
      }

      if (rawText) {
        // Strip any residual markdown fences just in case
        const cleanText = rawText.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
        intent = JSON.parse(cleanText);
        console.log('AI intent extracted:', intent, 'Mode:', searchMode);
      }
    } catch (e) {
      console.warn('AI intent extraction failed, falling back to fulltext:', e);
    }
  }

  // --- Build Supabase Query ---
  let dbQuery = supabase
    .from('listings')
    .select(`
      id,
      business_name,
      region,
      trust_score,
      claimed,
      slug,
      category:category_id (name, slug)
    `)
    .eq('status', 'active')
    .order('trust_score', { ascending: false })
    .limit(10);

  // Filter by category if AI identified one with confidence
  if (intent.category_slug && intent.confidence && intent.confidence > 0.4) {
    const { data: cat } = await supabase
      .from('categories')
      .select('id')
      .eq('slug', intent.category_slug)
      .maybeSingle();
    if (cat) {
      dbQuery = dbQuery.eq('category_id', cat.id);
    }
  }

  // Filter by region if AI identified one
  if (intent.region) {
    dbQuery = dbQuery.ilike('region', `%${intent.region}%`);
  }

  // Keyword filtering on business_name (safe, single field)
  const searchTerms = intent.keywords?.length ? intent.keywords : [query];
  const primaryTerm = searchTerms[0];
  if (primaryTerm) {
    dbQuery = dbQuery.ilike('business_name', `%${primaryTerm}%`);
  }

  let { data: results, error } = await dbQuery;

  // If no results with strict filter, widen search (drop category filter, search by name only)
  if ((!results || results.length === 0) && intent.category_slug) {
    const { data: wideResults } = await supabase
      .from('listings')
      .select(`id, business_name, region, trust_score, claimed, slug, category:category_id (name, slug)`)
      .eq('status', 'active')
      .ilike('business_name', `%${query}%`)
      .order('trust_score', { ascending: false })
      .limit(10);
    results = wideResults;
    searchMode = searchMode === 'ai' ? 'ai_widened' : 'fulltext';
  }

  if (error) {
    console.error('Supabase search error:', error);
    return new Response(JSON.stringify({ error: 'Search failed' }), { status: 500, headers });
  }

  return new Response(
    JSON.stringify({
      results: (results || []).map((r) => ({
        id: r.id,
        business_name: r.business_name,
        region: r.region,
        trust_score: r.trust_score,
        claimed: r.claimed,
        slug: r.slug,
        category_name: (r.category as { name?: string } | null)?.name || '',
      })),
      intent,
      total: results?.length || 0,
      search_mode: searchMode,
    }),
    { headers }
  );
};
