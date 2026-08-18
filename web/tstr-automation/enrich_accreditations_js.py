"""Re-run accreditation enrichment with crawl4ai (JS rendering).

Why: the plain-HTTP pass found evidence for only 1/10 labs. Most lab sites are
JS-rendered, so plain fetch may have seen an empty shell. This re-checks the same
labs with a real browser render before we conclude the data isn't on their sites.

Reads  /tmp/tstr_leads/outreach_ready.csv
Writes /tmp/tstr_leads/enrichment_js.json
"""
import asyncio
import csv
import json
import re
import sys

from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig

BODIES = {
    "A2LA": r"\bA2LA\b", "UKAS": r"\bUKAS\b", "DAkkS": r"\bDAkkS\b",
    "SAC": r"Singapore Accreditation Council|SAC[- ]SINGLAS|\bSINGLAS\b",
    "NVLAP": r"\bNVLAP\b", "IAS": r"International Accreditation Service",
    "ANAB": r"\bANAB\b", "COFRAC": r"\bCOFRAC\b", "RvA": r"\bRvA\b",
    "SCC": r"Standards Council of Canada", "NATA": r"\bNATA\b",
    "Nadcap": r"\bNadcap\b", "SANAS": r"\bSANAS\b", "ENAC": r"\bENAC\b",
    "ACCREDIA": r"\bACCREDIA\b", "PJLA": r"\bPJLA\b", "IANZ": r"\bIANZ\b",
    "DANAK": r"\bDANAK\b", "FINAS": r"\bFINAS\b", "NA (Norway)": r"\bNorsk akkreditering\b",
}
STANDARDS = {
    "ISO/IEC 17025": r"ISO[/\s]?IEC\s?17025|ISO\s?17025",
    "ISO/IEC 17020": r"ISO[/\s]?IEC\s?17020|ISO\s?17020",
    "ISO/IEC 17065": r"ISO[/\s]?IEC\s?17065",
    "ISO 9001": r"ISO\s?9001", "ISO 13485": r"ISO\s?13485",
    "ISO 14001": r"ISO\s?14001", "AS9100": r"\bAS9100\b",
    "GMP": r"\bGMP\b", "GLP": r"\bGLP\b",
}
CERT_NO = re.compile(
    r"(?:cert(?:ificate)?\.?\s*(?:no\.?|number|#)|accreditation\s*(?:no\.?|number))"
    r"\s*:?\s*([A-Z0-9][A-Z0-9\-/\.]{3,20})", re.IGNORECASE)

PATHS = ["", "/accreditation", "/accreditations", "/quality", "/certifications",
         "/about", "/capabilities"]


def origin(u):
    m = re.match(r"(https?://[^/]+)", u)
    return m.group(1) if m else u.rstrip("/")


async def check_lab(crawler, lead, cfg):
    base = lead["website"].rstrip("/")
    org = origin(base)
    urls = [base] + [org + p for p in PATHS[1:]]
    bodies, stds, certnos, pdfs, ok_pages = {}, {}, set(), set(), []

    for u in urls[:5]:
        try:
            res = await crawler.arun(url=u, config=cfg)
        except (OSError, ValueError, RuntimeError, TimeoutError) as exc:
            print(f"    warn: {u} -> {type(exc).__name__}", file=sys.stderr)
            continue
        if not getattr(res, "success", False):
            continue
        text = (getattr(res, "markdown", "") or "")[:200_000]
        if not text.strip():
            continue
        ok_pages.append(u)
        for name, pat in BODIES.items():
            if re.search(pat, text, re.IGNORECASE):
                bodies.setdefault(name, u)
        for name, pat in STANDARDS.items():
            if re.search(pat, text, re.IGNORECASE):
                stds.setdefault(name, u)
        for m in CERT_NO.finditer(text):
            c = m.group(1).strip(".")
            if not re.fullmatch(r"(19|20)\d{2}", c):
                certnos.add(c)
        for link in re.findall(r"\((https?://[^)\s]+\.pdf[^)\s]*)\)", text, re.IGNORECASE):
            if re.search(r"cert|accred|scope|iso|qual", link, re.IGNORECASE):
                pdfs.add(link)

    proof = bool(pdfs or certnos)
    verdict = ("SELLABLE" if bodies and stds and proof
               else "PARTIAL" if (bodies and stds) or proof
               else "THIN")
    return {"id": lead["id"], "business_name": lead["business_name"],
            "website": lead["website"], "pages_rendered": ok_pages,
            "bodies": bodies, "standards": stds,
            "cert_numbers": sorted(certnos)[:6], "pdfs": sorted(pdfs)[:6],
            "verdict": verdict, "needs_verification": not proof}


def load_leads(limit):
    with open("/tmp/tstr_leads/outreach_ready.csv") as fh:
        return list(csv.DictReader(fh))[:limit]


def save_results(out):
    with open("/tmp/tstr_leads/enrichment_js.json", "w") as f:
        json.dump(out, f, indent=2)


async def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    leads = load_leads(limit)

    browser = BrowserConfig(headless=True, verbose=False)
    cfg = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, page_timeout=30000)

    out = []
    async with AsyncWebCrawler(config=browser) as crawler:
        for i, lead in enumerate(leads, 1):
            r = await check_lab(crawler, lead, cfg)
            out.append(r)
            print(f"[{i}/{len(leads)}] {r['verdict']:8} {lead['business_name'][:30]:30} "
                  f"pages={len(r['pages_rendered'])} bodies={list(r['bodies']) or '-'} "
                  f"std={list(r['standards'])[:3] or '-'} pdf={len(r['pdfs'])} "
                  f"certno={len(r['cert_numbers'])}")
            sys.stdout.flush()

    save_results(out)
    tally = {}
    for r in out:
        tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1
    print(f"\nVERDICTS (JS-rendered): {tally}")


if __name__ == "__main__":
    asyncio.run(main())
