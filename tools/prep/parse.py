"""Facts pulled straight from the project so the prep page cannot drift from the code: the decision log, the migrations (tables and
columns) and the student API routes. Everything that leaves this module is scrubbed of identifiers (see LEAK)."""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]        # SkimForTeams/
DOCS = REPO / 'Bookkeeping'

# Things that must never appear on a page that may end up public: ids, hosts, addresses, secrets-shaped strings, names of accounts.
LEAK = [r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', r'https?://[^\s)\]>"\']+', r'[\w.+-]+@[\w-]+\.[\w.-]+', r'\b[0-9a-f]{32,}\b',
        r'R6BVE4', r'wbUft3CHDZ', r'152992146915', r'jrgdnppvffsqdkghmbhd', r'pragnya', r'c7014744', r'sb_publishable\w*', r'AIza\w{20,}',
        r'eyJ[\w-]{20,}', r'xox[bp]-\w+', r'ghp_\w{20,}', r'ExponentPushToken\[[^\]]+\]']

def scrub(text: str) -> str:
    t = text or ''
    t = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '[id]', t)
    t = re.sub(r'https?://[^\s)\]>"\']+', '[url]', t)
    t = re.sub(r'[\w.+-]+@[\w-]+\.[\w.-]+', '[email]', t)
    t = re.sub(r'\b[0-9a-f]{32,}\b', '[hash]', t)
    for word in ('R6BVE4', 'wbUft3CHDZ', '152992146915', 'jrgdnppvffsqdkghmbhd', 'c7014744'):
        t = t.replace(word, '[redacted]')
    t = re.sub(r'(?i)pragnya\w*', 'the human', t)
    return t

def leaks(text: str) -> list[str]:
    return [p for p in LEAK if re.search(p, text)]

def md_inline(t: str) -> str:
    """Keep the text readable: strip backticks and bold markers; keep it plain (the page escapes everything)."""
    t = re.sub(r'`([^`]*)`', r'\1', t); t = re.sub(r'\*\*([^*]+)\*\*', r'\1', t)
    return re.sub(r'\s+', ' ', t).strip()

PHASE = {'': '1', 'P2-': '2', 'P3-': '3', 'P4-': '4', 'P5-': '5', 'P6A-': '6A'}
TAGS = [('security', r'rls|row level|jwt|jwks|auth|token|secret|privacy|redact|permission|consent|rsc|cascade|delete|never read|private'),
        ('ai', r'llm|gemini|groq|model|prompt|embedding|classif|extract|confidence|redactor|eval|retriev|chat|citation'),
        ('push', r'push|notification|expo push|fcm|alert|quiet hours|reminder'),
        ('app', r'app\b|android|expo|react|reanimated|swipe|deck|gesture|screen|tab|offline|outbox|eas|ota|update'),
        ('data', r'postgres|database|migration|table|index|pgvector|supabase|schema|storage|sql|dedupe|idempot'),
        ('infra', r'cloud run|cloud build|scheduler|deploy|docker|container|pooler|github|pages|secret manager'),
        ('design', r'palette|colour|color|theme|design|motion|animation|logo|font|contrast|screenshot|website|site'),
        ('process', r'spec|test|decision|log|diff|commit|push|review|spike|acceptance|sdd')]

def tags_for(text: str) -> list[str]:
    low = text.lower(); out = [n for n, rx in TAGS if re.search(rx, low)]
    return out[:4]

