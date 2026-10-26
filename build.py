#!/usr/bin/env python3
"""Builds the Skim site: plain static HTML/CSS/JS, no framework, no third-party requests. Run: python3 build.py  (then serve this folder)."""
import html, json, pathlib
ROOT = pathlib.Path(__file__).parent
C = json.loads((ROOT / 'site.json').read_text())
E = html.escape

# Event-type colours: the same hues the app uses (App/skim/src/constants/theme.ts), light / dark.
TYPES = [  # id, label, icon path (24px grid), light, dark, one line
    ('quiz', 'Quiz', 'M12 3a9 9 0 100 18 9 9 0 000-18zm0 13v.01M9.5 9.5a2.5 2.5 0 114 2c-.9.6-1.5 1-1.5 2', '#854D0E', '#FACC15'),
    ('exam', 'Exam', 'M7 3h7l5 5v13H7zM14 3v5h5M10 13h6M10 17h6', '#A21CAF', '#E879F9'),
    ('assignment', 'Assignment', 'M4 20l4-1 11-11-3-3L5 16zM14 6l3 3', '#1D4ED8', '#7DB4FB'),
    ('project', 'Project', 'M12 3l9 5-9 5-9-5zM3 13l9 5 9-5', '#7E22CE', '#CE9CFD'),
    ('lab', 'Lab', 'M9 3h6M10 3v6l-5 9a2 2 0 002 3h10a2 2 0 002-3l-5-9V3', '#3F6212', '#A3E635'),
    ('class', 'Class', 'M4 5h7a2 2 0 012 2v13a2 2 0 00-2-2H4zM20 5h-7', '#0369A1', '#38BDF8'),
    ('office_hours', 'Office hours', 'M5 21V4h9v17M14 8h5v13M10 12v.01', '#0F766E', '#2DD4BF'),
    ('presentation', 'Presentation', 'M3 4h18v12H3zM12 16v4M8 20h8', '#166534', '#4ADE80'),
    ('other', 'Other', 'M3 12l9-9h8v8l-9 9zM15 8v.01', '#475569', '#A3B1C6'),
]
ICONS = {
    'stack': 'M12 3l9 5-9 5-9-5zM3 13l9 5 9-5',
    'swipe': 'M5 12h14M15 8l4 4-4 4',
    'link': 'M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1',
    'calendar': 'M4 6h16v14H4zM4 10h16M8 3v4M16 3v4',
    'bell': 'M6 17V11a6 6 0 0112 0v6l2 2H4zM10 21h4',
    'alert': 'M12 4l9 16H3zM12 10v4M12 17v.01',
    'star': 'M12 3l2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 16.5 6.6 19.5l1.2-6L3.3 9.3l6.1-.7z',
    'moon': 'M20 14A8 8 0 1110 4a6 6 0 0010 10z',
    'wifi': 'M3 9a13 13 0 0118 0M6 12.5a8.5 8.5 0 0112 0M9.5 16a4 4 0 015 0M12 19.5v.01',
    'snooze': 'M12 7v5l3 2M5 3L2 6M19 3l3 3M12 21a8 8 0 100-16 8 8 0 000 16z',
    'user': 'M12 12a4 4 0 100-8 4 4 0 000 8zM4 21a8 8 0 0116 0',
    'lock': 'M6 11h12v10H6zM8 11V8a4 4 0 018 0v3',
    'trash': 'M4 7h16M9 7V4h6v3M6 7l1 14h10l1-14',
    'eye-off': 'M3 3l18 18M10.6 6.2A9.7 9.7 0 0112 6c5 0 9 6 9 6a15 15 0 01-3.2 3.7M6.6 7.6C4.3 9.3 3 12 3 12s4 6 9 6a9 9 0 003.4-.7',
    'phone': 'M7 3h10v18H7zM11 18h2',
    'down': 'M12 4v12M7 12l5 5 5-5M5 20h14',
}
def svg(path, cls=''):
    return f'<svg class="ic {cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="{path}"/></svg>'
def icon(name, cls=''): return svg(ICONS[name], cls)

