"""Crawl4ai pilot: render 3 real testing-lab sources, extract markdown, feed to BAML.

Proves the pipeline: crawl4ai (JS render + markdown) -> BAML (typed LabListing).
Read-only: fetches public pages, prints structured output. No DB writes.
"""
import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "_baml_spike"))
from baml_client import b

with open("/tmp/or_key.txt") as _f:
    os.environ["OPENROUTER_API_KEY"] = _f.read().strip()

# 3 representative sources (testing labs / directories)
SOURCES = [
    ("SGS", "https://www.sgs.com/en"),
    ("TUV SUD", "https://www.tuvsud.com/en"),
    ("Intertek", "https://www.intertek.com/"),
]

async def crawl(url):
    from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig
    cfg = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, word_count_threshold=20)
    async with AsyncWebCrawler() as crawler:
        res = await crawler.arun(url=url, config=cfg)
        if res.success:
            return res.markdown[:5000] if res.markdown else ""
        return f"[crawl failed: {res.error_message}]"

async def main():
    for name, url in SOURCES:
        print(f"\n{'='*60}\n>> {name} ({url})")
        md = await crawl(url)
        if md.startswith("[crawl failed"):
            print(md); continue
        print(f"   crawled {len(md)} chars of markdown")
        try:
            out = b.ExtractLabListing(md)
            print("   BAML ->", json.dumps(out.model_dump() if hasattr(out,'model_dump') else out.__dict__, indent=2, default=str)[:700])
        except (ValueError, KeyError) as e:
            print("   BAML error:", repr(e)[:200])

if __name__ == "__main__":
    asyncio.run(main())
