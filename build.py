#!/usr/bin/env python3
"""Builds the Skim site from DESIGN_NEW.md: plain static HTML/CSS/JS, no framework, no third-party requests.
Run: python3 build.py  (then serve this folder). Content is in this file; the contact address is in site.json."""
import html, json, pathlib, urllib.parse
ROOT = pathlib.Path(__file__).parent
C = json.loads((ROOT / 'site.json').read_text())
E = html.escape
MAIL = C['contact_email']
MAILTO = 'mailto:' + MAIL + '?' + urllib.parse.urlencode({
    'subject': 'Collaborating on Skim',
    'body': 'Hi,\n\nI would like to collaborate on the testing phase of Skim.\n\nName:\nRole (professor / organisation / company):\nCourse or programme:\n'}, quote_via=urllib.parse.quote)

# ---- icons (Lucide-style outline, 24px grid) ---------------------------------------------------------------------------------
def svg(path, cls=''):
    return f'<svg class="ic {cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="{path}"/></svg>'
ICONS = {
    'star': 'M12 3l2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 16.5 6.6 19.5l1.2-6L3.3 9.3l6.1-.7z',
    'moon': 'M20 14A8 8 0 1110 4a6 6 0 0010 10z', 'wifi': 'M3 9a13 13 0 0118 0M6 12.5a8.5 8.5 0 0112 0M9.5 16a4 4 0 015 0M12 19.5v.01',
    'alert': 'M12 4l9 16H3zM12 10v4M12 17v.01', 'user': 'M12 12a4 4 0 100-8 4 4 0 000 8zM4 21a8 8 0 0116 0',
    'eye-off': 'M3 3l18 18M10.6 6.2A9.7 9.7 0 0112 6c5 0 9 6 9 6a15 15 0 01-3.2 3.7M6.6 7.6C4.3 9.3 3 12 3 12s4 6 9 6a9 9 0 003.4-.7',
    'trash': 'M4 7h16M9 7V4h6v3M6 7l1 14h10l1-14', 'lock': 'M6 11h12v10H6zM8 11V8a4 4 0 018 0v3',
    'mail': 'M3 6h18v12H3zM3 7l9 7 9-7', 'arrow': 'M5 12h14M13 6l6 6-6 6', 'down': 'M12 5v14M6 13l6 6 6-6',
    'school': 'M3 9l9-5 9 5-9 5zM7 11.5V16c0 1.5 2.2 3 5 3s5-1.5 5-3v-4.5', 'building': 'M4 21V5l8-2v18M12 9h8v12M7 9v.01M7 13v.01M7 17v.01M16 13v.01M16 17v.01',
    'cap': 'M12 4l10 5-10 5L2 9zM6 11.5V16c0 1.4 2.7 3 6 3s6-1.6 6-3v-4.5',
}
TYPES = [  # id, label, icon path
    ('quiz', 'Quiz', 'M12 3a9 9 0 100 18 9 9 0 000-18zm0 13v.01M9.5 9.5a2.5 2.5 0 114 2c-.9.6-1.5 1-1.5 2'),
    ('exam', 'Exam', 'M7 3h7l5 5v13H7zM14 3v5h5M10 13h6M10 17h6'), ('assignment', 'Assignment', 'M4 20l4-1 11-11-3-3L5 16zM14 6l3 3'),
    ('project', 'Project', 'M12 3l9 5-9 5-9-5zM3 13l9 5 9-5'), ('lab', 'Lab', 'M9 3h6M10 3v6l-5 9a2 2 0 002 3h10a2 2 0 002-3l-5-9V3'),
    ('class', 'Class', 'M4 5h7a2 2 0 012 2v13a2 2 0 00-2-2H4zM20 5h-7'), ('office-hours', 'Office hours', 'M5 21V4h9v17M14 8h5v13M10 12v.01'),
    ('presentation', 'Presentation', 'M3 4h18v12H3zM12 16v4M8 20h8'), ('other', 'Other', 'M3 12l9-9h8v8l-9 9zM15 8v.01'),
]