FEATURES = [  # icon, title, text, optional type id for colour
    ('stack', 'One deck for every course', 'Real Teams messages, files and date changes from all your courses, in one swipeable stack.', None),
    ('swipe', 'Swipe to decide', 'Swipe left to dismiss (with undo). Swipe right to open the full card.', None),
    ('link', 'Open in Teams, open the file', 'Every card links back to the original message and any attached file.', None),
    ('calendar', 'Dates, spotted', 'Dates appear as chips. If Skim is not sure, the card says "Unconfirmed".', 'quiz'),
    ('bell', 'Reminders that follow the date', 'Recommended or custom reminders. When a date moves, your reminder moves with it.', 'class'),
    ('alert', 'Change alerts', 'A notification when a date, time or venue changes.', 'update'),
    ('star', 'Stars and temporary stars', 'Keep a card in Starred, or star it for a day or a week.', 'assignment'),
    ('snooze', 'Snooze', 'Bring a card back later, when you can deal with it.', 'lab'),
    ('calendar', 'Add to your calendar', 'Send an event to your phone calendar in one tap.', 'office_hours'),
    ('alert', 'The Important checklist', 'Pick the kinds of event that matter. They stand out in red.', 'important'),
    ('moon', 'Quiet hours, mute, urgent only', 'Silence a course, set quiet hours, or let only urgent alerts through.', 'project'),
    ('wifi', 'Works offline', 'Your latest cards stay readable without a connection.', 'presentation'),
]

def page(title, desc, path, body, extra_head=''):
    url = C['base_url'] + path
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#0F172A">
<link rel="canonical" href="{url}">
<link rel="icon" href="{{R}}assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{{R}}assets/favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="{{R}}assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{C['base_url']}/assets/og-image.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script>document.documentElement.className="js"</script>
<link rel="stylesheet" href="{{R}}assets/style.css">
{extra_head}</head>
<body>
{body}
<script src="{{R}}assets/site.js" defer></script>
</body>
</html>
'''

def header(root):
    return f'''<header class="top"><div class="wrap bar">
<a class="brand" href="{root}"><img src="{root}assets/logo.svg" width="32" height="32" alt=""><span>Skim</span></a>
<nav aria-label="Main"><a href="{root}#features">Features</a><a href="{root}#faq">FAQ</a><a href="{root}privacy/">Privacy</a></nav>
</div></header>'''

def footer(root):
    return f'''<footer class="foot"><div class="wrap">
<div class="foot-row"><span>Skim {E(C['version'])} · early preview, Android only</span>
<span><a href="{root}privacy/">Privacy</a> · <a href="mailto:{E(C['contact_email'])}">Contact</a></span></div>
<p class="small">Not affiliated with Microsoft. Microsoft Teams is a trademark of Microsoft. Skim is not official IISc software.</p>
</div></footer>'''

def phone(label, n=0):
    return f'''<figure class="phone" data-placeholder="true"><div class="phone-in"><div class="ph-note"><strong>{E(label)}</strong><span>Screenshot placeholder</span></div></div></figure>'''

def home():
    chips = ''.join(f'<li class="chip t-{t[0].replace("_","-")}">{svg(t[2])}{E(t[1])}</li>' for t in TYPES)
    feats = ''.join(
        f'<li class="feat reveal"><span class="fi {("t-"+f[3]) if f[3] else ""}">{icon(f[0])}</span><div><h3>{E(f[1])}</h3><p>{E(f[2])}</p></div></li>' for f in FEATURES)
    shots = ['The deck', 'Mid-swipe', 'Card details', 'Recommended reminders', 'Starred', 'Important checklist', 'A change alert', 'Settings']
    gallery = ''.join(f'<li>{phone(s)}<figcaption>{E(s)}</figcaption></li>' for s in shots)
    body = f'''{header('./')}
