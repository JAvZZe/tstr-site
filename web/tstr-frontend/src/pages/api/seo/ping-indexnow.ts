import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ request }) => {
  try {
    const { urls } = await request.json();
    
    if (!urls || !Array.isArray(urls)) {
      return new Response(JSON.stringify({ error: 'Missing or invalid urls array' }), { status: 400 });
    }

    const host = "tstr.directory";
    const key = "ecdafe54e05b458897c8d990867d9342";
    
    const payload = {
      host: host,
      key: key,
      keyLocation: `https://${host}/${key}.txt`,
      urlList: urls
    };

    const response = await fetch('https://api.indexnow.org/IndexNow', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
      },
      body: JSON.stringify(payload)
    });

    if (response.ok || response.status === 202) {
      return new Response(JSON.stringify({ message: `Successfully pushed ${urls.length} urls to IndexNow` }), { status: 200 });
    } else {
      const errorText = await response.text();
      return new Response(JSON.stringify({ error: 'IndexNow API failed', details: errorText }), { status: response.status });
    }
  } catch (err) {
    return new Response(JSON.stringify({ error: 'Internal Server Error', details: err.message }), { status: 500 });
  }
};