# ---- screenshots: the human's real ones, themed ------------------------------------------------------------------------------
SIZES = '(min-width: 860px) 300px, 70vw'
def pic(name, alt, eager=False, themed=True, extra=''):
    """A <picture> that follows the visitor's theme when a light and a dark version exist (otherwise the one that exists)."""
    def srcset(n): return f'assets/shots/{n}-295.webp 295w, assets/shots/{n}-590.webp 590w'
    light, dark = f'{name}-light', f'{name}-dark'
    have = lambda n: (ROOT / f'assets/shots/{n}-590.webp').exists()
    if themed and have(light) and have(dark):
        src = f'<source media="(prefers-color-scheme: dark)" srcset="{srcset(dark)}" sizes="{SIZES}">'; base = light
    else:
        src = ''; base = light if have(light) else dark if have(dark) else name
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture>{src}<img src="assets/shots/{base}-590.webp" srcset="{srcset(base)}" sizes="{SIZES}" width="590" height="1218" '
            f'alt="{E(alt)}" {load} decoding="async" {extra}></picture>')

STEPS = [  # screen shown while this step is active: (image name, alt)
    ('deck-change', 'The Skim deck: a quiz card marked important, showing the date moved from Fri 30 Oct to Sat 7 Nov.'),
    ('teams', 'The Teams tab: a list of your courses, each with its own colour dot.'),
    ('deck-important', 'A card for a new assignment, with Important, Assignment and Unconfirmed tags, the due date and an attached file.'),
    ('detail', 'An opened card: a date change, then actions for reminders, starring, snoozing, asking a question, and adding to the calendar.'),
    ('reminders', 'The Reminders list: each reminder with its time, its kind (automatic or recommended) and an on/off switch; two are switched off.'),
    ('chat-anchored', 'Ask the course: the question "Has this changed?" about a quiz card, answered with the new date and a source chip to open the card.'),
]
def phone_html(i, eager=False):
    name, alt = STEPS[i]
    return f'<div class="screen{" is-on" if i == 0 else ""}" data-screen="{i}">{pic(name, alt, eager=eager and i == 0)}</div>'
def inline_phone(i):
    name, alt = STEPS[i]
    return f'<div class="phone inline"><div class="bezel"><div class="inner">{pic(name, alt, eager=i == 0)}</div></div></div>'

def chips():
    return ''.join(f'<li class="chip c-{t[0]}">{svg(t[2])}{E(t[1])}</li>' for t in TYPES)

def page(title, desc, path, body):
    url = C['base_url'] + path
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#F0FDFA" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#081B1A" media="(prefers-color-scheme: dark)">
<meta name="color-scheme" content="light dark">
<link rel="canonical" href="{url}">
<link rel="icon" href="{{R}}assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="{{R}}assets/favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="{{R}}assets/apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{C['base_url']}/assets/og-image.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="{{R}}assets/fonts/outfit-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{{R}}assets/fonts/work-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
<script>document.documentElement.className="js"</script>
<link rel="stylesheet" href="{{R}}assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{body}
<script src="{{R}}assets/site.js" defer></script>
</body>
</html>
'''

def header(root):
    return f'''<header class="top"><div class="wrap bar">
<a class="brand" href="{root}" aria-label="Skim, home"><img src="{root}assets/logo.svg" width="32" height="32" alt=""><span>Skim</span></a>
<nav aria-label="Main"><a href="{root}#story">How it works</a><a href="{root}#demo">App demo</a><a href="{root}#collaborate">Who it’s for</a><a href="{root}#privacy">Privacy</a>
<a class="btn sm" href="{E(MAILTO)}">Collaborate</a></nav>
</div></header>'''

def footer(root):
    return f'''<footer class="foot"><div class="wrap">
