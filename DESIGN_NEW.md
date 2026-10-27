# DESIGN_NEW.md: the Skim website

> **Status: BUILT (draft 1 implemented, 2026-10-27). Edit this file and re-run `python3 build.py`; the site is generated from it.** `DESIGN.md` (the monochrome shadcn reference) is **not** used as a system; only its taste is kept: quiet, hairline borders, large radii, tight confident headlines, nothing decorative.
> Built with the ui-ux-pro-max skill (landing patterns: *App Store style* and *Feature-Rich Showcase*; style: *Flat design*; palette seed: *education teal + amber*), then adjusted by hand and contrast-checked.

## 1. What the site is for
- **One job:** let professors, organisations and companies understand Skim in about a minute and **write to us to collaborate on the testing phase**.
- **Why not a download button:** Skim only works inside the human's Microsoft environment today (the bot is installed in one tenant; pairing codes come from those teams). A public APK would let strangers install an app they cannot use. The APK is shared privately with collaborators. *(Supersedes P5-D-110 for the site: no APK on the page, no GitHub Release.)*
- **Honesty rules (P5-D-117, kept):** "Early preview", "Android only", "testing phase". Never "official IISc software"; "Not affiliated with Microsoft". Nothing from Phase 6 sold as available that is not in the app. Subscription plans for organisations: **"coming", with no prices and no dates.**
- **Audiences, in order:** (1) professors and organisations (the collaboration call), (2) students who land here (they learn what it is and that their professor has to add Skim), (3) anyone curious.

## 2. Voice
Calm, specific, a little warm. Short sentences. Plain words ("card", "reminder", "date moved"), no buzzwords ("AI-powered", "revolutionary"). Say what it does, show it, stop.
- **Headline:** *Swipe through your semester.*
- **Subline:** *Skim turns your course's Teams posts and files into a deck of cards, with dates, reminders and alerts when a date moves.*
- **Primary button:** *Collaborate with us* (opens an email). **Secondary:** *See how it works* (scrolls to the story).
- **Badge:** *Early preview · Android · testing phase*

## 3. Page structure (single page + `/privacy/`)
A **scroll story** with one large phone pinned beside the text; the phone's screen changes with each chapter.

| # | Section | What it holds |
|---|---|---|
| 0 | Header | Logo + "Skim", links: How it works · Collaborate · Privacy, and a small "Collaborate" button. |
| 1 | **Hero** | Headline, subline, the two buttons, the badge, one line: *"Works with courses where Skim has been added."* The pinned phone starts here (the deck). |
| 2 | **Story, 5 chapters** | See below. Each chapter: a number, a short title, 2 to 3 lines, colour chips where relevant. |
| 3 | **Also** | Four small tiles: Starred · Important checklist · Works offline · Quiet hours and mute. |
| 4 | **Collaborate** | Three plain cards: *Professors*, *Organisations and companies*, *Students*. One email button. A line: "Plans for organisations are coming. For now we are collaborating during the testing phase." |
| 5 | **Privacy, plainly** | 5 short points with icons. Link to `/privacy/`. |
| 6 | Footer | Skim 1.0.0 · early preview · Android only · Privacy · Contact · "Not affiliated with Microsoft. Not official IISc software." |

**Story chapters** (phone screen in brackets):
1. **A professor posts in Teams.** Skim is added to the course team once. It quietly reads the standard channels (never private ones) and joins your courses with a code. *(Teams tab: your courses)*
2. **It becomes a card.** Dates, files and links, in one deck. Every kind of event has its own colour. *(the Deck, with an important card and a change card; nine colour chips beside it)*
3. **Swipe: dismiss or open.** Left to dismiss (with undo), right to open the full card, up to ask about it. *(mid-swipe with a label, then the card detail)*
4. **Dates move. Skim follows.** Reminders that move when a date moves, alerts when something changes or something new arrives, even with the app closed. *(the Reminders list, then a notification in the shade)*
5. **Ask the course.** Questions answered only from your course messages, with the sources shown. *(the chat sheet, an answer with source chips)*

## 4. Colour (both themes, follow the visitor's phone)
Flat, tonal surfaces. **No gradients, no coloured shadows.** Teal is the brand, amber is the one call to action. The nine event colours appear only as **small chips and tags** and inside screenshots.

| Token | Light | Dark | Use |
|---|---|---|---|
| `--bg` | `#F0FDFA` | `#081B1A` | page |
| `--paper` | `#FFFFFF` | `#0F2927` | cards, header |
| `--soft` | `#E6F7F4` | `#143532` | quiet panels, tiles |
| `--ink` | `#0B2B29` | `#ECFDF5` | headings, body |
| `--muted` | `#44625F` | `#A3C2BE` | secondary text |
| `--hair` | `#CFE5E1` | `#1F4A46` | 1 px borders |
| `--teal` | `#0F766E` | `#2DD4BF` | links, icons, text accents |
| `--teal-bright` | `#0D9488` | `#2DD4BF` | large shapes and graphics only |
| `--teal-soft` | `#CCFBF1` | `#134E4A` | chip and badge fills |
| `--amber` | `#F59E0B` | `#FBBF24` | the call-to-action button |
| `--on-amber` | `#1C1917` | `#1C1917` | text on amber: **dark, never white** |

Contrast (computed): ink on bg 14.5:1 / 16.9:1; muted on paper 6.7:1 / 8.1:1; teal on paper 5.5:1 / 8.3:1; on-amber on amber 8.1:1 / 10.5:1; white on `#0F766E` 5.5:1. `--teal-bright` on paper is 3.7:1, so it is **never used for text**. Colour is never the only signal (chips always carry a label).