<main id="main">
<section class="hero"><div class="wrap hero-grid">
<div class="hero-copy">
<p class="badge"><span class="dot"></span>Preview · Android only</p>
<h1>Your course’s Teams, skimmed into cards.</h1>
<p class="lead">Skim reads your course team’s posts and files, spots the dates, and turns them into a swipeable deck with reminders and change alerts.</p>
<p class="cta"><a class="btn" href="{E(C['apk_url'])}">{icon('down')}Download for Android (APK)</a><a class="btn ghost" href="#how">How it works</a></p>
<p class="small">Version {E(C['version'])} · early preview, currently in testing</p>
</div>
<div class="hero-phone">{phone('The deck')}</div>
</div></section>

<section id="how" class="sec"><div class="wrap">
<h2>How it works</h2>
<ol class="steps">
<li class="reveal"><span class="n">1</span><h3>Your professor adds Skim</h3><p>The Skim bot is added to the course team once. It quietly records posts and files.</p></li>
<li class="reveal"><span class="n">2</span><h3>The bot posts a code</h3><p>A pairing code appears in the team, so only people in the course get it.</p></li>
<li class="reveal"><span class="n">3</span><h3>Enter it in the app</h3><p>Type the code in Skim and the course shows up as cards.</p></li>
</ol></div></section>

<section id="features" class="sec alt"><div class="wrap">
<h2>What it does today</h2>
<p class="sub">Every kind of event has its own colour, in the app and here.</p>
<ul class="chips" aria-label="Event colours">{chips}</ul>
<ul class="feats">{feats}</ul>
</div></section>

<section id="screens" class="sec"><div class="wrap">
<h2>See it</h2>
<ul class="gallery">{gallery}</ul>
</div></section>

<section id="privacy" class="sec alt"><div class="wrap">
<h2>Privacy, plainly</h2>
<ul class="priv">
<li>{icon('user')}<span><strong>What Skim stores about you:</strong> your Google email and name, your stars, reminders and swipe state, and your phone’s notification token.</span></li>
<li>{icon('eye-off')}<span><strong>Professors see nothing about students.</strong> There is no professor view of what you read or starred.</span></li>
<li>{icon('trash')}<span><strong>Delete your account any time</strong> in Settings. Everything stored about you is removed.</span></li>
<li>{icon('lock')}<span><strong>Private channels are never read.</strong> Skim only follows the standard channels of teams its bot was added to.</span></li>
<li>{icon('eye-off')}<span><strong>No trackers on this site.</strong> No analytics, no cookies, no third-party requests.</span></li>
</ul>
<p><a href="privacy/">Read the full privacy policy</a></p>
</div></section>

<section id="faq" class="sec"><div class="wrap narrow">
<h2>FAQ</h2>
<details><summary>Why Android only?</summary><p>Skim is an early preview built and tested on Android first. An iPhone version is not available yet.</p></details>
<details><summary>How do I install an APK?</summary><ol>
<li>Open this page on your Android phone and tap <em>Download for Android (APK)</em>.</li>
<li>When the download finishes, open the file. If Android asks, allow your browser to <em>install unknown apps</em> (Settings → Apps → your browser → Install unknown apps).</li>
<li>Tap <em>Install</em>, then open Skim and sign in with Google.</li>
<li>You can switch the unknown-apps permission off again afterwards.</li></ol></details>
<details><summary>Does my professor need to do anything?</summary><p>Yes, once: add the Skim bot to the course team. After that, nothing more. Students join with the code the bot posts.</p></details>
<details><summary>Is this official IISc software?</summary><p>No. Skim is an independent early preview. It is not offered, endorsed or supported by IISc or Microsoft.</p></details>
<details><summary>What if the date in a message is wrong?</summary><p>Skim can misread a message. That is why every card always shows the original message, and a date it is unsure of is marked <em>Unconfirmed</em>. Open in Teams shows you the source.</p></details>
</div></section>