<div class="foot-row"><span>Skim {E(C['version'])}</span>
<span><a href="{root}privacy/">Privacy</a> · <a href="{E(MAILTO)}">Contact</a></span></div>
<p class="small">Not affiliated with Microsoft; Microsoft Teams is a trademark of Microsoft. Skim is an independent project.</p>
</div></footer>'''

def home():
    chapters = [
        ('1', 'A professor posts in Teams.', 'Skim is added to the course team once. It quietly reads the standard channels, never private ones. You join your course with a code, and the course shows up in the app.', ''),
        ('2', 'It becomes a card.', 'Every post and file that matters becomes a card: the date, the files, a link back to the original. Each kind of event has its own colour, and red is kept for what is important.', f'<ul class="chips" aria-label="Event colours">{chips()}</ul>'),
        ('3', 'Swipe. Dismiss, open, or ask.', 'Swipe left to dismiss, with undo. Swipe right to open the full card, with reminders, stars, snooze and add-to-calendar. Swipe up to ask a question about it.', ''),
        ('4', 'Dates move. Skim follows.', 'Reminders move when a date moves, and every one has a switch. You get an alert when something changes, and when something new arrives, even with the app closed.',
         '<div class="notes"><img src="assets/shots/notification-change-card.webp" width="590" height="175" loading="lazy" alt="A notification: Quiz 1 moved, now Fri 30 Oct.">'
         '<img src="assets/shots/notification-newpost-card.webp" width="590" height="175" loading="lazy" alt="A notification: New, Quiz 1, Wed 28 Oct."></div>'),
        ('5', 'Ask the course.', 'Ask in plain words: “When is the next quiz?” Answers come only from your course messages, name the course, and show their sources so you can check them.', ''),
    ]
    chap_html = ''.join(
        f'<article class="chapter reveal" data-step="{i + 1}"><p class="num" aria-hidden="true">{n}</p><h2>{E(t)}</h2><p>{E(p)}</p>{extra}'
        f'{inline_phone(i + 1)}</article>' for i, (n, t, p, extra) in enumerate(chapters))
    pinned = ''.join(phone_html(i, eager=True) for i in range(len(STEPS)))
    tiles = f'''<ul class="tiles">
<li class="tile big reveal"><div><h3>The Important checklist</h3><p>Tick the kinds of event that matter. They stand out in red, can remind you automatically, and can alert you when a date moves.</p></div>
<div class="phone small"><div class="bezel"><div class="inner">{pic('important', 'The Important tab: nine event kinds with colour tags, some ticked.')}</div></div></div></li>
<li class="tile reveal"><span class="fi">{svg(ICONS['star'])}</span><h3>Starred</h3><p>Keep a card, or star it for a day or a week.</p></li>
<li class="tile reveal"><span class="fi">{svg(ICONS['moon'])}</span><h3>Quiet hours and mute</h3><p>Silence a course, set quiet hours, or let only the urgent through.</p></li>
<li class="tile reveal"><span class="fi">{svg(ICONS['wifi'])}</span><h3>Works offline</h3><p>Your latest cards stay readable without a connection.</p></li>
</ul>'''
    codes = ''.join(f'<li class="code">{E(x)}</li>' for x in C['demo_codes'])
    body = f'''{header('./')}
<main id="main">
<div class="story" id="story-wrap"><div class="wrap story-grid">
<div class="story-text">
<section class="hero chapter" data-step="0" aria-labelledby="h1">
<h1 id="h1">Swipe through your semester.</h1>
<p class="lead">Skim turns your course’s Teams posts and files into a deck of cards, with dates, reminders and alerts when a date moves.</p>
<p class="cta"><a class="btn" href="{E(MAILTO)}">Collaborate with us {svg(ICONS['arrow'])}</a><a class="btn ghost" href="#story">See how it works</a></p>
<p class="small">Works with courses where Skim has been added.</p>
{inline_phone(0)}
</section>
<div id="story">{chap_html}</div>
</div>
<div class="pin" aria-label="The Skim app" role="group"><div class="phone"><div class="bezel"><div class="inner" id="screens">{pinned}</div></div></div></div>
</div></div>

<section class="band"><div class="wrap"><h2 class="center">And the rest of it</h2>{tiles}</div></section>

<section id="demo" class="sec"><div class="wrap narrow">
<h2 class="center">App demo</h2>
<p class="sub center">Try Skim on an Android phone. This is an early test build, so Android asks you to allow installing it from your browser.</p>
<p class="cta center"><a class="btn" href="{E(C['apk_url'])}" download>{svg(ICONS['arrow'])}Download the app demo</a></p>
<p class="small center">{E(C['apk_label'])}</p>
<ol class="steps">
<li><strong>Install it.</strong> Open the downloaded file and allow “install unknown apps” if your phone asks.</li>
<li><strong>Sign in with Google.</strong></li>
<li><strong>Join a team.</strong> Tap Join and type one of these codes:</li>
</ol>
<ul class="codes">{codes}</ul>
</div></section>

