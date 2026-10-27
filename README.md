# Skim site

The static site for Skim (home page and `/privacy/`). Plain HTML/CSS/JS, no framework, no third-party requests; fonts are self-hosted (Outfit, Work Sans; SIL OFL licences in `assets/fonts`).

- `DESIGN_NEW.md`: the design system and the decisions behind the page. Edit it, then update `build.py`.
- `site.json`: version, base URL, contact address.
- `python3 build.py`: regenerates `index.html`, `privacy/index.html` and `assets/style.css|site.js`.
- `python3 tools/process_shots.py`: turns the raw phone screenshots (`raw-screenshots/`, not committed) into the WebP files in `assets/shots/`.
- Preview locally: `python3 -m http.server` in this folder.
- There is no download: Skim works only in courses where it has been added, so the call to action is an email to collaborate.
- Published with GitHub Pages from `main` (root).