<section class="sec alt"><div class="wrap narrow">
<h2>For professors</h2>
<p>Skim is not open for course installs yet; it is in early testing. If you would like to know more, or try it with a course, please get in touch.</p>
<p><a class="btn ghost" href="mailto:{E(C['contact_email'])}?subject=Skim%20for%20my%20course">Email us</a></p>
</div></section>
</main>
{footer('./')}'''
    return page('Skim: your course’s Teams, skimmed into cards', 'Skim turns your course’s Microsoft Teams posts and files into a swipeable deck with dates, reminders and change alerts. Early preview for Android.', '/', body)

def privacy():
    body = f'''{header('../')}
<main id="main"><div class="wrap narrow prose">
<h1>Privacy policy</h1>
<p class="small">Skim {E(C['version'])} · early preview. This page describes what the Skim app and its service actually do today.</p>

<h2>Who we are</h2>
<p>Skim is an independent early-preview project. It is not official IISc or Microsoft software. Contact: <a href="mailto:{E(C['contact_email'])}">{E(C['contact_email'])}</a>.</p>

<h2>What we collect, and why</h2>
<ul>
<li><strong>Your Google account email and name,</strong> from Google sign-in, to identify you and show your account.</li>
<li><strong>Your Skim activity:</strong> the courses you joined, which cards you dismissed or opened, your stars, snoozes and reminders, and your settings (quiet hours, mute, Important types). This makes the app work across your devices and is never shown to anyone else.</li>
<li><strong>Your push token:</strong> an identifier from Expo’s push service for your phone, used only to send you reminders and change alerts. Notification text contains no personal names.</li>
<li><strong>Course content:</strong> when a professor adds the Skim bot to a course team, Skim records the posts, edits, deletions, reactions and file changes in that team’s standard channels, and reads files’ text, to build cards. Private and shared channels are never read.</li>
</ul>
<p>Skim does not collect your location, contacts, or anything else from your phone. The only phone permissions asked for are notifications, exact alarms for reminders, and writing an event to your calendar when you ask for it.</p>

<h2>Who can see what</h2>
<p>Professors and course staff cannot see which cards you read, starred or dismissed, or any of your settings. There is no professor view of student activity. Joining a course needs the code posted in its team, and message author names are shown as Teams shows them.</p>

<h2>Where it is stored</h2>
<ul>
<li>Account data, course content and your activity are stored in a database on <strong>Supabase</strong>.</li>
<li>The Skim service runs on <strong>Google Cloud</strong> (Cloud Run, Mumbai region).</li>
<li>Your phone also keeps a copy of your latest cards and your settings for offline use.</li>
</ul>

<h2>Third parties</h2>
<ul>
<li><strong>Google sign-in</strong> verifies who you are (Google’s own policy applies to that step).</li>
<li><strong>Expo’s push service</strong> delivers notifications to your phone.</li>
<li><strong>Language models</strong> process redacted course text to find dates and categories. Personal identifiers such as email addresses are removed before text is sent.</li>
<li>Nothing is sold, and nothing is used for advertising. This website has no analytics, cookies or third-party requests; the APK download is served by GitHub.</li>
</ul>

<h2>How long we keep it</h2>
<p>Your account data is kept until you delete your account. Course content is kept while the Skim bot remains in that team. If you leave a course in the app, the cards, history, stars and reminders you had for it are removed from your account.</p>

<h2>Deleting your data</h2>
<p>In the app, open Settings → Delete account and confirm by typing the word shown. This removes your subscriptions, activity, reminders, push tokens and your sign-in account at once. You can also write to the contact address above.</p>

