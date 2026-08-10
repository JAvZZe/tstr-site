#!/usr/bin/env python3
"""
secret_scan.py — Reusable secret scanner for TSTR.directory.

Modes:
  --staged    Scan only files staged for commit (default; used by pre-commit).
  --all       Scan the entire working tree (excluding ignore globs).
  --history   Scan all reachable git history blobs (slow; reports, does not block).

Exit codes:
  0  no secrets found (or --history report mode)
  1  secrets found in --staged / --all mode (hook should block)

Design:
  - Pattern-based (high-signal token prefixes). Avoids scanning vendored deps,
    local .env files, git internals, and already-redacted markers ("[REDACTED").
  - Never prints the secret value, only the file:line and a short masked preview.

This is the prevention control the project was missing: GitHub push protection
only catches a push AFTER it leaves the machine. This catches it BEFORE commit.
"""
import argparse
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ignore globs (relative to repo root). Vendored deps + local secrets never scanned.
IGNORE_DIRS = [
    "node_modules", "fresh_venv", ".venv", "venv", ".git", "dist", "build",
    ".astro", ".claude", "supabase/.temp", "_ARCHIVE",
]
IGNORE_FILE_GLOB = [".env", ".env.example", "package-lock.json", "pnpm-lock.yaml",
                    "yarn.lock", "*.min.js", "*.map", "frolic-session.json",
                    "frolic-backup-*.json"]

# High-signal secret patterns. Order: (name, regex).
# Minimum lengths tuned to REAL key lengths so documentation placeholders
# (e.g. "AIzaSy...L96k") do NOT false-positive. Google keys are 39 chars,
# Supabase PATs ~40, GitHub PATs ~36, Stitch ~60, OpenAI/Stripe ~48.
PATTERNS = [
    ("supabase_service_role", re.compile(r"sb_secret_[A-Za-z0-9_]{20,}")),
    ("supabase_pat", re.compile(r"sbp_[A-Za-z0-9]{30,}")),
    ("jwt", re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
    ("resend", re.compile(r"re_[A-Za-z0-9]{20,}")),
    ("google_api_key", re.compile(r"AIza[0-9A-Za-z_\-]{30,}")),
    ("openai_or_stripe", re.compile(r"sk-[A-Za-z0-9]{30,}")),
    ("openrouter", re.compile(r"sk-or-[A-Za-z0-9]{30,}")),
    ("linkedin", re.compile(r"WPL_AP1\.[A-Za-z0-9]{20,}")),
    ("stitch", re.compile(r"AQ\.[A-Za-z0-9]{30,}")),
    ("paypal", re.compile(r"EA[0-9A-Z]{20,}|EB[0-9A-Z]{20,}")),
    ("github_pat", re.compile(r"ghp_[A-Za-z0-9]{30,}")),
    ("gitlab_pat", re.compile(r"glpat-[A-Za-z0-9_\-]{15,}")),
    ("generic_live_sk", re.compile(r"sk_live_[A-Za-z0-9_\-]{10,}")),
]

REDACTED_MARK = "[REDACTED"


def is_ignored(path: str) -> bool:
    parts = path.split(os.sep)
    if any(d in parts for d in IGNORE_DIRS):
        return True
    base = os.path.basename(path)
    for g in IGNORE_FILE_GLOB:
        if g.startswith("*"):
            if base.endswith(g[1:]):
                return True
        elif g == base:
            return True
    # frolic backup glob exact
    return "frolic-backup" in base and base.endswith(".json")


def scan_text(text: str, path: str):
    hits = []
    for name, pat in PATTERNS:
        for m in pat.finditer(text):
            # skip already-redacted contexts
            start = max(0, m.start() - 20)
            ctx = text[start:m.end()]
            if REDACTED_MARK in ctx or "[REDACTED" in text[m.start():m.start() + 40]:
                continue
            line_no = text.count("\n", 0, m.start()) + 1
            preview = m.group(0)[:6] + "…" + m.group(0)[-4:]
            hits.append((name, line_no, preview))
    return hits


def scan_file(path: str):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError):
        return []
    return scan_text(text, path)