<section id="collaborate" class="sec"><div class="wrap">
<h2 class="center">Let’s test it with your course.</h2>
<p class="sub center">Skim is in an early testing phase and currently works with courses where it has been added. We are collaborating with professors, organisations and companies. Plans for organisations are coming; we are not setting prices yet.</p>
<ul class="cards3">
<li class="card reveal"><span class="fi">{svg(ICONS['cap'])}</span><h3>Professors</h3><p>Add Skim to your course team once. Students join with a code. You never see what any student read, starred or asked.</p></li>
<li class="card reveal"><span class="fi">{svg(ICONS['building'])}</span><h3>Organisations and companies</h3><p>Pilot Skim with your team or programme during the testing phase and shape what it becomes. Subscription plans are on the way.</p></li>
<li class="card reveal"><span class="fi">{svg(ICONS['user'])}</span><h3>Students</h3><p>Skim works when your professor adds it to your course team. Send them this page, or write to us and we will reach out.</p></li>
</ul>
<p class="cta center"><a class="btn" href="{E(MAILTO)}">{svg(ICONS['mail'])}Collaborate with us</a></p>
<p class="small center">Or write to <a href="{E(MAILTO)}">{E(MAIL)}</a></p>
</div></section>

<section id="privacy" class="band"><div class="wrap narrow">
<h2>Privacy, plainly</h2>
<ul class="priv">
<li>{svg(ICONS['user'])}<span><strong>What Skim stores about you:</strong> your Google email and name, your stars, reminders and swipe state, and your phone’s notification token.</span></li>
<li>{svg(ICONS['eye-off'])}<span><strong>Professors see nothing about students.</strong> There is no professor view of what you read, starred or asked.</span></li>
<li>{svg(ICONS['lock'])}<span><strong>Private channels are never read.</strong> Skim only follows the standard channels of teams its bot was added to.</span></li>
<li>{svg(ICONS['trash'])}<span><strong>Delete your account any time</strong> in Settings. Everything stored about you is removed.</span></li>
<li>{svg(ICONS['eye-off'])}<span><strong>No trackers on this site.</strong> No analytics, no cookies, no third-party requests.</span></li>
</ul>
<p><a href="privacy/">Read the full privacy policy</a></p>
</div></section>
</main>
{footer('./')}'''
    return page('Skim: swipe through your semester', 'Skim turns your course’s Microsoft Teams posts and files into a deck of cards with dates, reminders and alerts when a date moves. Early preview, Android, in testing.', '/', body)

def privacy():
    body = f'''{header('../')}
