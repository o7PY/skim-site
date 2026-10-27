"""raw-screenshots/*.jpeg (the human's phone, 590x1280) -> assets/shots/*.webp at 590 and 295 px wide.
Crops the phone's status bar (it holds notification icons, carrier names and media chips) and keeps the bottom gesture bar for margin
inside the rounded frame. Notification captures: the carrier row is repainted from the smooth blurred wallpaper around it, and the
real notification itself is also exported as a card. Nothing else is changed: the screenshots stay real (P5-D-118).
    python3 tools/process_shots.py"""
from PIL import Image
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW, OUT = f'{ROOT}/raw-screenshots/', f'{ROOT}/assets/shots/'
TOP, BOT = 62, 1280
SKIP = ('chat-open',)                                   # a long answer that read as inconsistent: not used
RENAME = {}

def inpaint_band(im, y0, y1):
    px = im.load(); w, _ = im.size
    a = [px[x, y0 - 1] for x in range(w)]; b = [px[x, y1 + 1] for x in range(w)]
    for y in range(y0, y1 + 1):
        t = (y - y0 + 1) / (y1 - y0 + 2)
        for x in range(w):
            px[x, y] = tuple(round(a[x][i] * (1 - t) + b[x][i] * t) for i in range(3))

def save(im, name):
    for w in (590, 295):
        r = im if w == 590 else im.resize((295, round(im.height * 295 / 590)), Image.LANCZOS)
        r.save(f'{OUT}{name}-{w}.webp', 'WEBP', quality=82, method=6)

os.makedirs(OUT, exist_ok=True)
for f in sorted(os.listdir(RAW)):
    if not f.endswith(('.jpeg', '.jpg', '.png')) or f.startswith(SKIP):
        continue
    name = os.path.splitext(f)[0].strip(); im = Image.open(RAW + f).convert('RGB')
    if name.startswith('notification'):
        inpaint_band(im, 44, 96)
        im.crop((0, 170, 590, 345)).save(f'{OUT}{name}-card.webp', 'WEBP', quality=84, method=6)
    save(im.crop((0, TOP, 590, BOT)), RENAME.get(name, name))