<h2>Changes</h2>
<p>If this policy changes, the new version is published here with a new date and app version.</p>
</div></main>
{footer('../')}'''
    return page('Privacy policy: Skim', 'What the Skim app stores, why, where, and how to delete it.', '/privacy/', body)

CSS = r'''
:root{--bg:#F3F6FB;--surface:#fff;--raised:#fff;--text:#0F172A;--muted:#475569;--border:#D3DBE8;--primary:#0369A1;--on-primary:#fff;--soft:#E0F2FE;--hero:#fff;
--t-quiz:#854D0E;--t-exam:#A21CAF;--t-assignment:#1D4ED8;--t-project:#7E22CE;--t-lab:#3F6212;--t-class:#0369A1;--t-office-hours:#0F766E;--t-presentation:#166534;--t-other:#475569;--t-update:#4338CA;--t-important:#B91C1C}
@media (prefers-color-scheme:dark){:root{--bg:#0F172A;--surface:#1B2235;--raised:#272E3F;--text:#F8FAFC;--muted:#B6C2D4;--border:#3A4254;--primary:#38BDF8;--on-primary:#0F172A;--soft:#18425A;--hero:#1B2235;
--t-quiz:#FACC15;--t-exam:#E879F9;--t-assignment:#7DB4FB;--t-project:#CE9CFD;--t-lab:#A3E635;--t-class:#38BDF8;--t-office-hours:#2DD4BF;--t-presentation:#4ADE80;--t-other:#A3B1C6;--t-update:#A5B4FC;--t-important:#FCA5A5}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--primary)}img,svg{max-width:100%}
.wrap{max-width:1080px;margin:0 auto;padding:0 16px}.narrow{max-width:760px}
.top{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--border)}
.bar{display:flex;align-items:center;justify-content:space-between;min-height:56px}
.brand{display:flex;align-items:center;gap:10px;color:var(--text);text-decoration:none;font-weight:800;font-size:20px}
nav a{margin-left:16px;color:var(--muted);text-decoration:none;font-weight:600;padding:12px 2px}nav a:hover{color:var(--text)}
.hero{padding:40px 0 24px}.hero-grid{display:grid;gap:32px;align-items:center}
@media(min-width:860px){.hero-grid{grid-template-columns:1.1fr .9fr}}
h1{font-size:clamp(32px,6vw,52px);line-height:1.08;margin:12px 0;letter-spacing:-.02em}
h2{font-size:clamp(24px,4vw,32px);margin:0 0 8px;letter-spacing:-.01em}h3{margin:0 0 4px;font-size:17px}
.lead{font-size:19px;color:var(--muted);max-width:34em}
.badge{display:inline-flex;gap:8px;align-items:center;margin:0;padding:4px 12px;border:1px solid var(--primary);color:var(--primary);border-radius:999px;font-weight:700;font-size:14px}
.badge .dot{width:8px;height:8px;border-radius:50%;background:currentColor}
.cta{display:flex;flex-wrap:wrap;gap:12px;margin:24px 0 8px}
.btn{display:inline-flex;align-items:center;gap:8px;min-height:48px;padding:0 22px;border-radius:999px;background:var(--primary);color:var(--on-primary);font-weight:700;text-decoration:none;transition:transform .15s,opacity .15s}
.btn:hover{transform:translateY(-1px)}.btn:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid var(--primary);outline-offset:3px}
.btn.ghost{background:transparent;color:var(--primary);border:1.5px solid var(--primary)}
.ic{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:none}
.small{font-size:14px;color:var(--muted)}
.sec{padding:56px 0}.sec.alt{background:var(--surface);border-block:1px solid var(--border)}.sub{color:var(--muted);margin:0 0 20px}
.steps{list-style:none;margin:24px 0 0;padding:0;display:grid;gap:16px}@media(min-width:760px){.steps{grid-template-columns:repeat(3,1fr)}}
.steps li{background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:20px}.steps p{margin:0;color:var(--muted)}
.n{display:grid;place-items:center;width:36px;height:36px;border-radius:50%;background:var(--soft);color:var(--primary);font-weight:800;margin-bottom:10px}
.chips{list-style:none;display:flex;flex-wrap:wrap;gap:8px;margin:0 0 28px;padding:0}
.chip{display:inline-flex;align-items:center;gap:6px;padding:4px 12px;border-radius:10px;font-weight:700;font-size:13px;color:var(--c);background:color-mix(in srgb,var(--c) 12%,var(--raised))}
.t-quiz{--c:var(--t-quiz)}.t-exam{--c:var(--t-exam)}.t-assignment{--c:var(--t-assignment)}.t-project{--c:var(--t-project)}.t-lab{--c:var(--t-lab)}.t-class{--c:var(--t-class)}.t-office-hours{--c:var(--t-office-hours)}.t-presentation{--c:var(--t-presentation)}.t-other{--c:var(--t-other)}.t-update{--c:var(--t-update)}.t-important{--c:var(--t-important)}
.chip .ic{width:15px;height:15px}
.feats{list-style:none;margin:0;padding:0;display:grid;gap:14px}@media(min-width:760px){.feats{grid-template-columns:repeat(2,1fr)}}@media(min-width:1000px){.feats{grid-template-columns:repeat(3,1fr)}}
.feat{display:flex;gap:14px;background:var(--bg);border:1px solid var(--border);border-radius:18px;padding:16px}.feat p{margin:0;color:var(--muted);font-size:15px}
.fi{display:grid;place-items:center;width:40px;height:40px;border-radius:12px;flex:none;color:var(--c,var(--primary));background:color-mix(in srgb,var(--c,var(--primary)) 14%,var(--raised))}
.feat.t-important{border-color:var(--t-important)}
.phone{margin:0 auto;width:min(260px,70vw);aspect-ratio:9/19;border-radius:34px;background:#0b1020;padding:9px;box-shadow:0 18px 40px rgba(2,6,23,.25)}
.phone-in{height:100%;border-radius:26px;background:var(--surface);display:grid;place-items:center;text-align:center;padding:16px;color:var(--muted);border:1px dashed var(--border)}
.ph-note{display:grid;gap:4px;font-size:14px}.ph-note strong{color:var(--text)}
.gallery{list-style:none;display:flex;gap:20px;overflow-x:auto;margin:20px 0 0;padding:8px 4px 20px;scroll-snap-type:x mandatory}
.gallery li{flex:none;width:200px;scroll-snap-align:start;text-align:center}.gallery .phone{width:200px}.gallery figcaption,.gallery li>figcaption{margin-top:8px;color:var(--muted);font-size:14px}
.priv{list-style:none;padding:0;margin:20px 0;display:grid;gap:14px}.priv li{display:flex;gap:12px;align-items:flex-start}.priv .ic{margin-top:4px;color:var(--primary)}
details{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:4px 18px;margin:10px 0}
summary{cursor:pointer;font-weight:700;padding:14px 0;min-height:48px}details[open] summary{border-bottom:1px solid var(--border);margin-bottom:10px}details p,details ol{color:var(--muted);margin:0 0 14px}
.foot{border-top:1px solid var(--border);padding:28px 0 40px;color:var(--muted)}.foot-row{display:flex;flex-wrap:wrap;gap:8px 24px;justify-content:space-between}
.prose{padding:32px 16px 56px}.prose h2{margin-top:32px}.prose li{margin:6px 0}
.js .reveal{opacity:0;transform:translateY(16px);transition:opacity .3s ease,transform .3s ease}.js .reveal.in{opacity:1;transform:none}
.hero-phone .phone{animation:rise .5s ease both}@keyframes rise{from{opacity:0;transform:translateY(24px)}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.js .reveal{opacity:1;transform:none;transition:none}.hero-phone .phone{animation:none}.btn{transition:none}}
'''
JS = '''(function(){
  var els=document.querySelectorAll('.reveal');
  if(!('IntersectionObserver' in window)||window.matchMedia('(prefers-reduced-motion: reduce)').matches){els.forEach(function(e){e.classList.add('in')});return;}
  var io=new IntersectionObserver(function(list){list.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{threshold:.15});
  els.forEach(function(e){io.observe(e)});
})();
'''
def write(rel, text):
    p = ROOT / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text)
write('index.html', home().replace('{R}', './'))
write('privacy/index.html', privacy().replace('{R}', '../'))
write('assets/style.css', CSS.strip() + '\n')
write('assets/site.js', JS)
write('.nojekyll', '')
write('robots.txt', f"User-agent: *\nAllow: /\nSitemap: {C['base_url']}/sitemap.xml\n")
write('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{C["base_url"]}/</loc></url><url><loc>{C["base_url"]}/privacy/</loc></url></urlset>\n')
print('built')