<main id="main"><div class="wrap narrow prose">
<h1>Privacy policy</h1>
<p class="small">Skim {E(C['version'])} · early preview. This page describes what the Skim app and its service actually do today.</p>
<h2>Who we are</h2>
<p>Skim is an independent early-preview project, not official IISc or Microsoft software. Contact: <a href="{E(MAILTO)}">{E(MAIL)}</a>.</p>
<h2>What we collect, and why</h2>
<ul>
<li><strong>Your Google account email and name,</strong> from Google sign-in, to identify you and show your account.</li>
<li><strong>Your Skim activity:</strong> the courses you joined, which cards you dismissed or opened, your stars, snoozes and reminders, and your settings (quiet hours, mute, new-post alerts, important kinds). This makes the app work across your devices and is never shown to anyone else.</li>
<li><strong>Your push token:</strong> an identifier from Expo’s push service for your phone, used only to send you reminders and alerts (a date that moved, a new post or file). Notification text holds course and event details only, never people’s names or message text.</li>
<li><strong>Course content:</strong> when a professor adds the Skim bot to a course team, Skim records the posts, edits, deletions, reactions and file changes in that team’s standard channels, and reads files’ text, to build cards. Private and shared channels are never read.</li>
<li><strong>Your questions to “Ask the course”:</strong> a question and the relevant course text are sent, with names, emails, phone numbers and roll numbers replaced, to a language-model provider to write the answer. The question and the answer are not stored on our server; we keep only the time of each question, to limit how many can be asked per hour.</li>
</ul>
<p>Skim does not collect your location, contacts, or anything else from your phone. The only phone permissions asked for are notifications, exact alarms for reminders, and writing an event to your calendar when you ask for it.</p>
<h2>Who can see what</h2>
<p>Professors and course staff cannot see which cards you read, starred, dismissed or asked about, or any of your settings. There is no professor view of student activity. Joining a course needs the code posted in its team, and message author names are shown as Teams shows them.</p>
<h2>Where it is stored</h2>
<ul><li>Account data, course content and your activity are stored in a database on <strong>Supabase</strong>.</li><li>The Skim service runs on <strong>Google Cloud</strong> (Cloud Run, Mumbai region).</li><li>Your phone also keeps a copy of your latest cards and your settings for offline use.</li></ul>
<h2>Third parties</h2>
<ul><li><strong>Google sign-in</strong> verifies who you are (Google’s own policy applies to that step).</li><li><strong>Expo’s push service</strong> delivers notifications to your phone.</li><li><strong>Language-model providers</strong> process redacted course text to find dates and categories, and to answer your questions.</li><li>Nothing is sold, and nothing is used for advertising. This website has no analytics, cookies or third-party requests.</li></ul>
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
@font-face{font-family:Outfit;src:url(fonts/outfit-latin.woff2) format("woff2");font-weight:100 900;font-display:swap}
@font-face{font-family:"Work Sans";src:url(fonts/work-sans-latin.woff2) format("woff2");font-weight:100 900;font-display:swap}
:root{--bg:#F0FDFA;--paper:#fff;--soft:#E6F7F4;--ink:#0B2B29;--muted:#44625F;--hair:#CFE5E1;--teal:#0F766E;--teal-bright:#0D9488;--teal-soft:#CCFBF1;--amber:#F59E0B;--amber-deep:#D97706;--on-amber:#1C1917;--frame:#12302D;--phone-shadow:0 28px 60px rgba(8,27,26,.18);
--c-quiz:#854D0E;--c-exam:#A21CAF;--c-assignment:#1D4ED8;--c-project:#7E22CE;--c-lab:#3F6212;--c-class:#0369A1;--c-office-hours:#0F766E;--c-presentation:#166534;--c-other:#475569;
--head:Outfit,system-ui,sans-serif;--body:"Work Sans",system-ui,sans-serif}
@media (prefers-color-scheme:dark){:root{--bg:#081B1A;--paper:#0F2927;--soft:#143532;--ink:#ECFDF5;--muted:#A3C2BE;--hair:#1F4A46;--teal:#2DD4BF;--teal-bright:#2DD4BF;--teal-soft:#134E4A;--amber:#FBBF24;--amber-deep:#F59E0B;--frame:#02100F;--phone-shadow:0 28px 60px rgba(0,0,0,.5);
--c-quiz:#FACC15;--c-exam:#E879F9;--c-assignment:#7DB4FB;--c-project:#CE9CFD;--c-lab:#A3E635;--c-class:#38BDF8;--c-office-hours:#2DD4BF;--c-presentation:#4ADE80;--c-other:#A3B1C6}}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:72px}
body{margin:0;background:var(--bg);color:var(--ink);font:400 17px/1.6 var(--body);-webkit-font-smoothing:antialiased}
img{max-width:100%;height:auto;display:block}a{color:var(--teal)}
.skip{position:absolute;left:-999px;top:8px;background:var(--paper);color:var(--ink);padding:10px 16px;border-radius:999px;z-index:20}.skip:focus{left:8px}
:focus-visible{outline:3px solid var(--teal);outline-offset:3px;border-radius:6px}
.wrap{max-width:1120px;margin:0 auto;padding:0 24px}.narrow{max-width:760px}.center{text-align:center}.small{font-size:14px;color:var(--muted)}
h1,h2,h3{font-family:var(--head);margin:0;color:var(--ink)}
h1{font-weight:700;font-size:clamp(40px,7vw,72px);line-height:1.04;letter-spacing:-.025em}
h2{font-weight:600;font-size:clamp(28px,4.5vw,44px);line-height:1.1;letter-spacing:-.02em}
h3{font-weight:600;font-size:22px;line-height:1.25}
.top{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--hair)}
.bar{display:flex;align-items:center;justify-content:space-between;min-height:64px}
.brand{display:flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;font:700 22px var(--head)}
nav{display:flex;align-items:center;gap:20px}nav a:not(.btn){color:var(--muted);text-decoration:none;font-weight:500;padding:12px 2px}nav a:not(.btn):hover{color:var(--ink)}
.btn{display:inline-flex;align-items:center;gap:10px;min-height:52px;padding:0 26px;border-radius:999px;background:var(--amber);color:var(--on-amber);font:600 17px var(--body);text-decoration:none;transition:background-color .15s}
.btn:hover{background:var(--amber-deep)}.btn.sm{min-height:44px;padding:0 20px;font-size:15px}
.btn.ghost{background:transparent;color:var(--teal);border:1.5px solid var(--teal)}.btn.ghost:hover{background:var(--teal-soft)}
.ic{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:none}
.badge{display:inline-flex;gap:8px;align-items:center;margin:0 0 20px;padding:5px 14px;border-radius:999px;background:var(--teal-soft);color:var(--teal);font-weight:600;font-size:14px}
.badge .dot{width:8px;height:8px;border-radius:50%;background:currentColor}
.lead{font-size:clamp(18px,2.4vw,21px);color:var(--muted);max-width:30em;margin:20px 0 0}
.cta{display:flex;flex-wrap:wrap;gap:12px;margin:28px 0 12px}.cta.center{justify-content:center}
.story-grid{display:grid;grid-template-columns:1fr;gap:0}
.story-text{min-width:0}
.hero{padding:56px 0 24px}.chapter{padding:24px 0 24px}
.chapter .num{font:700 64px/1 var(--head);color:var(--teal-bright);margin:0 0 8px;opacity:.9}
.chapter h2{font-size:clamp(28px,4vw,40px);margin-bottom:12px}.chapter p{margin:0 0 12px;color:var(--muted);max-width:32em}
.hero .lead{margin-top:20px}
.chips{list-style:none;display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 0;padding:0}
.chip{display:inline-flex;align-items:center;gap:6px;padding:4px 12px;border-radius:10px;font-weight:600;font-size:13px;color:var(--c);background:color-mix(in srgb,var(--c) 12%,var(--paper))}.chip .ic{width:15px;height:15px}
.c-quiz{--c:var(--c-quiz)}.c-exam{--c:var(--c-exam)}.c-assignment{--c:var(--c-assignment)}.c-project{--c:var(--c-project)}.c-lab{--c:var(--c-lab)}.c-class{--c:var(--c-class)}.c-office-hours{--c:var(--c-office-hours)}.c-presentation{--c:var(--c-presentation)}.c-other{--c:var(--c-other)}
.notes{display:grid;gap:10px;margin-top:16px;max-width:420px}.notes img{border-radius:20px;border:1px solid var(--hair)}
/* the phone */
.phone{width:min(300px,72vw);margin:0 auto}.phone.small{width:min(240px,60vw)}
.bezel{background:var(--frame);border-radius:34px;padding:8px;box-shadow:var(--phone-shadow);border:1px solid var(--hair)}
.inner{position:relative;border-radius:26px;overflow:hidden;aspect-ratio:590/1218;background:var(--soft)}
.inner img{width:100%;height:100%;object-fit:cover}
.inline{margin:24px auto 8px}
.pin{display:none}
@media (min-width:860px){
 .story-grid{grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);column-gap:56px}
 .pin{display:flex;align-items:center;justify-content:center;position:sticky;top:64px;height:calc(100vh - 64px);align-self:start;order:2}
 .pin .phone{width:min(300px,calc((100vh - 144px) * .4844 + 16px));margin:0}
 .story-text{order:1}.inline{display:none}
 .hero,.chapter:not(.hero){min-height:calc(100vh - 64px);display:flex;flex-direction:column;justify-content:center}
 .hero{padding-top:0;padding-bottom:0}.chapter:not(.hero){padding:0}
 .screen{position:absolute;inset:0;opacity:0;transition:opacity .25s ease}.screen.is-on{opacity:1}
 .screen picture,.screen img{width:100%;height:100%}
}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}.pin{display:none!important}.inline{display:block!important}.chapter:not(.hero),.hero{min-height:0!important}.screen{transition:none}.js .reveal{opacity:1!important;transform:none!important;transition:none!important}.btn{transition:none}}
.band{background:var(--soft);border-block:1px solid var(--hair);padding:80px 0}.sec{padding:88px 0}
.tiles{list-style:none;margin:40px 0 0;padding:0;display:grid;gap:16px}
@media (min-width:760px){.tiles{grid-template-columns:repeat(3,1fr);grid-auto-rows:auto}.tile.big{grid-column:span 3}}
.tile{background:var(--paper);border:1px solid var(--hair);border-radius:24px;padding:24px}.tile p{margin:6px 0 0;color:var(--muted)}
.tile.big{display:grid;gap:20px;align-items:center}@media (min-width:760px){.tile.big{grid-template-columns:1.2fr .8fr;padding:32px 40px}}
.fi{display:grid;place-items:center;width:44px;height:44px;border-radius:14px;background:var(--teal-soft);color:var(--teal);margin-bottom:14px}
.sub{max-width:44em;margin:16px auto 0;color:var(--muted)}
.cards3{list-style:none;margin:40px 0 32px;padding:0;display:grid;gap:16px}@media (min-width:860px){.cards3{grid-template-columns:repeat(3,1fr)}}
.steps{margin:24px auto;padding-left:22px;max-width:560px;display:grid;gap:10px}.steps li::marker{color:var(--teal);font-weight:700}
.codes{list-style:none;margin:16px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:12px;justify-content:center}
.code{font:700 22px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;letter-spacing:.14em;padding:12px 20px;border-radius:14px;background:var(--teal-soft);color:var(--teal);border:1px solid var(--hair);user-select:all}
.card{background:var(--paper);border:1px solid var(--hair);border-radius:24px;padding:28px}.card p{margin:8px 0 0;color:var(--muted)}
.priv{list-style:none;padding:0;margin:24px 0;display:grid;gap:16px}.priv li{display:flex;gap:14px;align-items:flex-start}.priv .ic{margin-top:4px;color:var(--teal)}
.foot{padding:36px 0 48px;color:var(--muted)}.foot-row{display:flex;flex-wrap:wrap;gap:8px 24px;justify-content:space-between}
.prose{padding:48px 24px 72px}.prose h1{font-size:clamp(34px,5vw,48px)}.prose h2{margin-top:36px;font-size:26px}.prose li{margin:8px 0}
.js .reveal{opacity:0;transform:translateY(16px);transition:opacity .3s ease,transform .3s ease}.js .reveal.in{opacity:1;transform:none}
@media (max-width:640px){nav a:not(.btn){display:none}.wrap{padding:0 16px}.sec,.band{padding:56px 0}}
'''
JS = '''(function(){
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var els=document.querySelectorAll('.reveal');
  if(!('IntersectionObserver' in window)||reduce){els.forEach(function(e){e.classList.add('in')});}
  else{var io=new IntersectionObserver(function(l){l.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{threshold:.12});els.forEach(function(e){io.observe(e)});}
  /* the pinned phone shows the screen of the chapter that is crossing the middle of the viewport */
  var screens=document.querySelectorAll('.screen'),chapters=document.querySelectorAll('.chapter[data-step]');
  if(!screens.length||!('IntersectionObserver' in window)||reduce)return;
  function show(n){screens.forEach(function(s){var on=s.getAttribute('data-screen')===String(n);s.classList.toggle('is-on',on);s.setAttribute('aria-hidden',on?'false':'true');});}
  show(0);
  var so=new IntersectionObserver(function(l){l.forEach(function(e){if(e.isIntersecting)show(e.target.getAttribute('data-step'));})},{rootMargin:'-45% 0px -45% 0px',threshold:0});
  chapters.forEach(function(c){so.observe(c)});
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
