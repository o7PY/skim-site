#!/usr/bin/env python3
"""Build skim-site/prep/index.html: one self-contained study page. Run: python3 tools/prep/build_prep.py
Fails if any identifier pattern (parse.LEAK) appears in the output."""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import parse, content_arch as A, content_study as S

OUT = HERE.parent.parent / 'prep'

ROUTE_DOC = {
 ('GET', '/api/v1/me'): 'Who am I: profile, settings, created on first call.',
 ('PATCH', '/api/v1/me/settings'): 'Change alert settings (new-post alerts, urgent only, quiet hours, reminder times).',
 ('DELETE', '/api/v1/me'): 'Delete the account: one delete cascades through every per-user table, then the sign-in user is removed.',
 ('POST', '/api/v1/subscriptions'): 'Join a course with its pairing code (rate limited: 10 tries an hour; 404/409/410/429).',
 ('GET', '/api/v1/subscriptions'): 'My courses, with colours and mute state.',
 ('PATCH', '/api/v1/subscriptions/{team_id}'): 'Mute or unmute a course; rename it for myself.',
 ('DELETE', '/api/v1/subscriptions/{team_id}'): 'Leave a course (its cards stop appearing).',
 ('GET', '/api/v1/deck'): 'The swipe deck: dealt cards, newest first, keyset cursor.',
 ('GET', '/api/v1/items/{id}'): 'One card in full, with its events, files and history. 404 if it is not in my courses.',
 ('POST', '/api/v1/items/{id}/state'): 'Dismiss, open, snooze or put back. Idempotent, so the offline outbox can retry.',
 ('PUT', '/api/v1/items/{id}/star'): 'Star a card (optionally temporary).',
 ('DELETE', '/api/v1/items/{id}/star'): 'Remove the star.',
 ('GET', '/api/v1/teams/{team_id}/cards'): 'Every card of one course, paged (the Teams tab).',
 ('GET', '/api/v1/history'): 'Dismissed and opened cards, newest first.',
 ('GET', '/api/v1/starred'): 'My starred cards.',
 ('GET', '/api/v1/reminders'): 'Fire times for the next 30 days (max 60): the device schedules local notifications from this.',
 ('GET', '/api/v1/reminders/all'): 'Every reminder with its time and on/off state, for the list in Starred.',
 ('PUT', '/api/v1/reminders/{id}'): 'Create a reminder (event + kind, an offset, or an absolute time).',
 ('PATCH', '/api/v1/reminders/{id}'): 'Switch a reminder off or on (the row is kept as a tombstone).',
 ('DELETE', '/api/v1/reminders/{id}'): 'Delete a reminder; automatic ones get a tombstone so they do not return.',
 ('POST', '/api/v1/devices'): 'Register an Expo push token (409 if another account holds an active one).',
 ('DELETE', '/api/v1/devices/{token}'): 'Unregister a push token (on sign-out).',
 ('GET', '/api/v1/sync'): 'Small catch-up call: what changed since last time.',
 ('POST', '/api/v1/chat'): 'Ask the course: scoped retrieval, redaction, a model, a post-check. 20/hour, 60/day. No transcripts stored.',
}

TABLE_NOTE = {
 'raw_activities': 'Every Teams activity stored untouched before any parsing (raw-first), with a dedupe key.',
 'teams': 'A course team the bot was added to, with its pairing code.',
 'messages': 'Normalised channel messages (current version, soft delete).',
 'message_versions': 'One row per edit, so history is never overwritten.',
 'events': 'Quizzes, exams, deadlines etc. found by the AI, with status, venue and confidence.',
 'event_changes': 'Old and new values whenever an event moves, is cancelled or changes venue.',
 'feed_items': 'The cards. One per message, file event or event change. Idempotent.',
 'user_item_state': 'Per student: dismissed, opened, snoozed, put back.',
 'reminders': 'Stored as intent (event + kind, or offset); fire times are computed.',
 'push_outbox': 'Alerts as rows first, sent later; one per user and thing (unique key).',
 'chat_usage': 'Only user id and a timestamp per accepted question, for the rate limit. No text.',
 'embeddings': 'vector(768) per message version or file chunk (pgvector).',
 'job_locks': 'The lease row that stops two run-all calls overlapping.',
 'join_attempts': 'Rate limiting for pairing-code guesses.',
 'devices': 'Expo push tokens per user.',
 'app_users': 'The student account row; every per-user table cascades from it.',
}

NUMBERS = [('34', 'database tables, all with row level security'), ('24', 'student API routes'), ('1,089', 'backend tests (with a real Postgres)'),
 ('483', 'app tests'), ('277', 'decisions logged with reasons'), ('54', 'labelled messages in the AI eval'), ('0', 'invented times in the eval (the target)'),
 ('15 min', 'heartbeat: Teams post to card to push'), ('768', 'embedding dimensions (pgvector)'), ('99-100', 'website Lighthouse scores'),
 ('~200 KB', 'website weight on a phone'), ('120', 'words max in a chat answer')]

