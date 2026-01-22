#!/usr/bin/env python3
"""
Privacy audit for the *public* portfolio repo.

Goal: fail fast if common private identifiers accidentally enter the site repo.
This is intentionally conservative; you can relax patterns later.

Usage:
  python3 tools/privacy_audit.py
  python3 tools/privacy_audit.py --path .
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# Candidate matcher; we only flag if it looks phone-ish (min digits + punctuation).
PHONE_CANDIDATE_RE = re.compile(r"(\+?\d[\d\s().-]{7,}\d)")

DENYLIST_PATHS = {
    "cv",
}

DENYLIST_EXTS = {
    ".pdf",
    ".doc",
    ".docx",
}

TEXT_EXTS = {
    ".html",
    ".css",
    ".js",
    ".ts",
    ".md",
    ".txt",
    ".json",
    ".xml",
    ".yml",
    ".yaml",
    ".svg",
}

def normalize_digits(s: str) -> str:
    return "".join(ch for ch in s if ch.isdigit())


def looks_like_date(s: str) -> bool:
    return bool(re.fullmatch(r"\d{4}[-/.]\d{2}[-/.]\d{2}", s.strip()))


def looks_like_ip(s: str) -> bool:
    # very small helper to avoid false positives like 127.0.0.1
    return bool(re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", s.strip()))


def load_allowlist(root: Path) -> tuple[set[str], set[str]]:
    """
    Allowlist for *intentionally public* identifiers.
    Stored in-repo as tools/privacy_allowlist.json (safe to publish).
    """
    allow_file = root / "tools" / "privacy_allowlist.json"
    if not allow_file.exists():
        return set(), set()
    raw = json.loads(allow_file.read_text(encoding="utf-8"))
    allowed_emails = {str(x).strip().lower() for x in raw.get("allowed_emails", []) if str(x).strip()}
    allowed_domains = {str(x).strip().lower() for x in raw.get("allowed_email_domains", []) if str(x).strip()}
    return allowed_emails, allowed_domains


def iter_files(root: Path) -> list[Path]:
    """
    Return files that are *publishable* from this repo.

    If we're inside a git repo, we only scan:
      - tracked files
      - untracked but NOT ignored files (i.e., would be added/pushed by accident)

    This is the behavior we want for privacy: ignored local material (like cv PDFs)
    should not block publishing, but *would* be caught if someone removes ignores.
    """
    # Prefer git-aware listing so .gitignore is honored.
    try:
        proc = subprocess.run(
            ["git", "ls-files", "-co", "--exclude-standard"],
            cwd=str(root),
            check=True,
            capture_output=True,
            text=True,
        )
        files = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
        return [root / f for f in files if f]
    except Exception:
        # Fallback: scan everything (best effort) while skipping .git
        out: list[Path] = []
        for p in root.rglob("*"):
            if p.is_dir():
                continue
            if ".git" in p.parts:
                continue
            out.append(p)
        return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default=".", help="Repo root to scan (default: .)")
    args = ap.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"ERROR: path does not exist: {root}", file=sys.stderr)
        return 2

    problems: list[str] = []
    allowed_emails, allowed_domains = load_allowlist(root)

    # Path/extension denylist
    for p in iter_files(root):
        rel = p.relative_to(root)
        if rel.parts and rel.parts[0] in DENYLIST_PATHS:
            problems.append(f"Forbidden path in public repo: {rel}")
            continue
        if p.suffix.lower() in DENYLIST_EXTS:
            problems.append(f"Forbidden file type in public repo: {rel}")

    # Content scan (only text-ish files)
    for p in iter_files(root):
        if p.suffix.lower() not in TEXT_EXTS:
            continue
        try:
            data = p.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            problems.append(f"Could not read {p}: {e}")
            continue

        for m in EMAIL_RE.finditer(data):
            email = m.group(0).strip().lower()
            if email in allowed_emails:
                continue
            if "@" in email:
                domain = email.split("@", 1)[1]
                if domain in allowed_domains:
                    continue
            problems.append(f"Email-like string found in {p.relative_to(root)}: {m.group(0)}")
            break

        # Very rough phone heuristic; can false-positive on IDs, so only flag if it contains separators
        for m in PHONE_CANDIDATE_RE.finditer(data):
            s = m.group(0).strip()
            if looks_like_date(s) or looks_like_ip(s):
                continue
            if not any(ch in s for ch in ("+", "(", ")", "-")):
                continue
            if len(normalize_digits(s)) < 10:
                continue
            problems.append(f"Phone-like string found in {p.relative_to(root)}: {s}")
            break

    if problems:
        print("PRIVACY AUDIT FAILED:\n", file=sys.stderr)
        for prob in problems:
            print(f"- {prob}", file=sys.stderr)
        return 1

    print("Privacy audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

