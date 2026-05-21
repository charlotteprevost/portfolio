# Portfolio

Minimal static portfolio site. HTML + CSS only; no build step.

## Canonical URL for recruiters

Use **one stable HTTPS URL** everywhere (resume, LinkedIn Featured, GitHub profile, email signature):

- After publishing to GitHub Pages, the site is typically:  
  `https://charlotteprevost.github.io/<repository-name>/`  
  Point the repo **Pages** settings at `/ (root)` or `/docs` depending on your layout; if this folder is the repo root, the canonical entry is `index.html` at the site root.

Search indexing is enabled (`robots`: index, follow) so the portfolio can appear in Google when linked from other sites.

## GitHub Pages

- **Source**: repository root
- **Entry**: `index.html`

## Local

```bash
python3 -m http.server 5173   # serve the site locally on port 5173
# open http://localhost:5173/  # preview in your browser
```

## Privacy

- No private CV/resume in the public site (see `.gitignore`).
- Run `python3 tools/privacy_audit.py` before pushing (portfolio-repo specific).
- For a broader audit across repos, run `python3 tools/audit_github_repos.py` (symlink to `PRIVATE/98_TOOLS/privacy_audit/audit_github_repos.py`; recreate with `bash PRIVATE/98_TOOLS/install_layout_symlinks.sh`).