def parse_decisions() -> list[dict]:
    """184 entries of the decision log + the pre-made decision tables of the specs (the human's)."""
    raw = (DOCS / 'DECISIONS.md').read_text()
    blocks = re.split(r'(?m)^(?=#{2,3} (?:P\d+[A-Z]?-)?D-\d+)', raw)
    out = []
    for b in blocks:
        m = re.match(r'#{2,3} ((?:P\d+[A-Z]?-)?D-\d+)\s*[:—-]+\s*(.*)\n', b)
        if not m:
            continue
        did, title = m.group(1), md_inline(m.group(2))
        title = re.sub(r'\s*\((\d{4}-\d{2}-\d{2}[^)]*)\)\s*$', '', title)
        body = b[m.end():].strip()
        fields = dict(re.findall(r'(?m)^- ([A-Za-z ]+): (.*)$', body))
        date = fields.get('Date') or (re.search(r'\((\d{4}-\d{2}-\d{2})', m.group(2)) or [None, ''])[1]
        if fields.get('Decision'):
            summary, why = md_inline(fields['Decision']), md_inline(fields.get('Why', ''))
            by = md_inline(fields.get('Made by', ''))
        else:
            paras = [p for p in re.split(r'\n\s*\n', body) if p.strip()]
            text = md_inline(' '.join(paras))
            by = (re.match(r'Made by: ([^.]*)\.', text) or [None, ''])[1]
            text = re.sub(r'^Made by: [^.]*\.\s*', '', text)
            summary, why = text, ''
        prefix = re.match(r'((?:P\d+[A-Z]?-)?)D-', did).group(1)
        out.append({'id': did, 'phase': PHASE.get(prefix, prefix.strip('-')), 'src': 'log', 'title': scrub(title), 'date': date or '', 'by': scrub(by),
                    'text': scrub(summary)[:900], 'why': scrub(why)[:500], 'tags': tags_for(title + ' ' + summary)})
    for f, ph in (('PHASE2.md', '2'), ('PHASE3.md', '3'), ('PHASE4.md', '4'), ('PHASE5.md', '5')):
        for did, text in re.findall(r'(?m)^\| ((?:P\d+[A-Z]?-)D-\d+) \| (.*) \|\s*$', (DOCS / f).read_text()):
            text = md_inline(text); title = re.split(r'[.:]\s', text, 1)[0][:90]
            out.append({'id': did, 'phase': ph, 'src': 'spec', 'title': scrub(title), 'date': '', 'by': 'the human (spec)', 'text': scrub(text)[:900], 'why': '', 'tags': tags_for(text)})
    return out

def parse_migrations() -> list[dict]:
    """Tables, columns and foreign keys from migrations/*.sql."""
    tables = []
    for f in sorted((REPO / 'migrations').glob('*.sql')):
        sql = f.read_text(); phase = f.name[:3]
        for m in re.finditer(r'create table if not exists (\w+) \((.*?)\n\);', sql, re.S):
            name, body = m.group(1), m.group(2)
            cols, fks = [], []
            for line in body.split('\n'):
                line = line.split('--')[0].strip().rstrip(',')
                if not line or re.match(r'(primary key|unique|check|constraint|\(|and |or )', line, re.I):
                    continue
                cm = re.match(r'(\w+)\s+([\w\[\]()]+(?:\s+\w+)?)', line)
                if not cm:
                    continue
                cname, ctype = cm.group(1), cm.group(2).split()[0]
                ref = re.search(r'references (\w+)\(', line)
                if ref:
                    fks.append({'col': cname, 'to': ref.group(1)})
                cols.append({'n': cname, 'type': ctype, 'pk': 'primary key' in line, 'nn': 'not null' in line, 'fk': ref.group(1) if ref else ''})
            tables.append({'name': name, 'mig': f.name, 'cols': cols, 'fks': fks})
    return tables

def parse_routes() -> list[dict]:
    """The student API: method and path of every route registered under /api/v1."""
    out = []
    for f in ('routes.py', 'routes_items.py', 'routes_reminders.py', 'routes_devices.py', 'routes_chat.py'):
        src = (REPO / 'src/skim/api' / f).read_text()
        for m in re.finditer(r'\.add_(get|post|put|patch|delete)\(\s*"([^"]+)"', src):
            out.append({'m': m.group(1).upper(), 'p': '/api/v1' + m.group(2), 'file': f})
    return out

if __name__ == '__main__':
    d = parse_decisions(); t = parse_migrations(); r = parse_routes()
    from collections import Counter
    print(len(d), Counter((x['phase'], x['src']) for x in d))
    print(len(t), 'tables;', len(r), 'routes')
    print([x['name'] for x in t])
    print(sum(len(x['text']) + len(x['why']) for x in d) // 1024, 'KB of decision text')
    print([ (x['m'],x['p']) for x in r][:6])
    bad = [(x['id'], leaks(x['text'] + x['why'] + x['title'])) for x in d if leaks(x['text'] + x['why'] + x['title'])]
    print('leaks after scrub:', bad[:5])
