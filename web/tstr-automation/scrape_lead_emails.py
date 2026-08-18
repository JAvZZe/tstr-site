"""Scrape contact emails for TSTR ICP lab targets.

Strategy: fetch homepage + likely contact pages, regex-extract emails, score them.
No LLM needed for emails (regex is more reliable + free). Writes leads CSV.
Read-only on the web; writes only to /tmp.
"""
import csv
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36"
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
# junk emails to ignore
JUNK_EMAIL = ("example.com", "sentry.io", "wixpress", "godaddy", ".png", ".jpg", "@2x",
              "domain.com", "yourdomain", "email.com", "test@", "noreply@", "no-reply@")
CONTACT_PATHS = ["", "/contact", "/contact-us", "/contactus", "/about/contact",
                 "/en/contact", "/about-us", "/imprint", "/legal-notice"]


def fetch(url, timeout=12):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read(400_000)
        return raw.decode("utf-8", errors="ignore")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, ValueError):
        return ""


def score_email(e, domain):
    """Prefer role-based addresses on the lab's own domain."""
    e = e.lower()
    s = 0
    if domain and domain.split(".")[0] in e.split("@")[-1]:
        s += 5
    for good in ("info@", "sales@", "enquir", "inquir", "contact@", "hello@", "office@"):
        if e.startswith(good) or good in e:
            s += 3
            break
    if any(j in e for j in JUNK_EMAIL):
        s -= 10
    return s


def emails_for(site, domain):
    found = {}
    base = site.rstrip("/")
    # normalise to origin for path joins
    try:
        p = urllib.parse.urlparse(base)
        origin = f"{p.scheme}://{p.netloc}"
    except ValueError:
        origin = base
    for path in CONTACT_PATHS:
        url = base if path == "" else origin + path
        html = fetch(url)
        if not html:
            continue
        # decode simple obfuscation
        html = html.replace("&#64;", "@").replace("[at]", "@").replace(" (at) ", "@")
        for e in EMAIL_RE.findall(html):
            if any(j in e.lower() for j in JUNK_EMAIL):
                continue
            if len(e) > 60:
                continue
            found[e.lower()] = max(found.get(e.lower(), -99), score_email(e, domain))
        if found:
            break  # stop at first page that yields emails
        time.sleep(0.4)
    if not found:
        return []
    return sorted(found.items(), key=lambda kv: -kv[1])


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    with open("/tmp/tstr_leads/icp.csv") as fh:
        rows = list(csv.DictReader(fh))
    # prioritise: trust_score desc (small independents first)
    rows.sort(key=lambda r: -int(r["trust_score"] or 0))
    out = []
    for i, r in enumerate(rows[:limit], 1):
        cands = emails_for(r["website"], r.get("website_domain") or "")
        best = cands[0][0] if cands else ""
        allc = ";".join(e for e, _ in cands[:4])
        status = "FOUND" if best else "none"
        print(f"[{i}/{limit}] {status:5} {r['business_name'][:34]:34} -> {best or '-'}")
        out.append({**r, "email_found": best, "email_candidates": allc})
        sys.stdout.flush()
    fields = list(rows[0].keys()) + ["email_found", "email_candidates"]
    with open("/tmp/tstr_leads/leads_with_email.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for o in out:
            w.writerow(o)
    hits = sum(1 for o in out if o["email_found"])
    print(f"\nDONE: {hits}/{len(out)} emails found -> /tmp/tstr_leads/leads_with_email.csv")


if __name__ == "__main__":
    main()