**Event colours** (same as the app, light / dark): quiz `#854D0E`/`#FACC15`, exam `#A21CAF`/`#E879F9`, assignment `#1D4ED8`/`#7DB4FB`, project `#7E22CE`/`#CE9CFD`, lab `#3F6212`/`#A3E635`, class `#0369A1`/`#38BDF8`, office hours `#0F766E`/`#2DD4BF`, presentation `#166534`/`#4ADE80`, other `#475569`/`#A3B1C6`. **Red appears only on an "important" card inside a screenshot, never in the page's own UI.**
*Note:* the site is teal and amber while the app is navy and sky blue. The logo's amber chip and the screenshots tie them together; if the two feel disconnected on review, the fix is to shift the page accent to the app's sky blue, not to touch the app.

## 5. Typography
- **Headlines: Outfit** (600 and 700). **Body: Work Sans** (400, 500). Both **self-hosted** (variable woff2, Latin subset, `font-display: swap`); no Google Fonts request.
- Scale (fluid): display `clamp(40px, 7vw, 72px)` / 1.04 / -0.025em · h2 `clamp(28px, 4.5vw, 44px)` / 1.1 / -0.02em · h3 22px / 1.25 · body 17px / 1.6 · small 14px / 1.5 · chip label 13px 600.
- Body never below 16 px (14 px only for captions and footer). Line length 60 to 70 characters.

## 6. Layout, shape, spacing
- 8 px grid. Container 1120 px, 24 px side gutters (16 px under 480 px). Sections 96 px apart on desktop, 64 px on phones.
- Radii: cards 24 px, tiles 20 px, buttons and badges pill (999), chips 10 px.
- Depth: 1 px `--hair` border, no shadow, except the phone frame (one soft shadow). Alternate `--bg` and `--soft` bands to separate sections.
- Icons: one set (Lucide-style thin outline, 2 px stroke), inline SVG. **No emoji as icons.**
- **Phone frame:** a generic, original device outline in CSS/SVG (no real device artwork), aspect 9:19.5 with reserved space so nothing shifts while images load.

## 7. Components
- **Primary button:** amber fill, dark text, pill, 52 px tall, 600. Hover: slightly deeper amber (no movement beyond 1 px), focus ring 3 px `--teal`.
- **Secondary:** transparent, 1.5 px teal border, teal text. **Header button:** the primary, 40 px.
- **Chip:** `--teal-soft` or an event colour at 12% over paper, text in that colour, icon + label, 10 px radius, 13 px.
- **Badge:** pill with a teal dot, "Early preview · Android · testing phase".
- **Card:** paper, 1 px hair, 24 px radius, 24 px padding. **Tile:** soft, 20 px radius.
- **Story chapter:** large numeral in `--teal-bright`, title (h3), text, optional chips.

## 8. Motion (calm and purposeful)
- Sections and chapters fade up once (16 px, 300 ms) as they enter (IntersectionObserver). **Nothing loops. Nothing autoplays.**
- The pinned phone cross-fades its screen in 250 ms when the active chapter changes. Hover and focus states 150 ms.
- **`prefers-reduced-motion`:** no reveal, no pin cross-fade; each chapter shows its own phone image statically.
- **Narrow screens (under 860 px):** no pinning. Each chapter shows its own phone, then its text.

## 9. Images and screenshots
- The human's **real screenshots only** (P5-D-118), in the generic phone frame; never faked. WebP, `width`/`height` set, `loading="lazy"` below the fold, hero image eager.
- Light and dark versions of the story screens; `<picture>` picks the one matching the visitor's theme.
- Page weight under 1.5 MB. Screenshot list in section 12.

## 10. Accessibility and performance
Contrast per section 4; visible focus on everything; 44 px minimum touch targets; one `h1`; landmarks (`header`, `main`, `footer`); alt text that says what the screen shows; skip link; works without JavaScript (all text visible, no pinning). Lighthouse mobile 95 or more in all four categories; no third-party requests, no cookies, no analytics.

## 11. Open items for the human
1. **Contact address:** `pragnyayadav22@gmail.com` (given by the human; it replaces the earlier onmicrosoft.com address, which needs an Exchange mailbox to receive outside mail).
2. **Web address:** GitHub Pages' default address (`o7py.github.io/skim-site`) for now; a custom domain later if wanted.
3. **Approve the privacy wording** (section 5 of the page and `/privacy/`): three claims come from the specs, not the code (text sent to language models is redacted; course content is kept while the bot stays in the team; leaving a course removes your data for it).
4. **Collaborators and Google sign-in:** the Google consent screen is still in *Testing*, so each collaborator must be added as a test user (up to 100) until it is moved to production. This replaces T9/T10 for the public-download plan.
5. **Pricing:** nothing on the page until a plan exists.

## 12. Screenshots: what is used, what is missing
Processed by `tools/process_shots.py` (status bar cropped, carrier names repainted on the notification captures; nothing else touched). **Used:** teams, deck-change (hero), deck-important, detail, reminders (dark only), chat-anchored, important, notification-change and notification-newpost (as cards), all themed light/dark where both exist. **Not used:** `chat-open-light` (a long answer that listed Quiz 3 on two dates; looks inconsistent), `chat-open-dark`, `swipe-ask-dark` (spare), `starred-light` (spare; the file was named `reminders-light` but shows the Starred tab). **To retake for polish:** `reminders-light` (Starred, then Reminders, ideally one switch off): chapter 4 shows the dark screen on the light page until then; optionally `starred-dark`, `settings-*`, `offline-dark`, `swipe-dismiss-dark`.

## 13. Result (2026-10-27)
Lighthouse mobile: home 99 / 100 / 100 / 100, privacy 100 / 100 / 100 / 100; 203 KB transferred on a phone; layout shift 0; no third-party requests. The nav link reads "Who it's for" (the button is "Collaborate").
