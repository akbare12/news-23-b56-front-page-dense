#!/usr/bin/env python3
"""news-23 b56 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
DJ_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
DJ_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DJ_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
LIB_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
LIB_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

def f(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (212, 175, 55)
RED = (178, 34, 34)
DARKRED = (139, 0, 0)
TEAL = (0, 128, 128)
BLUE = (0, 51, 102)
NAVY = (10, 25, 60)
GRAY = (110, 110, 110)
DARKGRAY = (60, 60, 60)
LIGHTGRAY = (235, 235, 235)
CREAM = (250, 244, 225)
PURPLE = (102, 51, 153)
GREEN = (34, 139, 34)
ORANGE = (230, 126, 34)

def text(x, y, s, font, fill=BLACK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def wrap(s, font, maxw):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def chip(x, y, label, color):
    # x,y = top-left of chip; returns width
    font = f(LIB_SANS_B, 10)
    w = int(d.textlength(label, font=font)) + 10
    d.rounded_rectangle([x, y, x + w, y + 12], radius=2, fill=color)
    d.text((x + 5, y + 1), label, font=font, fill=WHITE)
    return w

# ---------------- masthead ----------------
d.rectangle([0, 0, W, 58], fill=BLACK)
text(16, 6, "THE WORLD TODAY", f(DJ_SERIF_B, 44), WHITE)
text(W - 16, 20, "MONDAY 23 NOVEMBER 2026", f(LIB_SANS_B, 17), GOLD, anchor="ra")

# ---------------- kicker ----------------
text(16, 62, "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
     f(LIB_SANS_B, 14), RED)

# ---------------- number strip: 2 rows x 5 ----------------
numbers = [
    ("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", BLUE),
    ("11,762", "EBOLA CASES, DRC", GREEN), ("10T won", "SEOUL STABILISATION FUND", (150, 110, 0)),
    ("2%", "BILLIONAIRE TAX IN PARIS", PURPLE),
    ("$450M", "SKUBAL DEAL", PURPLE), ("165", "RUSSIAN MISSILES IN A WEEK", RED),
    ("12,000", "CLEARED IN MANCHESTER", BLUE), ("264 kg", "EXPLOSIVES SEIZED IN LEBANON", (150, 110, 0)),
    ("$107.3B", "ANTHROPIC IPO \u2014 LARGEST", PURPLE),
]
for i, (val, lab, col) in enumerate(numbers):
    row, c = divmod(i, 5)
    x = c * 205 + 8
    y = 78 + row * 36
    text(x, y, val, f(LIB_SANS_B, 18), col)
    text(x, y + 21, lab, f(LIB_SANS_B, 10), BLACK)
d.line([0, 150, W, 150], fill=LIGHTGRAY, width=1)

# ---------------- region bar ----------------
regions = [("ASIA-PACIFIC 7", 7, TEAL), ("AMERICAS 8", 8, BLUE), ("MIDDLE EAST 6", 6, (180, 140, 0)),
           ("EUROPE 5", 5, PURPLE), ("AFRICA 3", 3, RED), ("WORLD 2", 2, (90, 90, 90))]
x = 0
for name, n, col in regions:
    wseg = int(round(n / 31 * W))
    d.rectangle([x, 150, x + wseg, 172], fill=col)
    text(x + 6, 155, name, f(LIB_SANS_B, 12), WHITE)
    x += wseg

# ---------------- UTC strip ----------------
text(16, 175, "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles   ~18:00 IPO $97.17",
     f(LIB_SANS, 11), DARKGRAY)
text(W - 16, 175, "~ APPROX", f(LIB_SANS_B, 11), GRAY, anchor="ra")

# ---------------- hero scenes ----------------
SC_Y0, SC_Y1 = 188, 296
COLW = 341
# scene 1: Kospi chart + skyline
x0 = 0
d.rectangle([x0, SC_Y0, x0 + COLW, SC_Y1], fill=NAVY)
text(x0 + 10, SC_Y0 + 6, "-3.3%", f(LIB_SANS_B, 30), (255, 80, 60))
pts = [(10, 250), (50, 235), (90, 248), (130, 225), (170, 238), (210, 215), (250, 228), (290, 205), (330, 218)]
d.line(pts, fill=ORANGE, width=3)
for px, py in pts:
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 200, 90))
import random
random.seed(7)
bx = 12
while bx < 330:
    bw = random.randint(14, 26)
    bh = random.randint(18, 42)
    d.rectangle([bx, SC_Y1 - bh, bx + bw, SC_Y1], fill=(20, 45, 95))
    for wy in range(SC_Y1 - bh + 5, SC_Y1 - 3, 8):
        for wx in range(bx + 3, bx + bw - 2, 6):
            d.rectangle([wx, wy, wx + 2, wy + 3], fill=(255, 220, 100))
    bx += bw + 4
# scene 2: Guterres globe
x0 = 342
d.rectangle([x0, SC_Y0, x0 + COLW, SC_Y1], fill=TEAL)
text(x0 + 12, SC_Y0 + 8, "150 DELEGATES", f(LIB_SANS_B, 26), GOLD)
text(x0 + 12, SC_Y0 + 38, "BACK A RISK", f(LIB_SANS_B, 26), GOLD)
text(x0 + 12, SC_Y0 + 68, "FRAMEWORK", f(LIB_SANS_B, 26), GOLD)
gx, gy, gr = x0 + 285, SC_Y0 + 72, 27
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=WHITE, width=2)
d.ellipse([gx - 12, gy - gr, gx + 12, gy + gr], outline=WHITE, width=1)
d.line([gx - gr, gy, gx + gr, gy], fill=WHITE, width=1)
d.arc([gx - gr, gy - 14, gx + gr, gy + 14], 0, 360, fill=WHITE, width=1)
# scene 3: Power Index bars
x0 = 684
d.rectangle([x0, SC_Y0, x0 + COLW, SC_Y1], fill=CREAM)
text(x0 + 10, SC_Y0 + 4, "NARROWEST SINCE 2018", f(LIB_SANS_B, 13), BLACK)
text(x0 + COLW - 10, SC_Y0 + 4, "GAP 5.3", f(LIB_SANS_B, 13), (150, 110, 0), anchor="ra")
bars = [("78.9", "US", BLUE, 44), ("73.6", "CHINA", RED, 41), ("40.5", "INDIA", (180, 140, 0), 23)]
for i, (val, lab, col, bh) in enumerate(bars):
    bx = x0 + 22 + i * 108
    btop = SC_Y1 - 22 - bh
    text(bx + 45, btop - 20, val, f(LIB_SANS_B, 16), BLACK, anchor="ma")
    d.rectangle([bx, btop, bx + 90, SC_Y1 - 22], fill=col)
    text(bx + 45, SC_Y1 - 22 - 15, lab, f(LIB_SANS_B, 12), WHITE, anchor="ma")

# captions under scenes
caps = ["KOSPI 4,708.54  \u00b7  -161 PTS", "UN  \u00b7  BRIDGETOWN", "ASIA POWER INDEX 2026"]
for i, cap in enumerate(caps):
    x0 = i * 342
    d.rectangle([x0, 296, x0 + COLW, 314], fill=BLACK)
    text(x0 + 10, 300, cap, f(LIB_SANS_B, 12), WHITE)

# ---------------- hero text ----------------
heroes = [
    ("1", "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE", "REPORTED", BLUE),
    ("2", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
     "UNITED NATIONS", "REPORTED", BLUE),
    ("3", "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE", "REPORTED", BLUE),
]
for i, (num, head, body, src, chiplab, chipcol) in enumerate(heroes):
    x0 = i * 342 + 10
    # number circle
    d.ellipse([x0, 320, x0 + 20, 340], fill=RED)
    text(x0 + 10, 321, num, f(LIB_SANS_B, 13), WHITE, anchor="ma")
    hl = wrap(head, f(LIB_SANS_B, 18), 300)
    for j, ln in enumerate(hl[:2]):
        text(x0 + 26, 318 + j * 21, ln, f(LIB_SANS_B, 18), BLACK)
    bl = wrap(body, f(LIB_SANS, 12), 320)
    for j, ln in enumerate(bl[:2]):
        text(x0, 362 + j * 15, ln, f(LIB_SANS, 12), DARKGRAY)
    text(x0, 390, src, f(LIB_SANS, 10), GRAY)
    cw = int(d.textlength(chiplab, font=f(LIB_SANS_B, 10))) + 10
    chip(i * 342 + 333 - cw, 388, chiplab, chipcol)

# ---------------- MORE bar ----------------
d.rectangle([0, 404, W, 422], fill=BLACK)
text(16, 408, "MORE OF THE DAY  \u2014  10 STORIES", f(LIB_SANS_B, 13), WHITE)

# ---------------- cards ----------------
cards = [
    ("AMERICAS", TEAL, "BESSENT: NVIDIA ANSWERS", "Treasury chief wants China answers.", "Reuters", "REPORTED", BLUE),
    ("FBI", RED, "FBI PROBES NCIC HACK", "Hackers hit police NCIC database.", "AP", "REPORTED", BLUE),
    ("WHITE HOUSE", (180, 140, 0), "TRUMP: IRAN STRIKES MAY RESUME", "Strikes may resume in New Year.", "Reuters", "REPORTED", BLUE),
    ("MARKETS", BLUE, "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", "REPORTED", BLUE),
    ("SPORT", RED, "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED", BLUE),
    ("SPORT", RED, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.", "ESPN", "REPORTED", BLUE),
    ("LEGAL", PURPLE, "STATES SUE SPACEX", "Ten states challenge AI claims.", "AP", "REPORTED", BLUE),
    ("TECH", BLUE, "ANTHROPIC IPO: $107.3B", "Raised at $83; closes $97.17.", "WSJ", "REPORTED", BLUE),
    ("EUROPE", (180, 140, 0), "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed.", "AP", "CLAIM", RED),
    ("SPACE", (90, 90, 90), "RUSSIAN NUCLEAR SATELLITE", "Intel: satellite may carry a nuke.", "Reuters", "CLAIM", RED),
]
for i, (cat, catcol, head, body, src, chiplab, chipcol) in enumerate(cards):
    row, c = divmod(i, 5)
    x0 = c * 205 + 4
    y0 = 422 + row * 74
    d.rectangle([x0, y0, x0 + 197, y0 + 15], fill=catcol)
    text(x0 + 4, y0 + 2, cat, f(LIB_SANS_B, 10), WHITE)
    text(x0 + 193, y0 + 2, str(i + 1), f(LIB_SANS_B, 10), WHITE, anchor="ra")
    hl = wrap(head, f(LIB_SANS_B, 13), 193)
    for j, ln in enumerate(hl[:2]):
        text(x0 + 2, y0 + 18 + j * 15, ln, f(LIB_SANS_B, 13), BLACK)
    text(x0 + 2, y0 + 50, body, f(LIB_SANS, 11), DARKGRAY)
    text(x0 + 2, y0 + 63, src, f(LIB_SANS, 10), GRAY)
    cw = int(d.textlength(chiplab, font=f(LIB_SANS_B, 10))) + 10
    chip(x0 + 197 - cw, y0 + 61, chiplab, chipcol)

# ---------------- WHERE / ALSO bar ----------------
d.rectangle([0, 570, W, 588], fill=BLACK)
text(16, 574, "WHERE IT HAPPENED", f(LIB_SANS_B, 13), WHITE)
text(348, 574, "ALSO ON MONDAY", f(LIB_SANS_B, 13), WHITE)

# ---------------- map ----------------
d.rectangle([0, 588, 330, 826], fill=(245, 248, 240))
for gx in range(0, 331, 22):
    d.line([gx, 588, gx, 826], fill=(225, 232, 220), width=1)
for gy in range(588, 827, 22):
    d.line([0, gy, 330, gy], fill=(225, 232, 220), width=1)
# stylised land blobs
d.ellipse([15, 600, 150, 790], fill=(165, 205, 150))
d.ellipse([150, 590, 310, 770], fill=(165, 205, 150))
d.ellipse([150, 770, 250, 825], fill=(165, 205, 150))
d.ellipse([255, 775, 320, 822], fill=(165, 205, 150))
pins = [(280, 630), (95, 750), (295, 605), (50, 685), (70, 660), (230, 665),
        (40, 635), (25, 705), (50, 740), (105, 770), (215, 615), (230, 640), (250, 620)]
for i, (px, py) in enumerate(pins, 1):
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=WHITE, width=1)
    text(px, py - 5, str(i), f(LIB_SANS_B, 9), WHITE, anchor="ma")
text(10, 792, "Pins 1\u201313:  1 Seoul  \u00b7  2 Bridgetown  \u00b7  3 Beijing", f(LIB_SANS, 10), DARKGRAY)
text(10, 804, "4 Washington  \u00b7  5 New York  \u00b7  6 Tehran  \u00b7  7 Chicago", f(LIB_SANS, 10), DARKGRAY)
text(10, 816, "8 SF  \u00b7  9 Denver  \u00b7  10 Austin  \u00b7  11 Warsaw  \u00b7  12 Kyiv  \u00b7  13 Moscow", f(LIB_SANS, 10), DARKGRAY)

# ---------------- ALSO list ----------------
also = [
    "14. Paris: 100+ back 2% billionaire tax",
    "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week",
    "17. COP31: the day after pact rejected",
    "18. Benghazi: UN demands port probe",
    "19. Israel unity talks resume",
    "20. Gaza: two killed in Israeli strike",
    "21. West Bank settler attacks",
    "22. Iran war: no deal in sight",
    "23. Lebanon seizes 264 kg explosives",
    "24. Bahrain: strike hits plant, 2 hurt",
    "25. Sudan: defences down drones",
    "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits in exam row",
    "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
for i, item in enumerate(also):
    col = i // 9
    row = i % 9
    x = 348 + col * 340
    y = 594 + row * 26
    text(x, y, item, f(LIB_SANS, 12), BLACK)

# ---------------- DATE CHECK ----------------
d.rectangle([0, 828, W, 912], outline=RED, width=2)
text(16, 834, "DATE CHECK", f(LIB_SANS_B, 15), RED)
text(W - 16, 837, "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", f(LIB_SANS_B, 10), RED, anchor="ra")
text(16, 856, "LEFT OUT \u2014 NOT 23 NOV:  Democrats reach 258 seats (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo Isidro captured (22 Nov)  \u00b7", f(LIB_SANS, 12), BLACK)
text(16, 872, "EU-Indonesia pact (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar ruling (19 Nov)", f(LIB_SANS, 12), BLACK)
text(16, 890, "NOT YET:  Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff", f(LIB_SANS, 12), BLACK)

# ---------------- footer ----------------
text(16, 918, "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).", f(LIB_SANS, 10), GRAY)
text(16, 932, "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side's claim, not independently confirmed \u00b7 ONGOING = still developing.", f(LIB_SANS, 10), GRAY)
text(16, 946, "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.", f(LIB_SANS, 10), GRAY)

# ---------------- bottom bar ----------------
d.rectangle([0, 962, W, 1024], fill=BLACK)
text(W // 2, 980, "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions",
     f(LIB_SANS_B, 18), GOLD, anchor="ma")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
