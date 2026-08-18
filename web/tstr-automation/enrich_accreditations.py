"""Enrich TSTR lead listings with REAL accreditation evidence.

Goal: replace inferred "standards" with verifiable accreditations — issuing body,
certificate number, PDF/scope link, expiry — so a listing is credible enough to
sell. Anything we cannot confirm is flagged needs_verification (never invented).

Reads  /tmp/tstr_leads/outreach_ready.csv
Writes /tmp/tstr_leads/enrichment.json  (+ .md report)
Read-only on the web; no DB writes (review before ingest).
"""
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122 Safari/537.36")

# Pages where labs publish accreditation evidence
ACCRED_PATHS = [
    "", "/accreditation", "/accreditations", "/accreditation-certificates",
    "/quality", "/quality-assurance", "/certifications", "/certificates",
    "/about/accreditation", "/about/quality", "/approvals", "/scope",
    "/en/accreditation", "/capabilities", "/services",
]

# Real accreditation bodies (what buyers actually check)
BODIES = {
    "A2LA": r"\bA2LA\b", "UKAS": r"\bUKAS\b", "DAkkS": r"\bDAkkS\b",
    "SAC": r"Singapore Accreditation Council|\bSAC\b", "NVLAP": r"\bNVLAP\b",
    "IAS": r"International Accreditation Service|\bIAS\b",
    "ANAB": r"\bANAB\b", "COFRAC": r"\bCOFRAC\b", "RvA": r"\bRvA\b",
    "SCC": r"Standards Council of Canada|\bSCC\b", "NATA": r"\bNATA\b",
    "Nadcap": r"\bNadcap\b|\bNADCAP\b", "SANAS": r"\bSANAS\b",
    "SWEDAC": r"\bSWEDAC\b", "ENAC": r"\bENAC\b", "ACCREDIA": r"\bACCREDIA\b",
}

# Accreditation standards (the ones that matter for testing labs)
STANDARDS = {
    "ISO/IEC 17025": r"ISO[/\s]?IEC\s?17025|ISO\s?17025",
    "ISO/IEC 17020": r"ISO[/\s]?IEC\s?17020|ISO\s?17020",
    "ISO/IEC 17065": r"ISO[/\s]?IEC\s?17065|ISO\s?17065",
    "ISO 9001": r"ISO\s?9001",
    "ISO 13485": r"ISO\s?13485",
    "ISO 14001": r"ISO\s?14001",
    "ISO 45001": r"ISO\s?45001",
    "GMP": r"\bGMP\b|Good Manufacturing Practice",
    "GLP": r"\bGLP\b|Good Laboratory Practice",
    "AS9100": r"\bAS9100\b",
}

CERT_NO_RE = re.compile(
    r"(?:cert(?:ificate)?\.?\s*(?:no\.?|number|#)\s*:?\s*)([A-Z0-9][A-Z0-9\-/\.]{3,20})",
    re.IGNORECASE)
PDF_RE = re.compile(r'href="([^"]+\.pdf[^"]*)"', re.IGNORECASE)


def fetch(url, timeout=14):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            ctype = r.headers.get("Content-Type", "")
            if "html" not in ctype.lower():
                return ""
            return r.read(600_000).decode("utf-8", errors="ignore")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
            OSError, ValueError):
        return ""


def visible_text(html):
    html = re.sub(r"(?is)<(script|style|noscript).*?</\1>", " ", html)
    return re.sub(r"\s+", " ", re.sub(r"(?s)<[^>]+>", " ", html))


def origin_of(url):
    try:
        p = urllib.parse.urlparse(url)
        return f"{p.scheme}://{p.netloc}"
    except ValueError:
        return url.rstrip("/")


def analyse(site):
    """Crawl a lab's accreditation-ish pages; return evidence found."""
    origin = origin_of(site)
    base = site.rstrip("/")
    seen_bodies, seen_stds, cert_nos, pdfs, pages = {}, {}, set(), set(), []

    for path in ACCRED_PATHS:
        url = base if path == "" else origin + path
        html = fetch(url)
        if not html:
            continue
        pages.append(url)
        text = visible_text(html)

        for name, pat in BODIES.items():
            if re.search(pat, text):
                seen_bodies.setdefault(name, url)
        for name, pat in STANDARDS.items():
            if re.search(pat, text):
                seen_stds.setdefault(name, url)
        for m in CERT_NO_RE.finditer(text):
            cand = m.group(1).strip(".")
            if not re.fullmatch(r"\d{4}", cand):      # drop bare years
                cert_nos.add(cand)
        for m in PDF_RE.finditer(html):
            href = m.group(1)
            if re.search(r"cert|accred|scope|iso|quality", href, re.IGNORECASE):
                pdfs.add(urllib.parse.urljoin(url, href))
        time.sleep(0.3)
        if len(pages) >= 6:
            break

    return {"pages_checked": pages, "bodies": seen_bodies, "standards": seen_stds,
            "cert_numbers": sorted(cert_nos)[:6], "pdfs": sorted(pdfs)[:6]}


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    with open("/tmp/tstr_leads/outreach_ready.csv") as fh:
        leads = list(csv.DictReader(fh))[:limit]

    out = []
    for i, lead in enumerate(leads, 1):
        ev = analyse(lead["website"])
        # sellable = a real accreditation body AND an accreditation standard
        strong = bool(ev["bodies"]) and bool(ev["standards"])
        has_proof = bool(ev["pdfs"] or ev["cert_numbers"])
        verdict = ("SELLABLE" if strong and has_proof else
                   "PARTIAL" if strong or has_proof else "THIN")
        rec = {**{k: lead[k] for k in ("id", "business_name", "website",
                                       "trust_score", "category_slug")},
               **ev, "verdict": verdict,
               "needs_verification": not has_proof}
        out.append(rec)
        print(f"[{i}/{len(leads)}] {verdict:8} {lead['business_name'][:32]:32} "
              f"bodies={list(ev['bodies']) or '-'} std={list(ev['standards'])[:3] or '-'} "
              f"pdf={len(ev['pdfs'])} certno={len(ev['cert_numbers'])}")
        sys.stdout.flush()

    with open("/tmp/tstr_leads/enrichment.json", "w") as f:
        json.dump(out, f, indent=2)

    tally = {}
    for r in out:
        tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1
    print(f"\nVERDICTS: {tally}")
    print("wrote /tmp/tstr_leads/enrichment.json")


if __name__ == "__main__":
    main()
