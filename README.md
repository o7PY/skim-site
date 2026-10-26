# Skim site

The static site for Skim (home page and `/privacy/`). Plain HTML/CSS/JS, no framework, no third-party requests.

- `site.json`: version, download link, contact email.
- `python3 build.py`: regenerates `index.html`, `privacy/index.html` and `assets/` from the templates in `build.py`.
- Preview locally: `python3 -m http.server` in this folder.
- Published with GitHub Pages from `main` (root). The APK is a GitHub Release asset, not a file in the repo.