def staged_files():
    out = subprocess.run(
        ["git", "-C", ROOT, "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        capture_output=True, text=True, check=False,
    ).stdout.splitlines()
    return [f for f in out if f and not is_ignored(f)]


def all_files():
    results = []
    for dp, dn, fn in os.walk(ROOT):
        if any(ig in dp.split(os.sep) for ig in IGNORE_DIRS):
            continue
        for f in fn:
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, ROOT)
            if is_ignored(rel):
                continue
            results.append(rel)
    return results


def history_scan():
    """Scan all blobs across git history. Report only; exit 0 regardless.

    Uses a single combined regex `git grep -E -n -I "<p1>|<p2>|..." <revs>` over
    `git rev-list --all` — one pass instead of N prefixes x M commits. A hard timeout
    prevents hangs on very large histories (this mode is manual/report-only, never
    run by the pre-commit hook).
    """
    print("== History scan (report only; secrets below remain in git history) ==")
    revs = subprocess.run(
        ["git", "-C", ROOT, "rev-list", "--all"],
        capture_output=True, text=True, check=False,
    ).stdout.splitlines()
    if not revs:
        print("  No commits found in history.")
        return 0
    # Combined regex of high-signal prefixes (fixed alternation, one grep pass).
    prefixes = ["sb_secret_", "sbp_", "AIzaSy", "re_", "WPL_AP1\\.", "AQ\\.",
                "ghp_", "sk-or-", "sk_live_", "glpat-", "EA[0-9A-Z]{8,}", "EB[0-9A-Z]{8,}"]
    pattern = "|".join(prefixes)
    try:
        proc = subprocess.run(
            ["git", "-C", ROOT, "grep", "-I", "-E", "-n", "-e", pattern] + revs,
            capture_output=True, text=True, check=False, timeout=150,
        )
    except subprocess.TimeoutExpired:
        print("  History scan timed out (>150s). Run on a shallow/limited range, e.g.:")
        print("    git grep -E -n -e '<pattern>' HEAD~50..HEAD")
        return 0
    seen = {}
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split(":", 2)  # <commit>:<path>:<lineno>:<text>
        path = parts[1] if len(parts) >= 2 else line
        seen[path] = seen.get(path, 0) + 1
    if not seen:
        print("  No high-signal secrets found in git history.")
    else:
        print(f"  Found secrets in {len(seen)} path(s) across history:")
        for p, c in sorted(seen.items(), key=lambda x: -x[1]):
            print(f"  {c:4d}  {p}")
        print("  ACTION: rotate these credentials; git history cannot be cleaned without a")
        print("           force-push/rewrite (coordinate with the repo owner). Redaction of the")
        print("           working tree does NOT remove them from history.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="TSTR secret scanner")
    ap.add_argument("--staged", action="store_true", help="scan staged files (default)")
    ap.add_argument("--all", action="store_true", help="scan whole working tree")
    ap.add_argument("--history", action="store_true", help="scan git history (report only)")
    args = ap.parse_args()

    if args.history:
        return history_scan()

    if args.all:
        files = all_files()
        mode = "--all"
    else:
        files = staged_files()
        mode = "--staged"

    print(f"== secret_scan {mode}: {len(files)} file(s) ==")
    total = 0
    for rel in files:
        full = os.path.join(ROOT, rel)
        if not os.path.isfile(full):
            continue
        for name, line_no, preview in scan_file(full):
            total += 1
            print(f"  SECRET[{name}] {rel}:{line_no}  {preview}")
    if total:
        print(f"\nFOUND {total} secret(s). Blocking commit. Rotate the credential, redact the value, and re-stage.")
        return 1
    print("  clean: no staged secrets detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