FLOW = ['<b>A professor posts</b> in a standard channel of the course team. The Skim bot, added once, receives it.',
 '<b>Raw first:</b> the backend stores the untouched activity in Postgres before parsing anything.',
 '<b>Every 15 minutes</b> Cloud Scheduler runs the job chain: Graph sync, then AI (redact, classify, extract; code computes dates), then cards.',
 '<b>The student app</b> signs in with Google, swaps it for a Supabase token, and calls the API; the backend verifies the token.',
 '<b>Cards, reminders, alerts:</b> the deck, reminders computed from the event\'s current date, pushes through Expo and FCM.',
 '<b>Ask the course:</b> retrieval over the student\'s courses, redaction, a model, and a post-check that only allows cited facts.']

PITCH = S.QA[0]['a']

# The decisions worth defending in an interview (47 of 277). Pick by id; for ids that appear in both the
# spec table and the log, only the longer entry is flagged.
IMPORTANT = '''D-002 D-003 D-006 D-008 D-010 D-011 D-017
P2-D-105 P2-D-109 P2-D-110 P2-D-124 P2-D-132
P3-D-002 P3-D-003 P3-D-004 P3-D-005 P3-D-008 P3-D-010 P3-D-011 P3-D-012 P3-D-019 P3-D-020 P3-D-034 P3-D-036
P4-D-103 P4-D-105 P4-D-107 P4-D-119 P4-D-120 P4-D-121 P4-D-122 P4-D-127 P4-D-131 P4-D-134 P4-D-136 P4-D-150 P4-D-177
P5-D-6 P5-D-13 P5-D-14 P5-D-111 P5-D-117
P6A-D-001 P6A-D-003 P6A-D-005 P6A-D-006 P6A-D-012'''.split()

QTRY = {
 'teams': 'Notice the colour dot per course. Which table and column does that come from? (subscriptions)',
 'deck-change': 'Find the old and new date. Why can a reminder follow it without being rewritten?',
 'deck-important': 'Which parts are real Teams text and which are AI structure? Why does that matter?',
 'detail': 'Which actions need the network, and which go through the outbox?',
 'reminders': 'Why is a switched-off reminder kept instead of deleted?',
 'chat-anchored': 'Trace this answer: scope, retrieval, redaction, model, post-check. Which step names the course?',
 'important': 'Why are red hues reserved for "important" only?',
}

def main():
    dec = parse.parse_decisions()
    for d in dec:
        for k in ('text', 'why', 'title'):
            d[k] = parse.scrub(d[k])
    best = {}
    for d in dec:
        if d['id'] in IMPORTANT and len(d['text']) + len(d['why']) >= best.get(d['id'], (0, None))[0]:
            best[d['id']] = (len(d['text']) + len(d['why']), id(d))
    missing = [i for i in IMPORTANT if i not in best]
    if missing:
        sys.exit('important ids not found: %s' % missing)
    for d in dec:
        d['imp'] = d['id'] in best and best[d['id']][1] == id(d)
    routes = [dict(r, d=ROUTE_DOC.get((r['m'], r['p']), '')) for r in parse.parse_routes()]
    for r in routes:
        if not r['d']:
            sys.exit('missing route description: %s %s' % (r['m'], r['p']))
    tour = [dict(t, q=QTRY.get(t['img'], '')) for t in S.TOUR]
    data = dict(
        pitch=PITCH, numbers=NUMBERS, flow=FLOW, timeline=S.TIMELINE, groups=A.GROUPS, nodes=A.NODES, edges=A.EDGES,
        scenarios=A.SCENARIOS, jobs=A.JOBS, tables=parse.parse_migrations(), tablenotes=TABLE_NOTE, routes=routes,
        tour=tour, mech=S.MECHANISMS, decisions=dec,
        stories=S.STORIES, qa=S.QA, gloss=S.GLOSSARY, website=S.WEBSITE)
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    tpl = (HERE / 'src/template.html').read_text()
    html = tpl.replace('/*CSS*/', (HERE / 'src/prep.css').read_text()).replace('/*JS*/', (HERE / 'src/prep.js').read_text())
    html = html.replace('/*DATA*/null', blob)
    # leak scan (the SVG namespace string is not an identifier)
    scan = html.replace('http:/' + '/www.w3.org/2000/svg', '')
    bad = parse.leaks(scan)
    if bad:
        sys.exit('LEAK PATTERNS FOUND, not writing: %s' % bad)
    OUT.mkdir(exist_ok=True)
    (OUT / 'index.html').write_text(html)
    print('wrote', OUT / 'index.html', len(html) // 1024, 'KB;', len(dec), 'decisions;', len(routes), 'routes')

if __name__ == '__main__':
    main()
